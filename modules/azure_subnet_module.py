from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os

class AzureSubnetModule:
    def __init__(self, subscription_id):
        """Initialize the AzureSubnetModule with Azure credentials and subscription ID."""
        self.subscription_id = subscription_id
        self.network_client = NetworkManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        )

    def create_subnet(self, resource_group_name, vnet_name, subnet_name, address_prefix):
        """Create a new subnet in an existing virtual network (VNet) in Azure."""
        subnet_params = {
            'address_prefix': address_prefix
        }
        try:
            subnet_poller = self.network_client.subnets.begin_create_or_update(
                resource_group_name, vnet_name, subnet_name, subnet_params)
            subnet_result = subnet_poller.result()
            print(f"Subnet '{subnet_name}' created successfully.")
            return subnet_result
        except Exception as e:
            print(f"Failed to create subnet '{subnet_name}'. Error: {e}")

    def delete_subnet(self, resource_group_name, vnet_name, subnet_name):
        """Delete an existing subnet in a virtual network (VNet) in Azure."""
        try:
            delete_poller = self.network_client.subnets.begin_delete(
                resource_group_name, vnet_name, subnet_name)
            delete_poller.result()
            print(f"Subnet '{subnet_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete subnet '{subnet_name}'. Error: {e}")

    def get_subnet(self, resource_group_name, vnet_name, subnet_name):
        """Get the details of a specific subnet in a virtual network (VNet) in Azure."""
        try:
            subnet = self.network_client.subnets.get(
                resource_group_name, vnet_name, subnet_name)
            print(f"Details of Subnet '{subnet_name}': {subnet}")
            return subnet
        except Exception as e:
            print(f"Failed to get details for subnet '{subnet_name}'. Error: {e}")

    def list_subnets(self, resource_group_name, vnet_name):
        """List all subnets in a specific virtual network (VNet) in Azure."""
        try:
            subnets = self.network_client.subnets.list(resource_group_name, vnet_name)
            subnets_list = list(subnets)
            print(f"List of subnets in VNet '{vnet_name}': {[subnet.name for subnet in subnets_list]}")
            return subnets_list
        except Exception as e:
            print(f"Failed to list subnets in VNet '{vnet_name}'. Error: {e}")

    def update_subnet(self, resource_group_name, vnet_name, subnet_name, address_prefix):
        """Update an existing subnet's address prefix in a virtual network (VNet) in Azure."""
        subnet_params = {
            'address_prefix': address_prefix
        }
        try:
            subnet_poller = self.network_client.subnets.begin_create_or_update(
                resource_group_name, vnet_name, subnet_name, subnet_params)
            subnet_result = subnet_poller.result()
            print(f"Subnet '{subnet_name}' updated successfully.")
            return subnet_result
        except Exception as e:
            print(f"Failed to update subnet '{subnet_name}'. Error: {e}")
            