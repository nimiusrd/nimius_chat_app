terraform {
  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.0"
    }
  }
}

# Configures the provider to use the resource block's specified project for quota checks.
provider "google-beta" {
  user_project_override = true
}

# Configures the provider to not use the resource block's specified project for quota checks.
# This provider should only be used during project creation and initializing services.
provider "google-beta" {
  alias                 = "no_user_project_override"
  user_project_override = false
}

# Creates a new Google Cloud project.
resource "google_project" "default" {
  provider = google-beta.no_user_project_override

  name       = var.project_name
  project_id = var.project_id
  # Required for any service that requires the Blaze pricing plan
  # (like Firebase Authentication with GCIP)
  billing_account = var.billing_account

  # Required for the project to display in any list of Firebase projects.
  labels = {
    "firebase" = "enabled"
  }
}

# Enables required APIs.
resource "google_project_service" "default" {
  provider = google-beta.no_user_project_override
  project  = google_project.default.project_id
  for_each = toset([
    "cloudbilling.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "firebase.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "cloudkms.googleapis.com",
    # Enabling the ServiceUsage API allows the new project to be quota checked from now on.
    "serviceusage.googleapis.com",
    # Enabling the Text-to-Speech API for the new project.
    "texttospeech.googleapis.com",
  ])
  service = each.key

  # Don't disable the service if the resource block is removed by accident.
  disable_on_destroy = false
}

resource "google_kms_key_ring" "tfstate_key_ring" {
  project  = google_project.default.project_id
  name     = "tfstate-key-ring"
  location = var.region
}

resource "google_kms_crypto_key" "tfstate_crypto_key" {
  name            = "tfstate-crypto-key"
  key_ring        = google_kms_key_ring.tfstate_key_ring.id
  rotation_period = "100000s"

  lifecycle {
    prevent_destroy = true
  }
}

data "google_storage_project_service_account" "gcs_account" {
  project = google_project.default.project_id
}

resource "google_kms_crypto_key_iam_binding" "binding" {
  crypto_key_id = google_kms_crypto_key.tfstate_crypto_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"

  members = ["serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"]
}

resource "google_storage_bucket" "tfstate_bucket" {
  project  = google_project.default.project_id
  name     = "${var.project_id}-tfstate"
  location = var.region

  encryption {
    default_kms_key_name = google_kms_crypto_key.tfstate_crypto_key.id
  }

  depends_on = [google_kms_crypto_key_iam_binding.binding]
}

# Enables Firebase services for the new project created above.
resource "google_firebase_project" "default" {
  provider = google-beta
  project  = google_project.default.project_id

  # Waits for the required APIs to be enabled.
  depends_on = [
    google_project_service.default
  ]
}

resource "google_firebase_web_app" "default" {
  provider        = google-beta
  project         = google_project.default.project_id
  display_name    = var.firebase_app_name
  deletion_policy = "DELETE"
}

data "google_firebase_web_app_config" "default" {
  provider   = google-beta
  project    = google_project.default.project_id
  web_app_id = google_firebase_web_app.default.app_id
}

resource "google_firebase_hosting_site" "default" {
  provider = google-beta.no_user_project_override
  project  = google_project.default.project_id
  site_id  = var.firebase_app_site_id
  app_id   = google_firebase_web_app.default.app_id
}

