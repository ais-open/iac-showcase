"""An Azure Python Pulumi program"""

import pulumi
from pulumi_azure import compute, core, network

config = pulumi.Config("pulumi-demo")
password = config.require("password")

# Create an Azure Resource Group
resource_group = core.ResourceGroup('pulumi_group')

# Create network, subnet and NIC
vnet = network.VirtualNetwork('network', 
                                 address_spaces=['10.1.0.0/16'],
                                 location=resource_group.location,
                                 name='pulumi-network',
                                 resource_group_name=resource_group.name,
                                 subnets=[{
                                    "name": "default",
                                    "address_prefix": "10.1.1.0/24",
                                 }])

subnet = network.Subnet(
    "server-subnet",
    resource_group_name=resource_group.name,
    virtual_network_name=vnet.name,
    address_prefixes=['10.1.2.0/24'],
    name='pulumi-subnet')

nic = network.NetworkInterface('nic',
                               ip_configurations=[{
                                    'name': 'pulumi-ipconf',
                                    'subnet_id': subnet.id,
                                    'private_ip_address_allocation': 'Dynamic'
                               }],
                               location=resource_group.location,
                               name='pulumi-nic',
                               resource_group_name=resource_group.name)

# Create instance
instance = compute.VirtualMachine(
    'machine',
    location=resource_group.location,
    name='pulumi-machine',
    network_interface_ids=[nic.id],
    os_profile={
        "computer_name": "pulumi-machine",
        "admin_username": "adminuser",
        "admin_password": password
    },
    os_profile_windows_config={
    },
    resource_group_name=resource_group.name, 
    storage_image_reference={
        "publisher": "MicrosoftWindowsServer",
        "offer": "WindowsServer",
        "sku": "2016-Datacenter",
        "version": "latest"
    },
    storage_os_disk={
        "create_option": "FromImage",
        "caching": "ReadWrite",
        "managed_disk_type": 'Standard_LRS',
        "name": "pulumi_os_disk"
    },
    vm_size='Standard_F2')


# Export the connection string for the storage account
pulumi.export('private_ip', nic.private_ip_address)
