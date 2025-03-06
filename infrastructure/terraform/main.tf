terraform {
  cloud {}
}

# Module for creating a Resource Group
module "resource_group" {
  source              = "./modules/resource_group"
  environment         = var.environment
  resource_group_name = var.resource_group_name
  location            = var.location
  depends_on          = []
}

# Module for creating a Storage Account
module "storage_account" {
  source               = "./modules/storage_account"
  environment          = var.environment
  storage_account_name = var.storage_account_name
  resource_group_name  = module.resource_group.name
  location             = module.resource_group.location
  depends_on           = [module.resource_group]
}

# Module for creating an App Service Plan
module "app_service_plan" {
  source              = "./modules/app_service_plan"
  environment         = var.environment
  service_plan_name   = var.service_plan_name
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  depends_on          = [module.resource_group]
}

# Module for creating an Azure Function App
module "function_app" {
  source                     = "./modules/function_app"
  environment                = var.environment
  function_app_name          = var.function_app_name
  resource_group_name        = module.resource_group.name
  location                   = module.resource_group.location
  service_plan_id            = module.app_service_plan.id
  storage_account_name       = module.storage_account.name
  storage_account_access_key = module.storage_account.primary_access_key
  depends_on                 = [module.resource_group, module.storage_account, module.app_service_plan]
  OPENAI_API_KEY             = module.cognitive_account.api_key
}

# Module for creating a Cognitive Services Account
module "cognitive_account" {
  source                 = "./modules/cognitive_account"
  environment            = var.environment
  cognitive_account_name = var.cognitive_account_name
  resource_group_name    = module.resource_group.name
  location               = "eastus"
}

# Module for creating a User Assigned Identity
module "gh_uai" {
  source              = "./modules/user_assigned_identity"
  name                = "gh-uai-${var.environment}"
  location            = var.location
  resource_group_name = module.resource_group.name
  depends_on          = [module.resource_group]
  github_organization = var.github_organization
  github_repository   = var.github_repository
  audience_name       = local.default_audience_name
  issuer_url          = local.github_issuer_url
}
