output "config" {
  value = {
    projectId         = google_firebase_project.default.project
    appId             = google_firebase_web_app.default.app_id
    apiKey            = data.google_firebase_web_app_config.default.api_key
    authDomain        = data.google_firebase_web_app_config.default.auth_domain
    storageBucket     = lookup(data.google_firebase_web_app_config.default, "storage_bucket", "")
    messagingSenderId = lookup(data.google_firebase_web_app_config.default, "messaging_sender_id", "")
    measurementId     = lookup(data.google_firebase_web_app_config.default, "measurement_id", "")
  }
}

output "need-to-set-secret" {
  description = "Set the secret in the Secret Manager."
  value = {
    url                 = "https://console.cloud.google.com/security/secret-manager?project=${google_project.default.project_id}"
    backend_config_toml = google_secret_manager_secret.backend_config_toml.id
    frontend_dotenv     = google_secret_manager_secret.frontend_dotenv.id
    terraform_tfvars    = google_secret_manager_secret.terraform_tfvars.id
  }
}

output "service-account" {
  description = "Service account for Artifact Registry"
  value = {
    artifact_registry = google_service_account.artifact_registry_sa.email
    cloud_build       = google_service_account.cloud_build_sa.email
  }
}

output "bucket" {
  description = "The name of the Firebase storage bucket"
  value = {
    tfstate_bucket = google_storage_bucket.tfstate_bucket.name
  }
}
