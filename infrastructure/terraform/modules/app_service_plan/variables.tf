variable "service_plan_name" {
  description = "The name of the Service Plan"
  type        = string
  sensitive   = false
  nullable = false

  validation {
    condition     = length(var.service_plan_name) >= 1 && length(var.service_plan_name) <= 40
    error_message = "The service plan name must be between 1 and 40 characters."
  }
}

variable "resource_group_name" {
  description = "The name of the Resource Group"
  type        = string
  sensitive   = false
  nullable = false

  validation {
    condition     = length(var.resource_group_name) >= 1 && length(var.resource_group_name) <= 90
    error_message = "The resource group name must be between 1 and 90 characters."
  }
}

variable "location" {
  description = "The location of the Resource Group"
  type        = string
  sensitive   = false
  nullable = false
}

variable "environment" {
  description = "The environment in which the resources are deployed"
  type        = string
  sensitive   = false
  nullable = false
}
