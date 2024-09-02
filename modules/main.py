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

if __name__ == "__main__":
    main()
