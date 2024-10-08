from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os

class AzureVNetModule:
    def __init__(self, subscription_id):
        """Initialize the AzureVNetModule with Azure credentials and subscription ID."""
        self.subscription_id = subscription_id
        self.network_client = NetworkManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        self.timeout = timeout
        )

    def create_vnet(self, resource_group_name, vnet_name, location, address_prefix):
        """Create a new virtual network (VNet) in Azure with timeout handling."""
        params = {
            'location': location,
            'address_space': {
                'address_prefixes': [address_prefix]
            }
        }
        try:
            start_time = time.time()
            vnet_poller = self.network_client.virtual_networks.begin_create_or_update(
                resource_group_name, vnet_name, params)

            while not vnet_poller.done():
                if time.time() - start_time > self.timeout:
                    raise TimeoutError(f"Operation timed out while creating VNet '{vnet_name}'.")
                time.sleep(5)  # Check every 5 seconds

            vnet_result = vnet_poller.result()
            print(f"VNet '{vnet_name}' created successfully.")
            return vnet_result
        except TimeoutError as te:
            print(te)
        except AzureError as e:
            print(f"Failed to create VNet '{vnet_name}'. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while creating VNet '{vnet_name}'. Error: {e}")

    def delete_vnet(self, resource_group_name, vnet_name):
        """Delete an existing virtual network (VNet) in Azure."""
        try:
            start_time = time.time()
            delete_poller = self.network_client.virtual_networks.begin_delete(
                resource_group_name, vnet_name)

            while not delete_poller.done():
                if time.time() - start_time > self.timeout:
                    raise TimeoutError(f"Operation timed out while deleting VNet '{vnet_name}'.")
                time.sleep(5)

            delete_poller.result()
            print(f"VNet '{vnet_name}' deleted successfully.")
        except TimeoutError as te:
            print(te)
        except AzureError as e:
            print(f"Failed to delete VNet '{vnet_name}'. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while deleting VNet '{vnet_name}'. Error: {e}")

    def update_vnet(self, resource_group_name, vnet_name, address_prefix):
        """Update an existing virtual network (VNet) in Azure."""
        params = {
            'address_space': {
                'address_prefixes': [address_prefix]
            }
        }
        try:
            start_time = time.time()
            update_poller = self.network_client.virtual_networks.begin_create_or_update(
                resource_group_name, vnet_name, params)

            while not update_poller.done():
                if time.time() - start_time > self.timeout:
                    raise TimeoutError(f"Operation timed out while updating VNet '{vnet_name}'.")
                time.sleep(5)

            update_result = update_poller.result()
            print(f"VNet '{vnet_name}' updated successfully.")
            return update_result
        except TimeoutError as te:
            print(te)
        except AzureError as e:
            print(f"Failed to update VNet '{vnet_name}'. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while updating VNet '{vnet_name}'. Error: {e}")

    def list_vnets(self, resource_group_name):
        """List all virtual networks (VNets) in a resource group in Azure."""
        try:
            vnets = self.network_client.virtual_networks.list(resource_group_name)
            vnet_list = list(vnets)
            print(f"Listed all VNets in resource group '{resource_group_name}'.")
            return vnet_list
        except AzureError as e:
            print(f"Failed to list VNets in resource group '{resource_group_name}'. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while listing VNets in resource group '{resource_group_name}'. Error: {e}")

    def get_vnet_details(self, resource_group_name, vnet_name):
        """Retrieve details of an existing virtual network (VNet) in Azure."""
        try:
            vnet_details = self.network_client.virtual_networks.get(resource_group_name, vnet_name)
            print(f"Details of VNet '{vnet_name}' retrieved successfully.")
            return vnet_details
        except AzureError as e:
            print(f"Failed to retrieve details for VNet '{vnet_name}'. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while retrieving details for VNet '{vnet_name}'. Error: {e}")
            