resource "google_secret_manager_secret" "terraform_tfvars" {
  project   = google_project.default.project_id
  secret_id = "terraform_tfvars"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "backend_config_toml" {
  project   = google_project.default.project_id
  secret_id = "backend_config_toml"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "frontend_dotenv" {
  project   = google_project.default.project_id
  secret_id = "frontend_dotenv"

  replication {
    auto {}
  }
}

resource "google_service_account" "artifact_registry_sa" {
  project                      = google_project.default.project_id
  account_id                   = "artifact-registry"
  display_name                 = "Service Account for Artifact Registry"
  create_ignore_already_exists = true
}

resource "google_project_iam_member" "artifact_registry_admin" {
  project = var.project_id
  role    = "roles/artifactregistry.admin"
  member  = "serviceAccount:${google_service_account.artifact_registry_sa.email}"
}

resource "google_artifact_registry_repository" "backend" {
  provider      = google-beta
  project       = var.project_id
  location      = var.region
  repository_id = "backend"
  description   = "Docker repository for the backend service"
  format        = "DOCKER"

  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "delete-all-images"
    action = "DELETE"
    condition {

    }
  }
  cleanup_policies {
    id     = "keep-latest-version"
    action = "KEEP"
    most_recent_versions {
      keep_count = 1
    }
  }
}

resource "google_artifact_registry_repository" "builder" {
  provider      = google-beta
  project       = var.project_id
  location      = var.region
  repository_id = "builder"
  description   = "Docker repository for builder images"
  format        = "DOCKER"

  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "delete-all-images"
    action = "DELETE"
    condition {

    }
  }
  cleanup_policies {
    id     = "keep-latest-version"
    action = "KEEP"
    most_recent_versions {
      keep_count = 1
    }
  }
}

resource "google_service_account" "cloud_build_sa" {
  project                      = google_project.default.project_id
  account_id                   = "cloud-build"
  display_name                 = "Service Account for Cloud Build"
  create_ignore_already_exists = true
}

resource "google_project_iam_member" "cloud_build_sa_member" {
  for_each = toset([
    "roles/serviceusage.serviceUsageConsumer",
    "roles/cloudbuild.builds.builder",
    "roles/storage.admin",
    "roles/iam.serviceAccountUser",
    "roles/secretmanager.secretAccessor",
    "roles/run.admin",
    "roles/firebase.admin",
    "roles/artifactregistry.admin",
  ])
  project = google_project.default.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.cloud_build_sa.email}"
}

resource "google_cloudbuild_trigger" "deploy-to-cloud-run" {
  project = google_project.default.project_id
  name    = "deploy-to-cloud-run"

  github {
    owner = var.github_owner
    name  = var.github_repo_name
    push {
      branch = "main"
    }
  }

  filename = "backend/cloudbuild.yaml"
  included_files = [
    "backend/**"
  ]
  service_account = google_service_account.cloud_build_sa.id


  substitutions = {
    "_LOCATION"     = var.region
    "_SERVICE_NAME" = var.backend_service_name
  }
}

resource "google_cloudbuild_trigger" "deploy-to-firebase-hosting" {
  project = google_project.default.project_id
  name    = "deploy-to-firebase-hosting"

  github {
    owner = var.github_owner
    name  = var.github_repo_name
    push {
      branch = "main"
    }
  }

  filename = "frontend/cloudbuild.yaml"
  included_files = [
    "frontend/**"
  ]
  service_account = google_service_account.cloud_build_sa.id


  substitutions = {
    "_LOCATION" = var.region
  }
}

resource "google_cloudbuild_trigger" "create-firebase-builder" {
  project = google_project.default.project_id
  name    = "create-firebase-builder"

  github {
    owner = var.github_owner
    name  = var.github_repo_name
    push {
      branch = "builder"
    }
  }

  filename        = "firebase/cloudbuild.yaml"
  service_account = google_service_account.cloud_build_sa.id

  substitutions = {
    "_LOCATION" = var.region
  }
}

resource "google_cloudbuild_trigger" "run-terraform-apply" {
  project = google_project.default.project_id
  name    = "run-terraform-apply"

  github {
    owner = var.github_owner
    name  = var.github_repo_name
    push {
      branch = "main"
    }
  }

  included_files = [
    "*.tf",
    "cloudbuild.terraform-apply.yaml"
  ]

  filename        = "cloudbuild.terraform-apply.yaml"
  service_account = google_service_account.cloud_build_sa.id
  approval_config {
    approval_required = true
  }
}

resource "google_cloudbuild_trigger" "run-terraform-plan" {
  project = google_project.default.project_id
  name    = "run-terraform-plan"

  github {
    owner = var.github_owner
    name  = var.github_repo_name
    push {
      branch = ".*"
    }
  }

  included_files = [
    "*.tf",
    "cloudbuild.terraform-plan.yaml"
  ]

  filename        = "cloudbuild.terraform-plan.yaml"
  service_account = google_service_account.cloud_build_sa.id
}
