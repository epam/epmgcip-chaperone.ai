variable "location" {
  description = "The location where the user-assigned managed identity will be created."
  type        = string
}

variable "name" {
  description = "The name of the user-assigned managed identity."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group in which the user-assigned managed identity will be created."
  type        = string
}

variable "branches" {
  description = "List of branches for federated identity"
  type        = list(string)
  default     = ["main", "master"]
}

variable "github_organization" {
  description = "GitHub organization name"
  type        = string
}

variable "github_repository" {
  description = "GitHub repository name"
  type        = string
}

variable "audience_name" {
  description = "The audience name for the federated identity"
  type        = string
}

variable "issuer_url" {
  description = "The issuer URL for the federated identity"
  type        = string
}
