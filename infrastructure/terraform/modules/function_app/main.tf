# Create a Linux-based Function App for hosting the Azure Function
resource "azurerm_linux_function_app" "function_app" {
  name                        = var.function_app_name
  location                    = var.location
  resource_group_name         = var.resource_group_name
  service_plan_id             = var.service_plan_id
  storage_account_name        = var.storage_account_name
  storage_account_access_key  = var.storage_account_access_key
  https_only                  = true

  site_config {
    application_stack {
      python_version = "3.11"
    }
    cors {
      allowed_origins = ["*"]
    }
  }

  # Application settings for the Function App
  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python" # Specifies the runtime (Python)
    "OPENAI_API_KEY"           = var.OPENAI_API_KEY
  }

  tags = {
    environment = var.environment
  }
}

# Function App Slot
resource "azurerm_linux_function_app_slot" "deployment_slot" {
  name                        = "deployment-slot"
  function_app_id             = azurerm_linux_function_app.function_app.id
  storage_account_name        = var.storage_account_name
  storage_account_access_key  = var.storage_account_access_key

  site_config {}

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
  }
}
