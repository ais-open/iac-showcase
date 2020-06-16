# Azure Blueprint

### Zero Trust Architecture implementation

Follow the instructions to get the Zero Trust Architecture environment deployed to your azure. While you learn how to leverage Azure Blueprint for orchesting this deployment can also help to learn more about secured architecture.

- [ATO-Toolkit](https://github.com/Azure/ato-toolkit)
- [Zero Trust Blueprint deployment](https://github.com/Azure/ato-toolkit/blob/master/automation/zero-trust-architecture/README.md)

Steps to follow after Blueprint is deployed to Azure subscription:

- Cloning and deploying Blueprint can be done in Azure cloudshell or Azure Powershell. Update the tenant and subscription id's below and run in Azure Powershell
  
  ```Cli
  Connect-AzAccount -Tenant "000000-0000-00000" -SubscriptionId "00-000-00000000" -EnvironmentName AzureCloud
  ```

- [Publish Blueprint](https://docs.microsoft.com/en-us/azure/governance/blueprints/overview#blueprint-publishing)
- [Assign Blueprint](https://docs.microsoft.com/en-us/azure/governance/blueprints/overview#blueprint-assignment)
- Watch the status of blueprint deployment. Any errors will be shown in the blueprint assignment page and are inituitive to identify the error.
- Your blue print deployment is successful when you  see 'Succeeded'
- If it fails, fix the error. Then use 'Update Assignment' to re-run the deployment.
