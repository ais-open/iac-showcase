#Prerequisities for ARM/PowerShell
#Need Az Module 
Import-Module Az
Install-Module Az -AllowClobber -Force

#Creating ResourceGroup
New-AzResourceGroup -Name $resourceGroupName -Location $location

Remove-AzResourceGroup -ResourceGroupName $resourceGroupName -Verbose

#Demo on Testing Validation of Deployment
Test-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
-TemplateFile ./azuredeploy.json -Verbose 

#Deploy the Template to RGP
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
  -TemplateFile ./azuredeploy.json -Verbose 

#Discuss Incremental and Complete commands for changing a deployed template
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName 
-TemplateFile ./azuredeploy.json -Mode Incremental



