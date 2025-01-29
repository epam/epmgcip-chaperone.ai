output "function_app_name" {
  description = "Name of the Azure Function App"
  sensitive   = false
  value       = module.function_app.name
}

output "function_app_url" {
  description = "URL of the Azure Function App"
  value       = module.function_app.url
}

output "resource_group_name" {
  description = "The name of the Resource Group"
  sensitive   = false
  value       = module.resource_group.name
}

output "storage_account_name" {
  description = "The name of the Storage Account"
  sensitive   = true
  value       = module.storage_account.name
}

output gh_uai_client_id {
  description = "Client ID of the GitHub User Assigned Identity"
  value       = module.gh_uai.user_assigned_identity_client_id
}
