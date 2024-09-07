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

    def list_scale_sets(self, resource_group_name):
        """List all Virtual Machine Scale Sets in a specific resource group."""
        try:
            scale_sets = self.compute_client.virtual_machine_scale_sets.list(resource_group_name)
            scale_set_list = list(scale_sets)
            print(f"Retrieved {len(scale_set_list)} scale sets from resource group '{resource_group_name}'.")
            return scale_set_list
        except Exception as e:
            print(f"Failed to list scale sets in resource group '{resource_group_name}'. Error: {e}")

    def get_scale_set(self, resource_group_name, scale_set_name):
        """Get the details of a specific Virtual Machine Scale Set in Azure."""
        try:
            scale_set = self.compute_client.virtual_machine_scale_sets.get(
                resource_group_name, scale_set_name)
            print(f"Retrieved Scale Set '{scale_set_name}' details successfully.")
            return scale_set
        except Exception as e:
            print(f"Failed to retrieve Scale Set '{scale_set_name}'. Error: {e}")

    def scale_set(self, resource_group_name, scale_set_name, new_capacity):
        """Scale the Virtual Machine Scale Set by adjusting the number of VMs."""
        try:
            scale_set_params = {
                'sku': {
                    'capacity': new_capacity
                }
            }
            scale_poller = self.compute_client.virtual_machine_scale_sets.begin_create_or_update(
                resource_group_name, scale_set_name, scale_set_params)
            scale_poller.result()
            print(f"Scaled Scale Set '{scale_set_name}' to {new_capacity} instances.")
        except Exception as e:
            print(f"Failed to scale Scale Set '{scale_set_name}'. Error: {e}")

    def start_scale_set_vms(self, resource_group_name, scale_set_name, instance_ids):
        """Start specific VMs in the Virtual Machine Scale Set."""
        try:
            start_poller = self.compute_client.virtual_machine_scale_set_vms.begin_start(
                resource_group_name, scale_set_name, instance_ids)
            start_poller.result()
            print(f"Started VMs in Scale Set '{scale_set_name}' with instance IDs: {instance_ids}.")
        except Exception as e:
            print(f"Failed to start VMs in Scale Set '{scale_set_name}'. Error: {e}")

    def stop_scale_set_vms(self, resource_group_name, scale_set_name, instance_ids):
        """Stop specific VMs in the Virtual Machine Scale Set."""
        try:
            stop_poller = self.compute_client.virtual_machine_scale_set_vms.begin_power_off(
                resource_group_name, scale_set_name, instance_ids)
            stop_poller.result()
            print(f"Stopped VMs in Scale Set '{scale_set_name}' with instance IDs: {instance_ids}.")
        except Exception as e:
            print(f"Failed to stop VMs in Scale Set '{scale_set_name}'. Error: {e}")

    def reimage_scale_set_vms(self, resource_group_name, scale_set_name, instance_ids):
        """Reimage specific VMs in the Virtual Machine Scale Set."""
        try:
            reimage_poller = self.compute_client.virtual_machine_scale_set_vms.begin_reimage(
                resource_group_name, scale_set_name, instance_ids)
            reimage_poller.result()
            print(f"Reimaged VMs in Scale Set '{scale_set_name}' with instance IDs: {instance_ids}.")
        except Exception as e:
            print(f"Failed to reimage VMs in Scale Set '{scale_set_name}'. Error: {e}")

    def update_scale_set_tags(self, resource_group_name, scale_set_name, tags):
        """Update the tags associated with a Virtual Machine Scale Set."""
        try:
            scale_set_params = {
                'tags': tags
            }
            tag_poller = self.compute_client.virtual_machine_scale_sets.begin_create_or_update(
                resource_group_name, scale_set_name, scale_set_params)
            tag_poller.result()
            print(f"Updated tags for Scale Set '{scale_set_name}' successfully.")
        except Exception as e:
            print(f"Failed to update tags for Scale Set '{scale_set_name}'. Error: {e}")
