import os
import logging
import time
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from requests.exceptions import HTTPError
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

# Retrieve Azure subscription ID and other values from environment variables
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group = os.getenv('AZURE_RESOURCE_GROUP', 'default-resource-group')
location = os.getenv('AZURE_LOCATION', 'switzerlandnorth')
tags = {
    "Environment": os.getenv('AZURE_ENVIRONMENT', 'Development'),
    "Project": os.getenv('AZURE_PROJECT', 'AzureNetwork')
}

# Validate the Azure Subscription ID
if not subscription_id:
    raise ValueError("Error: The environment variable 'AZURE_SUBSCRIPTION_ID' is not set or is empty.")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Retry decorator for transient issues with exponential backoff
@retry(
    stop=stop_after_attempt(5),  # Retry up to 5 attempts
    wait=wait_exponential(multiplier=1, min=4, max=60),  # Exponential backoff from 4s to 60s
    retry=retry_if_exception_type(HTTPError)  # Only retry on HTTP errors
)
def call_azure_api(func, *args, **kwargs):
    """
    Wrapper function for Azure API calls with retry logic.
    """
    response = func(*args, **kwargs)
    response.raise_for_status()  # Raise an exception for 4XX/5XX HTTP errors
    return response

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

def main():
    logger.info("Starting the Azure resource creation process")

    timeout = 300  # Timeout for resource provisioning

    # Create instances of each Azure module class
    vnet_module = AzureVNetModule(subscription_id)
    vm_module = AzureVMModule(subscription_id)
    nsg_module = AzureNSGModule(subscription_id)
    subnet_module = AzureSubnetModule(subscription_id)
    vng_module = AzureVNGModule(subscription_id)
    route_table_module = AzureRouteTableModule(subscription_id)
    scale_set_module = AzureScaleSetModule(subscription_id)

    resources_created = {
        'vnet': False, 'subnet': False, 'nsg': False, 'vng': False, 'route_table': False, 'scale_set': False, 'vm': False
    }

    try:
        # Create VNet
        vnet_name = os.getenv('AZURE_VNET_NAME', 'test-vnet')
        call_azure_api(vnet_module.create_vnet, resource_group, vnet_name, location, "10.0.0.0/16", tags)
        if wait_for_provisioning(vnet_module, resource_group, vnet_name, timeout):
            resources_created['vnet'] = True
        else:
            raise Exception(f"VNet '{vnet_name}' failed to provision")

        # Create Subnet
        subnet_name = os.getenv('AZURE_SUBNET_NAME', 'test-subnet')
        call_azure_api(subnet_module.create_subnet, resource_group, vnet_name, subnet_name, "10.0.1.0/24", tags)
        if wait_for_provisioning(subnet_module, resource_group, subnet_name, timeout):
            resources_created['subnet'] = True
        else:
            raise Exception(f"Subnet '{subnet_name}' failed to provision")

        # Create NSG
        nsg_name = os.getenv('AZURE_NSG_NAME', 'test-nsg')
        call_azure_api(nsg_module.create_nsg, resource_group, nsg_name, location, tags)
        if wait_for_provisioning(nsg_module, resource_group, nsg_name, timeout):
            resources_created['nsg'] = True
        else:
            raise Exception(f"NSG '{nsg_name}' failed to provision")

        # Create Virtual Network Gateway
        vng_name = os.getenv('AZURE_VNG_NAME', 'test-vng')
        call_azure_api(vng_module.create_virtual_network_gateway, resource_group, vng_name, location, "Vpn", "RouteBased", "subnet_id", "public_ip_id", tags)
        if wait_for_provisioning(vng_module, resource_group, vng_name, timeout):
            resources_created['vng'] = True
        else:
            raise Exception(f"Virtual Network Gateway '{vng_name}' failed to provision")

        # Create Route Table
        rt_name = os.getenv('AZURE_RT_NAME', 'test-rt')
        call_azure_api(route_table_module.create_route_table, resource_group, rt_name, location, tags)
        if wait_for_provisioning(route_table_module, resource_group, rt_name, timeout):
            resources_created['route_table'] = True
        else:
            raise Exception(f"Route Table '{rt_name}' failed to provision")

        # Create Scale Set
        scale_set_name = os.getenv('AZURE_SCALE_SET_NAME', 'test-scale-set')
        call_azure_api(scale_set_module.create_scale_set, resource_group, scale_set_name, location, "Standard_DS1_v2", 2, "subnet_id", tags)
        if wait_for_provisioning(scale_set_module, resource_group, scale_set_name, timeout):
            resources_created['scale_set'] = True
        else:
            raise Exception(f"Scale Set '{scale_set_name}' failed to provision")

        # Create VM
        vm_name = os.getenv('AZURE_VM_NAME', 'test-vm')
        call_azure_api(vm_module.create_vm, resource_group, vm_name, location, "nic_id", "Standard_DS1_v2", tags)
        if wait_for_provisioning(vm_module, resource_group, vm_name, timeout):
            resources_created['vm'] = True
        else:
            raise Exception(f"VM '{vm_name}' failed to provision")

    except Exception as e:
        logger.error(f"An error occurred during resource creation or deletion: {e}")
    finally:
        # Cleanup logic here
        if resources_created['vm']:
            try:
                call_azure_api(vm_module.delete_vm, resource_group, vm_name)
                logger.info(f"VM '{vm_name}' deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete VM '{vm_name}': {e}")
        
        if resources_created['scale_set']:
            try:
                call_azure_api(scale_set_module.delete_scale_set, resource_group, scale_set_name)
                logger.info(f"Scale Set '{scale_set_name}' deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete Scale Set '{scale_set_name}': {e}")
        
        if resources_created['subnet']:
            try:
                call_azure_api(subnet_module.delete_subnet, resource_group, vnet_name, subnet_name)
                logger.info(f"Subnet '{subnet_name}' deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete Subnet '{subnet_name}': {e}")
        
        if resources_created['vnet']:
            try:
                call_azure_api(vnet_module.delete_vnet, resource_group, vnet_name)
                logger.info(f"VNet '{vnet_name}' deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete VNet '{vnet_name}': {e}")

if __name__ == "__main__":
    main()
    