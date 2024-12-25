# Azure Setup Instructions

This document provides step-by-step instructions to set up Azure for the project and obtain the necessary data for GitHub Actions secrets.

---

## **Step 1: Log in to Azure**

1. Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
2. Log in to an Azure account:
   ```bash
   az login
   ```
   - A browser window will open for authentication.
   - After successful login, a JSON output of account details will be displayed.

---

## **Step 2: Check the Subscription**

1. List all available subscriptions:
   ```bash
   az account list --output table
   ```
2. Set the subscription to use:
   ```bash
   az account set --subscription <subscription-id>
   ```
3. Verify the active subscription:
   ```bash
   az account show
   ```
   Output:
   ```json
   {
     "id": "<subscription-id>",
     "name": "<subscription-name>",
     "tenantId": "<tenant-id>",
     "user": {
       "name": "user@example.com",
       "type": "user"
     }
   }
   ```

   - **`id`**: This is the `subscriptionId`.
   - **`tenantId`**: This is the `tenantId`.

---

## **Step 3: Manually Create a Service Principal**

Service Principals are essential for authenticating GitHub Actions with Azure. For security and control, it is recommended to create Service Principals manually, especially for Production environments.

### **Why Configure Manually?**
1. **Security**: Manual creation ensures that secrets (e.g., client secrets) are not exposed in logs or Terraform state files.
2. **Control**: Allows verification of roles and permissions before integration with automation.
3. **Best Practices**: Minimizes the risk of misconfiguration during automated deployments for Production environments.
4. **Terraform Limitation**: Terraform stores sensitive data like client secrets in its state file, which can pose a security risk.

### **How to Create a Service Principal Manually**

1. Create a Service Principal for the project environment (e.g., `DEV`, `STAGING`, `PROD`):
   ```bash
   az ad sp create-for-rbac --name "<MyServicePrincipal>-DEV" --role="Contributor" --scopes="/subscriptions/<subscription-id>" --sdk-auth
   ```
   Example output:
   ```json
   {
     "clientId": "<client-id>",
     "clientSecret": "<client-secret>",
     "subscriptionId": "<subscription-id>",
     "tenantId": "<tenant-id>",
     "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
     "resourceManagerEndpointUrl": "https://management.azure.com/",
     "activeDirectoryGraphResourceId": "https://graph.windows.net/",
     "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
     "galleryEndpointUrl": "https://gallery.azure.com/",
     "managementEndpointUrl": "https://management.core.windows.net/"
   }
   ```
2. Save the output securely. The following fields will be needed for GitHub Actions secrets:
   - `clientId` → `AZURE_CLIENT_ID`
   - `clientSecret` → `AZURE_CLIENT_SECRET`
   - `subscriptionId` → `AZURE_SUBSCRIPTION_ID`
   - `tenantId` → `AZURE_TENANT_ID`

3. Repeat this process for each environment (`DEV`, `STAGING`, `PROD`) with unique names like `MyServicePrincipal-STAGING` and `MyServicePrincipal-PROD`.

---

## **Step 4: Add Secrets to GitHub Actions**

1. Go to the GitHub repository.
2. Navigate to **Settings** → **Secrets and variables** → **Actions**.
3. Add the following secrets for each environment (e.g., `DEV`, `STAGING`, `PROD`):
   - **`AZURE_CLIENT_ID`**: From the `clientId` field.
   - **`AZURE_CLIENT_SECRET`**: From the `clientSecret` field.
   - **`AZURE_SUBSCRIPTION_ID`**: From the `subscriptionId` field.
   - **`AZURE_TENANT_ID`**: From the `tenantId` field.

For example:
- `DEV_AZURE_CLIENT_ID`
- `DEV_AZURE_CLIENT_SECRET`
- `DEV_AZURE_SUBSCRIPTION_ID`
- `DEV_AZURE_TENANT_ID`

Repeat the process for `STAGING` and `PROD`.

![alt text](/assets/github-actions-secrets.png)

---

## **Step 5: (Optional) Reset the Client Secret**

If the `clientSecret` is lost, reset it with the following command:
```bash
az ad sp credential reset --name "MyServicePrincipal-DEV"
```
Example output:
```json
{
  "appId": "<client-id>",
  "password": "<new-client-secret>",
  "tenant": "<tenant-id>"
}
```
- Use the new `password` as `AZURE_CLIENT_SECRET`.

---

## **Step 6: Obtain OpenAI API Keys (if applicable)**

1. Log in to the [OpenAI Dashboard](https://platform.openai.com/).
2. Navigate to **API Keys**.
3. Create API keys for each environment (`DEV`, `STAGING`, `PROD`).
4. Add the keys to GitHub Actions secrets:
   - `DEV_OPENAI_API_KEY`
   - `STAGING_OPENAI_API_KEY`
   - `PROD_OPENAI_API_KEY`

---

## **Verification**

1. Ensure all secrets are added to GitHub:
   - Go to **Settings** → **Secrets and variables** → **Actions**.
   - Verify the presence of all required secrets.
2. Run the GitHub Actions workflow and confirm it uses the correct secrets.

---

The Azure setup is now complete, and the necessary data has been added to GitHub Actions secrets.

