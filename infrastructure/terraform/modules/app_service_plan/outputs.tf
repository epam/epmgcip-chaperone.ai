output "name" {
  description = "The name of the App Service Plan"
  value = azurerm_service_plan.plan.name
  sensitive = true
}

output "id" {
  description = "The ID of the App Service Plan"
  value = azurerm_service_plan.plan.id
  sensitive = true
}