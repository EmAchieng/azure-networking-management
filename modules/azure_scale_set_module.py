from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import os

class AzureScaleSetModule:
    def __init__(self, subscription_id):
        """Initialize the AzureScaleSetModule with Azure credentials and subscription ID."""
        self.subscription_id = subscription_id
        self.compute_client = ComputeManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        )

    def create_scale_set(self, resource_group_name, scale_set_name, location, vm_size, capacity, subnet_id):
        """Create a new Virtual Machine Scale Set in Azure."""
        scale_set_params = {
            'location': location,
            'sku': {
                'tier': 'Standard',
                'capacity': capacity,
                'name': vm_size
            },
            'upgrade_policy': {
                'mode': 'Manual'
            },
            'virtual_machine_profile': {
                'storage_profile': {
                    'image_reference': {
                        'publisher': 'Canonical',
                        'offer': 'UbuntuServer',
                        'sku': '18.04-LTS',
                        'version': 'latest'
                    }
                },
                'os_profile': {
                    'computer_name_prefix': 'autoscalevm',
                    'admin_username': 'azureuser',
                    'admin_password': os.getenv('SCALE_SET_ADMIN_PASSWORD') 
                },
                'network_profile': {
                    'network_interface_configurations': [{
                        'name': scale_set_name + '-nic',
                        'primary': True,
                        'ip_configurations': [{
                            'name': scale_set_name + '-ipconfig',
                            'subnet': {
                                'id': subnet_id
                            }
                        }]
                    }]
                }
            }
        }
        try:
            scale_set_poller = self.compute_client.virtual_machine_scale_sets.begin_create_or_update(
                resource_group_name, scale_set_name, scale_set_params)
            scale_set_result = scale_set_poller.result()
            print(f"Scale Set '{scale_set_name}' created successfully.")
            return scale_set_result
        except Exception as e:
            print(f"Failed to create Scale Set '{scale_set_name}'. Error: {e}")

    def delete_scale_set(self, resource_group_name, scale_set_name):
        """Delete an existing Virtual Machine Scale Set in Azure."""
        try:
            delete_poller = self.compute_client.virtual_machine_scale_sets.begin_delete(
                resource_group_name, scale_set_name)
            delete_poller.result()
            print(f"Scale Set '{scale_set_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete Scale Set '{scale_set_name}'. Error: {e}")
