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
