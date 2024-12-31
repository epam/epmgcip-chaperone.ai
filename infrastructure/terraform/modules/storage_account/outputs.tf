output "name" {
  description = "The name of the Storage Account"
  value = azurerm_storage_account.storage.name
  sensitive = true
}

output "primary_access_key" {
  description = "The primary access key of the Storage Account"
  value = azurerm_storage_account.storage.primary_access_key
  sensitive = true
}
