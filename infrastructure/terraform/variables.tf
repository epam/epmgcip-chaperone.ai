variable "environment" {
  description = "The environment in which the resources are deployed"
  type        = string
  sensitive   = false
  nullable    = false

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
  description = "The Azure region for resources"
  default     = "Central US"
  type        = string
  sensitive   = false
}

variable "storage_account_name" {
  description = "The name of the Storage Account"
  type        = string
  sensitive   = false
  nullable    = false
}

variable "function_app_name" {
  description = "The name of the Function App"
  type        = string
  sensitive   = false
  nullable    = false

  validation {
    condition     = length(var.function_app_name) >= 1 && length(var.function_app_name) <= 60 && var.function_app_name == lower(var.function_app_name)
    error_message = "The function app name must be between 1 and 60 characters, consist of lowercase letters, numbers, and hyphens only."
  }
}

variable "service_plan_name" {
  description = "The name of the Service Plan"
  type        = string
  sensitive   = false
  nullable    = false

  validation {
    condition     = length(var.service_plan_name) >= 1 && length(var.service_plan_name) <= 40
    error_message = "The service plan name must be between 1 and 40 characters."
  }
}

# Define the OPENAI_API_KEY variable
variable "OPENAI_API_KEY" {
  description = "API Key for OpenAI services"
  type        = string
  sensitive   = true
  nullable    = false
}
