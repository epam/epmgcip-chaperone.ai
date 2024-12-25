# Create a Resource Group to group related Azure resources
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name # Name of the Resource Group
  location = var.location            # Azure Region for the Resource Group

  tags = {
    environment = var.environment
  }
}
