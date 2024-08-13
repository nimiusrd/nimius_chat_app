variable "project_name" {
  type        = string
  description = "The display name of the Firebase project"
}

variable "project_id" {
  type        = string
  description = "The GCP project to deploy resources"
}

variable "billing_account" {
  type        = string
  sensitive   = true
  description = "The billing account to associate with the project"
}

variable "region" {
  default     = "asia-northeast1"
  type        = string
  description = "The region to deploy resources"
}

variable "zone" {
  default     = "asia-northeast1-a"
  type        = string
  description = "The zone to deploy resources"
}

variable "firebase_app_name" {
  type        = string
  description = "The display name of the Firebase app"
}

variable "firebase_bucket_name" {
  type        = string
  description = "The name of the Firebase storage bucket"
}

variable "firebase_app_site_id" {
  type        = string
  description = "The ID of the Firebase app's site"
}

variable "backend_service_name" {
  type        = string
  description = "The name of the backend service"
}

variable "github_repo_name" {
  description = "The name of the GitHub repository"
  type        = string
}

variable "github_owner" {
  description = "The owner of the GitHub repository"
  type        = string
}
