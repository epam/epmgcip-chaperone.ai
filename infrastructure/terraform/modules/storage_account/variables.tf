variable "environment" {
  description = "The environment in which the resources are deployed"
  type        = string
  sensitive   = false
  nullable    = false
}

variable "storage_account_name" {
  description = "The name of the Storage Account"
  type        = string
  sensitive   = false
  nullable    = false

  validation {
    condition     = length(var.storage_account_name) >= 3 && length(var.storage_account_name) <= 24 && var.storage_account_name == lower(var.storage_account_name)
    error_message = "The storage account name must be between 3 and 24 characters, consist of lowercase letters and numbers only."
  }
}

variable "resource_group_name" {
  description = "The name of the Resource Group"
  type        = string
  sensitive   = false
  nullable    = false

  validation {
    condition     = length(var.resource_group_name) >= 1 && length(var.resource_group_name) <= 90
    error_message = "The resource group name must be between 1 and 90 characters."
  }
}

variable "location" {
  description = "The location of the Resource Group"
  type        = string
  sensitive   = false
  nullable    = false
}