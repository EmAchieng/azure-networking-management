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
        )

    def create_vnet(self, resource_group_name, vnet_name, location, address_prefix):
        """Create a new virtual network (VNet) in Azure."""
        params = {
            'location': location,
            'address_space': {
                'address_prefixes': [address_prefix]
            }
        }
        try:
            vnet_poller = self.network_client.virtual_networks.begin_create_or_update(
                resource_group_name, vnet_name, params)
            vnet_result = vnet_poller.result()
            print(f"VNet '{vnet_name}' created successfully.")
            return vnet_result
        except Exception as e:
            print(f"Failed to create VNet '{vnet_name}'. Error: {e}")

    def delete_vnet(self, resource_group_name, vnet_name):
        """Delete an existing virtual network (VNet) in Azure."""
        try:
            delete_poller = self.network_client.virtual_networks.begin_delete(
                resource_group_name, vnet_name)
            delete_poller.result()
            print(f"VNet '{vnet_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete VNet '{vnet_name}'. Error: {e}")
