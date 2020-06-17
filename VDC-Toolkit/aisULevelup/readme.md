# **To deploy Azure Virtual Datacenter for aisU Levelup**

aisU Levelup environment has following Azure resources deployed VNET, Storage Account, Key Vault, and Windows VM.

## Start learning about VDC Toolkit

- [Azure Virtual Datacenter Toolkit](https://github.com/Azure/vdc)
- [Quick Start Guide](https://github.com/Azure/vdc/blob/master/Docs/quickstart.md)

## Prepare your environment for deployment

### Clone the repository

These steps assume that the `git` command is on your path.

1. Open a terminal window
2. Navigate to a folder where you want to store the source for the toolkit. For, e.g. `c:\git`, navigate to that folder.
3. Run `git clone https://github.com/Azure/vdc.git`. This will clone the GitHub repository in a folder named `vdc`.
4. Run `cd vdc` to change directory in the source folder.
5. Run `git checkout master` to switch to the branch with the current in-development version of the toolkit.

### Build the Docker image

1. Ensure that the [Docker daemon](https://docs.docker.com/config/daemon/) is running. If you are new to Docker, the easiest way to do this is to install [Docker Desktop](https://www.docker.com/products/docker-desktop).
1. Open a terminal window
1. Navigate to the folder where you cloned the repository. _The rest of the quickstart assumes that this path is `C:\git\vdc\`_
1. Run `docker build . -t vdc:latest` to build the image.

### Run the toolkit container

After the image finishing building, you can run it using:

`docker run -it --entrypoint="pwsh" --rm -v C:\git\vdc\Config:/usr/src/app/Config -v C:\git\vdc\Environments:/usr/src/app/Environments -v C:\git\vdc\Modules:/usr/src/app/Modules vdc:latest`

A few things to note:

- You don't need to build the image every time you want to run the container. You'll only need to rebuild it if there are changes to the source (primarily changes in the `Orchestration` folder).
- The `docker run` command above will map volumes in the container to volumes on the host machine. This will allow you to directly modify files in these directories (`Config`,`Environments`, and `Modules`).

When the container starts, you will see the prompt
`PS /usr/src/app>`

## Configure the toolkit

To configure the toolkit for this quickstart, we will need to collect the following information.

You'll need:

- A subscription for the toolkit to use for logging and tracking deployment.
- The associated tenant id of the Azure Active Directory associated with those subscriptions.
- The object id of the user account that you'll use to run the deployment.
- The object id of a [service principal](https://docs.microsoft.com/azure/
- An organization name for generating a prefix for naming resources.
- The desired password of the Windows jumpbox.

Note: You can use a single subscription. You'll just need to provide the same subscription id in multiple locations in the configuration.

## Create new Environment - aisULevelUp

Copy the folder [aisULevelUp](.) to downloaded VDC toolkit project in Environments folder

### New environment in subscriptions

Add the new environment 'LEVELUP' in the [subscriptions.json](../../Environments/_Common/subscriptions.json). The deployment will look for the enviroment configurations to deploy. Set tenant and subscription id's

```JSON
"LEVELUP": {
    "Comments": "aisU Levelup demo (MSDN) subscription and tenant information",
    "TenantId": "000000-000-0000-0000",
    "SubscriptionId": "000000-000-0000-0000"
  }
```

**NOTE:**

Ignore the following environment variables and set the others as we are not going to run CI/CD pipeline, deploy Active Directory VM's, and Linux

```PowerShell
$ENV:DEVOPS_SERVICE_PRINCIPAL_USER_ID = "[SERVICE_PRINCIPAL_USER_ID]"
$ENV:DOMAIN_ADMIN_USERNAME = "[DOMAIN_ADMIN_USER_NAME]"
$ENV:DOMAIN_ADMIN_USER_PWD = "[DOMAIN_ADMIN_USER_PASSWORD]"
$ENV:ADMIN_USER_SSH = "[SSH_KEY]"
```

Set these environment variables and run in docker environment
```PowerShell

$ENV:ORGANIZATION_NAME = "[ORGANIZATION_NAME]"
$ENV:AZURE_ENVIRONMENT_NAME = "[AZURE_ENVIRONMENT]"
$ENV:AZURE_LOCATION = "[AZURE_REGION]"
$ENV:TENANT_ID = "[TENANT_ID]"
$ENV:SUBSCRIPTION_ID = "[SUBSCRIPTION_ID]"
$ENV:KEYVAULT_MANAGEMENT_USER_ID  = "[KEY_VAULT_MANAGEMENT_USER_ID]"
$ENV:ADMIN_USER_NAME = "[VM_ADMIN_USER_NAME]"
$ENV:ADMIN_USER_PWD = "[VM_ADMIN_USER_PASSWORD]"
$ENV:AZURE_DISCOVERY_URL = "https://management.azure.com/metadata/endpoints?api-version=2019-05-01"
```

## Setting the Parameters

Any application specific parameters updates should be done in the [parameters.json](../../Environments/aisULevelup/parameters.json) file such as IP address, subnet names, subnet range, secrets etc.

## Deploying the aisU Levelup environment

1. Return to the running Docker container from earlier in the quickstart.
1. If you have not already done so, run `Connect-AzAccount -Tenant "[TENANT_ID]" -SubscriptionId "[SUBSCRIPTION_ID]" -EnvironmentName "[AZURE_ENVIRONMENT]"` to login and set an Azure context.
2. Run the script to update config files with tenant & subscription id's
   
   ```Powershell
   ./Orchestration/OrchestrationService/Pre_req_script.ps1
   ```
3. To deploy the entire aisU Levelup environment, you can run a single command:

    ``` PowerShell
    ./Orchestration/OrchestrationService/ModuleConfigurationDeployment.ps1 -DefinitionPath ./Environments/aisULevelup/definition.json
    ```

The toolkit will begin deploying the constituent modules and the status will be sent to the terminal.
Open the [Azure portal](https://portal.azure.us) and you can check the status of the invididual deployments. Azure portal link will be based on azure environment.

## Deploying individual modules

If you prefer you can deploy the constituent modules for MS-VDI individually.
The following is the series of commands to execute.

``` PowerShell
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "VirtualNetworkSPOKE"
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "DiagnosticStorageAccount"
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "EnableServiceEndpointOnDiagnosticStorageAccount"
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "LogAnalytics"
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "KeyVault"
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "ArtifactsStorageAccount"
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "UploadScriptsToArtifactsStorage"
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "JumpboxASG"
        .\Orchestration\OrchestrationService\ModuleConfigurationDeployment.ps1 -DefinitionPath .\Environments\aisULevelup\definition.json -ModuleConfigurationName "WindowsVM"
```

**NOTE:**

1. If deployment reports, unable to find deployment storage account, it could be that PowerShell is not connected to Azure.
2. Open a new PowerShell/Docker instance if there was any changes to files in Environments folder

### **Teardown the environment**

``` PowerShell
./Orchestration/OrchestrationService/ModuleConfigurationDeployment.ps1 -TearDownEnvironment -DefinitionPath ./Environments/aisULevelup/definition.json
```

Note: This is the same command you used to deploy except that you include ` -TearDownEnvironment`.
It uses the same configuration, so if you change the configuration the tear down may not execute as expected.

### **Remove vdc-toolkit-rg**

Teardown removes only the resources deployed from VDC toolkit orchestration but do not actually remove the resource group (vdc-toolkit-rg) and storage accounts created by VDC toolkit deployment.
vdc-toolkit-rg

Use the Azure Cli to remove the resource group and the storage accounts. Find the storage account name from the vdc-toolkit-rg resource group.

``` AzureCli
az account set --subscription [SUBSCRIPTION_ID]

az storage container legal-hold clear --resource-group vdc-toolkit-rg --account-name [STORAGE_ACCOUNT_NAME] --container-name deployments --tags audit

az storage container legal-hold clear --resource-group vdc-toolkit-rg --account-name [STORAGE_ACCOUNT_NAME] --container-name audit --tags audit

az group delete -n vdc-toolkit-rg
```

### **Remove KeyVault**

For safety reasons, the key vault will not be deleted. Instead, it will be set to a _removed_ state. This means that the name is still considered in use. To fully delete the key vault, use:

``` PowerShell
Get-AzKeyVault -InRemovedState | ? { Write-Host "Removing vault: $($_.VaultName)"; Remove-AzKeyVault -InRemovedState -VaultName $_.VaultName -Location $_.Location -Force }
```
