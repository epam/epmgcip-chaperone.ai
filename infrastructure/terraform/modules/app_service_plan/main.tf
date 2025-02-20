# Create a Consumption Plan (cost-efficient)
resource "azurerm_service_plan" "plan" {
  name                = var.service_plan_name
  location            = var.location
  resource_group_name = var.resource_group_name

  os_type = "Linux"
  sku_name = "Y1" # Y1 is the SKU for the Consumption Plan

  tags = {
    environment = var.environment
  }
}
