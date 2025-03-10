resource "azurerm_cognitive_account" "openai" {
  name                  = var.cognitive_account_name
  location              = var.location
  resource_group_name   = var.resource_group_name
  kind                  = "OpenAI"
  sku_name              = "S0"
  custom_subdomain_name = var.cognitive_account_name

  network_acls {
    default_action = "Allow"
  }

  tags = {
    environment = var.environment
  }
}

resource "azurerm_cognitive_deployment" "chat_deployment" {
  name                 = "chat-deployment"
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    name    = var.chat_model
    format  = "OpenAI"
  }

  sku {
    name = "GlobalStandard"
  }
}
