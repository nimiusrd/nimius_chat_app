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
