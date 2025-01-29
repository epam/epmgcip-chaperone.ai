output "name" {
  value     = azurerm_linux_function_app.function_app.name
  sensitive = false
}

output "url" {
  value = azurerm_linux_function_app.function_app.default_hostname
}
