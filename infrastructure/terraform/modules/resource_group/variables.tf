variable "environment" {
  description = "The environment in which the resources are deployed"
  type        = string
  sensitive   = false
  nullable    = false
}

variable "resource_group_name" {
  description = "The name of the Azure Resource Group"
  type        = string
  sensitive   = false
  nullable    = false

  validation {
    condition     = length(var.resource_group_name) >= 1 && length(var.resource_group_name) <= 90
    error_message = "The resource group name must be between 1 and 90 characters."
  }
}

variable "location" {
  description = "The Azure region for the Resource Group"
  type        = string
  sensitive   = false
  nullable    = false
}
