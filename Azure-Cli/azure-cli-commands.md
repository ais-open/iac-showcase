# Azure Cli Commands

```cli
az login
```

## Update for your admin password

```cli
$AdminPassword=[PASSWORD]
```

## Create a resource

```cli
az group create --name myResourceGroup --location usgovarizona
```

## Create a virtual network

```cli
az network vnet create --resource-group myResourceGroup --name myVnet --subnet-name mySubnet
```

## Create a public IP address

```cli
az network public-ip create --resource-group myResourceGroup --name myPublicIP
```

## Create a network security group

```cli
az network nsg create --resource-group myResourceGroup --name myNetworkSecurityGroup
```

## Create a virtual network card and associate with public IP address and NSG

```
az network nic create --resource-group myResourceGroup --name myNic --vnet-name myVnet --subnet mySubnet --network-security-group myNetworkSecurityGroup --public-ip-address myPublicIP
```

## Create a virtual machine

```cli
az vm create --resource-group myResourceGroup --name myVM --location usgovarizona --nics myNic --image win2016datacenter --admin-username azureuser --admin-password $AdminPassword
```

## Open port 3389 to allow RDP traffic to host

```cli
az vm open-port --port 3389 --resource-group myResourceGroup --name myVM
```