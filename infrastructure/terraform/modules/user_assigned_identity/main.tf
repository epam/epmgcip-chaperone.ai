resource "azurerm_user_assigned_identity" "msi" {
  location            = var.location
  name                = var.name
  resource_group_name = var.resource_group_name
}

# Federated Identity for main branches
resource "azurerm_federated_identity_credential" "branches_credential" {
  resource_group_name = var.resource_group_name
  for_each            = toset(var.branches)
  name                = "github-actions-${each.key}"
  parent_id           = azurerm_user_assigned_identity.msi.id
  issuer              = var.issuer_url
  subject             = "repo:${var.github_organization}/${var.github_repository}:ref:refs/heads/${each.key}"
  audience            = [var.audience_name]
}

# Federated Identity for Pull Requests
resource "azurerm_federated_identity_credential" "pull_requests_credential" {
  resource_group_name = var.resource_group_name
  name                = "github-actions-pull-requests"
  parent_id           = azurerm_user_assigned_identity.msi.id
  issuer              = var.issuer_url
  subject             = "repo:${var.github_organization}/${var.github_repository}:pull_request"
  audience            = [var.audience_name]
}

resource "azurerm_role_assignment" "github_actions_role_assignment" {
  principal_id         = azurerm_user_assigned_identity.msi.principal_id
  role_definition_name = "Contributor"
  scope                = data.azurerm_subscription.primary.id
}

data "azurerm_subscription" "primary" {}
