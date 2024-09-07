from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os

class AzureVNGModule:
    def __init__(self, subscription_id):
        """Initialize the AzureVNGModule with Azure credentials and subscription ID."""
        self.subscription_id = subscription_id
        self.network_client = NetworkManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        )

    def create_virtual_network_gateway(self, resource_group_name, vng_name, location, gateway_type, vpn_type, subnet_id, public_ip_id):
        """Create a new Virtual Network Gateway (VNG) in Azure."""
        vng_params = {
            'location': location,
            'gateway_type': gateway_type,
            'vpn_type': vpn_type,
            'ip_configurations': [{
                'name': vng_name + '-ipconfig',
                'subnet': {
                    'id': subnet_id
                },
                'public_ip_address': {
                    'id': public_ip_id
                }
            }]
        }
        try:
            vng_poller = self.network_client.virtual_network_gateways.begin_create_or_update(
                resource_group_name, vng_name, vng_params)
            vng_result = vng_poller.result()
            print(f"Virtual Network Gateway '{vng_name}' created successfully.")
            return vng_result
        except Exception as e:
            print(f"Failed to create Virtual Network Gateway '{vng_name}'. Error: {e}")

    def delete_virtual_network_gateway(self, resource_group_name, vng_name):
        """Delete an existing Virtual Network Gateway (VNG) in Azure."""
        try:
            delete_poller = self.network_client.virtual_network_gateways.begin_delete(
                resource_group_name, vng_name)
            delete_poller.result()
            print(f"Virtual Network Gateway '{vng_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete Virtual Network Gateway '{vng_name}'. Error: {e}")

    def update_virtual_network_gateway(self, resource_group_name, vng_name, gateway_type=None, vpn_type=None):
        """Update an existing Virtual Network Gateway (VNG) in Azure."""
        vng_params = {}
        if gateway_type:
            vng_params['gateway_type'] = gateway_type
        if vpn_type:
            vng_params['vpn_type'] = vpn_type

        try:
            update_poller = self.network_client.virtual_network_gateways.begin_create_or_update(
                resource_group_name, vng_name, vng_params)
            update_result = update_poller.result()
            print(f"Virtual Network Gateway '{vng_name}' updated successfully.")
            return update_result
        except Exception as e:
            print(f"Failed to update Virtual Network Gateway '{vng_name}'. Error: {e}")

    def list_virtual_network_gateways(self, resource_group_name):
        """List all Virtual Network Gateways (VNGs) in a resource group in Azure."""
        try:
            vngs = self.network_client.virtual_network_gateways.list(resource_group_name)
            vng_list = list(vngs)
            print(f"Listed all Virtual Network Gateways in resource group '{resource_group_name}'.")
            return vng_list
        except Exception as e:
            print(f"Failed to list Virtual Network Gateways in resource group '{resource_group_name}'. Error: {e}")

    def get_virtual_network_gateway_details(self, resource_group_name, vng_name):
        """Retrieve details of an existing Virtual Network Gateway (VNG) in Azure."""
        try:
            vng_details = self.network_client.virtual_network_gateways.get(resource_group_name, vng_name)
            print(f"Details of Virtual Network Gateway '{vng_name}' retrieved successfully.")
            return vng_details
        except Exception as e:
            print(f"Failed to retrieve details for Virtual Network Gateway '{vng_name}'. Error: {e}")
            