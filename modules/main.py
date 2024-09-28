import os
import logging
import time
import requests
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

def wait_for_provisioning(module, resource_group, resource_name, timeout=300, interval=10):
    """
    Polls the Azure resource to check its provisioning state until it's "Succeeded" or a timeout occurs.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        provisioning_state = module.get_provisioning_state(resource_group, resource_name)
        if provisioning_state == 'Succeeded':
            logger.info(f"{resource_name} is fully provisioned.")
            return True
        elif provisioning_state in ['Failed', 'Canceled']:
            logger.error(f"{resource_name} provisioning failed with state: {provisioning_state}.")
            return False
        logger.info(f"Waiting for {resource_name} to be provisioned... Current state: {provisioning_state}")
        time.sleep(interval)
    logger.error(f"Timeout occurred while waiting for {resource_name} provisioning.")
    return False

def handle_rate_limiting(func, *args, **kwargs):
    """
    A wrapper to handle rate-limiting based on HTTP 429 responses.
    """
    while True:
        response = func(*args, **kwargs)
        if response.status_code == 429:  # Check for rate-limiting
            logger.warning("Rate limit exceeded. Retrying after a short delay...")
            time.sleep(30)  # Wait for 30 seconds before retrying; adjust as necessary
            continue
        return response
        
def main():
     # Log the start of the operation
    logger.info("Starting the Azure resource creation process")

    # Define a timeout (in seconds) for the Azure operations
    timeout = 300  

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

    # Track created resources
    resources_created = {
        'vnet': False,
        'subnet': False,
        'nsg': False,
        'vng': False,
        'route_table': False,
        'scale_set': False,
        'vm': False
    }

    try:
        # Create VNet
        vnet_name = "test-vnet"
        vnet_module.create_vnet(resource_group, vnet_name, location, "10.0.0.0/16")
        if wait_for_provisioning(vnet_module, resource_group, vnet_name, timeout):
            resources_created['vnet'] = True
        else:
            raise Exception(f"VNet '{vnet_name}' failed to provision")

        # Create Subnet
        subnet_name = "test-subnet"
        subnet_module.create_subnet(resource_group, vnet_name, subnet_name, "10.0.1.0/24")
        if wait_for_provisioning(subnet_module, resource_group, subnet_name, timeout):
            resources_created['subnet'] = True
        else:
            raise Exception(f"Subnet '{subnet_name}' failed to provision")

        # Create NSG
        nsg_name = "test-nsg"
        nsg_module.create_nsg(resource_group, nsg_name, location)
        if wait_for_provisioning(nsg_module, resource_group, nsg_name, timeout):
            resources_created['nsg'] = True
        else:
            raise Exception(f"NSG '{nsg_name}' failed to provision")

        # Create Virtual Network Gateway
        vng_name = "test-vng"
        vng_module.create_virtual_network_gateway(
            resource_group, vng_name, location, "Vpn", "RouteBased", 
            "subnet_id", "public_ip_id"
        )
        if wait_for_provisioning(vng_module, resource_group, vng_name, timeout):
            resources_created['vng'] = True
        else:
            raise Exception(f"Virtual Network Gateway '{vng_name}' failed to provision")

        # Create Route Table
        rt_name = "test-rt"
        route_table_module.create_route_table(resource_group, rt_name, location)
        if wait_for_provisioning(route_table_module, resource_group, rt_name, timeout):
            resources_created['route_table'] = True
        else:
            raise Exception(f"Route Table '{rt_name}' failed to provision")

        # Create Scale Set
        scale_set_name = "test-scale-set"
        scale_set_module.create_scale_set(
            resource_group, scale_set_name, location, "Standard_DS1_v2", 2, "subnet_id"
        )
        if wait_for_provisioning(scale_set_module, resource_group, scale_set_name, timeout):
            resources_created['scale_set'] = True
        else:
            raise Exception(f"Scale Set '{scale_set_name}' failed to provision")

        # Create VM
        vm_name = "test-vm"
        vm_module.create_vm(
            resource_group, vm_name, location, "nic_id", "Standard_DS1_v2"
        )
        if wait_for_provisioning(vm_module, resource_group, vm_name, timeout):
            resources_created['vm'] = True
        else:
            raise Exception(f"VM '{vm_name}' failed to provision")

        # List of all virtual network gateways
        vng_gateways = vng_module.list_virtual_network_gateways(resource_group)
        logger.info(f"List of VNGs: {vng_gateways}")

        # Get details of a specific virtual network gateway
        vng_details = vng_module.get_virtual_network_gateway_details(resource_group, vng_name)
        logger.info(f"VNG Details: {vng_details}")

        # Delete the virtual network gateway
        vng_module.delete_virtual_network_gateway(resource_group, vng_name)
        logger.info(f"Virtual Network Gateway '{vng_name}' deleted successfully")
        resources_created['vng'] = False

    except Exception as e:
        logger.error(f"An error occurred during resource creation or deletion: {e}")
    finally:
        # Cleanup other resources (subnet, VNet, VM, etc.)
        if resources_created['vm']:
            try:
                vm_module.delete_vm(resource_group, vm_name)
                logger.info(f"VM '{vm_name}' deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete VM '{vm_name}': {e}")
        
        if resources_created['scale_set']:
            try:
                scale_set_module.delete_scale_set(resource_group, scale_set_name)
                logger.info(f"Scale Set '{scale_set_name}' deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete Scale Set '{scale_set_name}': {e}")
        
        if resources_created['subnet']:
            try:
                subnet_module.delete_subnet(resource_group, vnet_name, subnet_name)
                logger.info(f"Subnet '{subnet_name}' deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete Subnet '{subnet_name}': {e}")
        
        if resources_created['vnet']:
            try:
                vnet_module.delete_vnet(resource_group, vnet_name)
                logger.info(f"VNet '{vnet_name}' deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete VNet '{vnet_name}': {e}")
                
if __name__ == "__main__":
    main()
