output "function_app_name" {
  description = "Name of the Azure Function App"
  sensitive   = true
  value       = module.function_app.name
}

output "function_app_url" {
  description = "URL of the Azure Function App"
  value       = module.function_app.url
}

output "resource_group_name" {
  description = "The name of the Resource Group"
  sensitive   = true
  value       = module.resource_group.name
}

output "storage_account_name" {
  description = "The name of the Storage Account"
  sensitive   = true
  value       = module.storage_account.name
}
