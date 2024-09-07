from modules.azure_vnet_module import AzureVNetModule
from modules.azure_vm_module import AzureVMModule
from modules.azure_nsg_module import AzureNSGModule
from modules.azure_subnet_module import AzureSubnetModule
from modules.azure_vng_module import AzureVNGModule
from modules.azure_route_table_module import AzureRouteTableModule
from modules.azure_scale_set_module import AzureScaleSetModule
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve Azure subscription ID from environment variables
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

def main():
    # Create instances of each Azure module class
    vnet_module = AzureVNetModule(subscription_id)
    vm_module = AzureVMModule(subscription_id)
    nsg_module = AzureNSGModule(subscription_id)
    subnet_module = AzureSubnetModule(subscription_id)
    vng_module = AzureVNGModule(subscription_id)
    route_table_module = AzureRouteTableModule(subscription_id)
    scale_set_module = AzureScaleSetModule(subscription_id)

    # usage of the VNet module
    vnet_module.create_vnet("resource_group", "test-vnet", "switzerlandnorth", "10.0.0.0/16")

    # usage of the Subnet module
    subnet_module.create_subnet("resource_group", "test-vnet", "test-subnet", "10.0.1.0/24")

    # usage of the NSG module 
    nsg_module.create_nsg("resource_group", "test-nsg", "switzerlandnorth")

     # usage of the Virtual Network Gateway module
    vng_module.create_virtual_network_gateway(
        "resource_group", "test-vng", "switzerlandnorth", "Vpn", "RouteBased", 
        "subnet_id", "public_ip_id"
    )

    # usage of the Route Table module 
    route_table_module.create_route_table("resource_group", "test-rt", "switzerlandnorth")

    #  usage of the Scale Set module
    scale_set_module.create_scale_set(
        "resource_group", "test-scale-set", "switzerlandnorth", "Standard_DS1_v2", 2, "subnet_id"
    )

    # usage of the VM module
    vm_module.create_vm(
        "resource_group", "test-vm", "switzerlandnorth", "nic_id", "Standard_DS1_v2"
    )

    # List of all virtual network gateways
    vng_gateways = vng_module.list_virtual_network_gateways("resource_group")
    print(f"List of VNGs: {vng_gateways}")

    # Get details of a specific virtual network gateway
    vng_details = vng_module.get_virtual_network_gateway_details("resource_group", "test-vng")
    print(f"VNG Details: {vng_details}")

    # Delete the virtual network gateway
    vng_module.delete_virtual_network_gateway("resource_group", "test-vng")

    # Cleanup other resources (subnet, VNet, VM, etc.)
    vm_module.delete_vm("resource_group", "test-vm")
    scale_set_module.delete_scale_set("resource_group", "test-scale-set")
    subnet_module.delete_subnet("resource_group", "test-vnet", "test-subnet")
    vnet_module.delete_vnet("resource_group", "test-vnet")

if __name__ == "__main__":
    main()
