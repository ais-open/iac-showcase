#Prerequisities for ARM/PowerShell
#Need Az Module 
#




$resourceGroupName = "DEMO-IaC-RGP"
$location = "EAST US"

New-AzResourceGroup -Name $resourceGroupName -Location $location

#Demo on Testing Validation of Deployment
Test-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
-TemplateFile ./azureRedeploy.json -Verbose 

#Deploy the Template to RGP
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
  -TemplateFile ./azureRedeploy.json -Verbose 

#Discuss Incremental and Complete commands for changing a deployed template
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName 
-TemplateFile ./azureRedeploy.json -Mode Incremental



