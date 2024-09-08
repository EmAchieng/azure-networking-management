import os
import logging
from dotenv import load_dotenv

from modules.azure_vnet_module import AzureVNetModule
from modules.azure_vm_module import AzureVMModule
from modules.azure_nsg_module import AzureNSGModule
from modules.azure_subnet_module import AzureSubnetModule
from modules.azure_vng_module import AzureVNGModule
from modules.azure_route_table_module import AzureRouteTableModule
from modules.azure_scale_set_module import AzureScaleSetModule


# Load environment variables from the .env file
load_dotenv()

# Retrieve Azure subscription ID from environment variables
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
     # Log the start of the operation
    logger.info("Starting the Azure resource creation process")

    # Create instances of each Azure module class
    vnet_module = AzureVNetModule(subscription_id)
    vm_module = AzureVMModule(subscription_id)
    nsg_module = AzureNSGModule(subscription_id)
    subnet_module = AzureSubnetModule(subscription_id)
    vng_module = AzureVNGModule(subscription_id)
    route_table_module = AzureRouteTableModule(subscription_id)
    scale_set_module = AzureScaleSetModule(subscription_id)

    # Define resources
    resource_group = "resource_group"
    location = "switzerlandnorth"

    try:
        # Create VNet
        vnet_name = "test-vnet"
        vnet_module.create_vnet(resource_group, vnet_name, location, "10.0.0.0/16")
        logger.info(f"VNet '{vnet_name}' created successfully")

        # Create Subnet
        subnet_name = "test-subnet"
        subnet_module.create_subnet(resource_group, vnet_name, subnet_name, "10.0.1.0/24")
        logger.info(f"Subnet '{subnet_name}' created successfully")

        # Create NSG
        nsg_name = "test-nsg"
        nsg_module.create_nsg(resource_group, nsg_name, location)
        logger.info(f"NSG '{nsg_name}' created successfully")

        # Create Virtual Network Gateway
        vng_name = "test-vng"
        vng_module.create_virtual_network_gateway(
            resource_group, vng_name, location, "Vpn", "RouteBased", 
            "subnet_id", "public_ip_id"
        )
        logger.info(f"Virtual Network Gateway '{vng_name}' created successfully")

        # Create Route Table
        rt_name = "test-rt"
        route_table_module.create_route_table(resource_group, rt_name, location)
        logger.info(f"Route Table '{rt_name}' created successfully")

        # Create Scale Set
        scale_set_name = "test-scale-set"
        scale_set_module.create_scale_set(
            resource_group, scale_set_name, location, "Standard_DS1_v2", 2, "subnet_id"
        )
        logger.info(f"Scale Set '{scale_set_name}' created successfully")

        # Create VM
        vm_name = "test-vm"
        vm_module.create_vm(
            resource_group, vm_name, location, "nic_id", "Standard_DS1_v2"
        )
        logger.info(f"VM '{vm_name}' created successfully")

        # List of all virtual network gateways
        vng_gateways = vng_module.list_virtual_network_gateways(resource_group)
        logger.info(f"List of VNGs: {vng_gateways}")

        # Get details of a specific virtual network gateway
        vng_details = vng_module.get_virtual_network_gateway_details(resource_group, vng_name)
        logger.info(f"VNG Details: {vng_details}")

        # Delete the virtual network gateway
        vng_module.delete_virtual_network_gateway(resource_group, vng_name)
        logger.info(f"Virtual Network Gateway '{vng_name}' deleted successfully")

    except Exception as e:
        logger.error(f"An error occurred during resource creation or deletion: {e}")
    finally:
        # Cleanup other resources (subnet, VNet, VM, etc.)
        try:
            vm_module.delete_vm(resource_group, vm_name)
            logger.info(f"VM '{vm_name}' deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete VM '{vm_name}': {e}")
        
        try:
            scale_set_module.delete_scale_set(resource_group, scale_set_name)
            logger.info(f"Scale Set '{scale_set_name}' deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete Scale Set '{scale_set_name}': {e}")
        
        try:
            subnet_module.delete_subnet(resource_group, vnet_name, subnet_name)
            logger.info(f"Subnet '{subnet_name}' deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete Subnet '{subnet_name}': {e}")
        
        try:
            vnet_module.delete_vnet(resource_group, vnet_name)
            logger.info(f"VNet '{vnet_name}' deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete VNet '{vnet_name}': {e}")

if __name__ == "__main__":
    main()
