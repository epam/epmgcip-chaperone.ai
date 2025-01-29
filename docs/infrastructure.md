# **Azure Function App Deployment with Terraform**

This repository contains the infrastructure-as-code (IaC) configuration for deploying an Azure Function App using Terraform. The setup leverages **Terraform Cloud** for state management and **GitHub Actions** for CI/CD automation.

---

## **Features**
- Automated deployment of Azure infrastructure:
  - Azure Resource Group
  - Azure Storage Account
  - Azure App Service Plan
  - Azure Function App
- Environment-specific configurations (`DEV`, `STAGING`, `PROD`)
- Secure secrets management via GitHub Secrets and Terraform Cloud variables
- Manual and automatic workflow triggers for different environments

---

## **Prerequisites**
### 1. **Azure Subscription**
You must have an active Azure subscription.

### 2. **Create an Azure Service Principal**
A Service Principal is needed for Terraform to interact with your Azure subscription. Follow these steps:

#### **Step 1: Login to Azure CLI**
Run the following command to log in to Azure:
```bash
az login
```

#### **Step 2: Create a Service Principal**
Execute the following command to create a Service Principal:
```bash
az ad sp create-for-rbac --role "User Access Administrator" --scopes /subscriptions/<YOUR_SUBSCRIPTION_ID>
```

Replace `<YOUR_SUBSCRIPTION_ID>` with your Azure Subscription ID.

#### **Step 3: Save the Output**
The command will output the following JSON:
```json
{
  "appId": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "displayName": "azure-cli-2023-XX-XX-XX",
  "password": "XXXXXXXXXXXXXXXXXXXXXXXX",
  "tenant": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
}
```
Take note of the following values:
- **`appId`** → This is your `ARM_CLIENT_ID`.
- **`password`** → This is your `ARM_CLIENT_SECRET`.
- **`tenant`** → This is your `ARM_TENANT_ID`.
- Your **Subscription ID** is your `ARM_SUBSCRIPTION_ID`.

---

### 3. **Terraform Cloud Account**
1. Sign up for [Terraform Cloud](https://app.terraform.io).
2. Create an **organization** in Terraform Cloud.
3. Generate a **Terraform Cloud API Token**:
   - Go to **User Settings** > **Tokens** > **Create an API token**.
   - Save the token securely.

---

## **Setup**

### **1. Terraform Cloud Workspace Configuration**
Create workspaces in Terraform Cloud for each environment (`DEV`, `STAGING`, `PROD`).

Add the following **Environment Variables** in project variable set (e.g. "Azure"):

| Key                   | Type      | Value                          | Category |
|-----------------------|-----------|--------------------------------|----------|
| `ARM_SUBSCRIPTION_ID` | Sensitive | Azure Subscription ID          | Env      |
| `ARM_TENANT_ID`       | Sensitive | Azure Tenant ID                | Env      |

#### Workspace Variables:
Add the following **Environment Variables** in each workspace:

| Key                   | Type      | Value                          | Category |
|-----------------------|-----------|--------------------------------|----------|
| `ARM_CLIENT_ID`       | Sensitive | Azure Service Principal ID     | Env      |
| `ARM_CLIENT_SECRET`   | Sensitive | Azure Service Principal Secret | Env      |


Add the following **Terraform Variables** in each workspace:

| Key                   | Type      | Value                  | Category   |
|-----------------------|-----------|------------------------|------------|
| `environment`         | String    | `DEV`/`STAGING`/`PROD` | Terraform  |
| `function_app_name`   | String    | Azure Function name    | Terraform  |
| `OPENAI_API_KEY`      | Sensitive | Your OpenAI API key    | Terraform  |
| `resource_group_name` | String    | Azure Resource Group   | Terraform  |
| `service_plan_name`   | String    | App Service Plan Name  | Terraform  |
| `storage_account_name`| String    | Storage Account Name   | Terraform  |

---

### **2. GitHub Secrets Configuration**
Navigate to your repository’s **Settings** > **Secrets and variables** > **Actions**, and add the following secrets:

| Name                               | Value                           |
|------------------------------------|---------------------------------|
| `ARM_SUBSCRIPTION_ID`              | Azure Subscription ID           |
| `ARM_TENANT_ID`                    | Azure Tenant ID                 |
| `TF_API_TOKEN`                     | Terraform Cloud API Token       |
| `TF_CLOUD_ORGANIZATION`            | Terraform Cloud Organization    |
| `TF_CLOUD_WORKSPACE_BASE_NAME`     | Base name for workspaces (e.g., `myapp`) |

---

## **Deployment Workflows**

### **GitHub Actions Workflow**
The repository is configured with GitHub Actions to automate infrastructure deployment.

### **1. Automatic Deployment**
- **DEV Environment**: Triggered on pull requests to the `main` branch.
- **STAGING Environment**: Triggered on push to the `main` or `master` branch.

### **2. Manual Deployment**
For `PROD` or custom environments:
1. Go to the **Actions** tab in your repository.
2. Select the `Deploy to Azure with Terraform` workflow.
3. Click **Run workflow** and specify the desired environment (e.g., `PROD`).

---

## **Step-by-Step Instructions**

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-repo>.git
   cd <your-repo>
   ```

2. Push your code to the main branch to trigger the `STAGING` deployment:
   ```bash
   git add .
   git commit -m "Deploy infrastructure"
   git push origin main
   ```

3. To deploy manually (e.g., for `PROD`):
   - Go to **Actions** in GitHub.
   - Select `Deploy to Azure with Terraform`.
   - Click **Run workflow** and specify the environment.

---

## **Infrastructure Cleanup**

To destroy all resources, use the **Destroy Terraform Resources** workflow:
1. Go to **Actions** in GitHub.
2. Select `Destroy Terraform Resources`.
3. Trigger the workflow manually and specify the environment (e.g., `DEV`, `STAGING`, `PROD`).

---

## **Code Deployment**
1. Place your Azure Function code in the `functions` directory in the repository.
2. The function will be automatically deployed during the `Deploy` step.

---

## **Troubleshooting**

- **Workspace Not Found**: Ensure `TF_CLOUD_WORKSPACE_BASE_NAME` is correct and matches Terraform Cloud workspaces.
- **Authentication Errors**: Verify `ARM_*` environment variables are set correctly in Terraform Cloud.
- **Quota Errors**: Ensure your Azure subscription has sufficient quotas.
- **Function App Runtime Errors**: Confirm the correct runtime version in the function configuration.

---