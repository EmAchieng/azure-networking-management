from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import os

class AzureVMModule:
    def __init__(self, subscription_id):
        """Initialize the AzureVMModule with Azure credentials and subscription ID."""
        self.subscription_id = subscription_id
        self.compute_client = ComputeManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        )

    def create_vm(self, resource_group_name, vm_name, location, nic_id, vm_size='Standard_DS1_v2'):
        """Create a new virtual machine (VM) in Azure."""
        vm_params = {
            'location': location,
            'hardware_profile': {
                'vm_size': vm_size
            },
            'storage_profile': {
                'image_reference': {
                    'publisher': 'Canonical',
                    'offer': 'UbuntuServer',
                    'sku': '18.04-LTS',
                    'version': 'latest'
                }
            },
            'os_profile': {
                'computer_name': vm_name,
                'admin_username': 'azureuser',
                'admin_password': os.getenv('VM_ADMIN_PASSWORD')  
            },
            'network_profile': {
                'network_interfaces': [{
                    'id': nic_id,
                    'primary': True
                }]
            }
        }
        try:
            vm_poller = self.compute_client.virtual_machines.begin_create_or_update(
                resource_group_name, vm_name, vm_params)
            vm_result = vm_poller.result()
            print(f"VM '{vm_name}' created successfully.")
            return vm_result
        except Exception as e:
            print(f"Failed to create VM '{vm_name}'. Error: {e}")

    def delete_vm(self, resource_group_name, vm_name):
        """Delete an existing virtual machine (VM) in Azure."""
        try:
            delete_poller = self.compute_client.virtual_machines.begin_delete(
                resource_group_name, vm_name)
            delete_poller.result()
            print(f"VM '{vm_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete VM '{vm_name}'. Error: {e}")

    def start_vm(self, resource_group_name, vm_name):
        """Start a virtual machine (VM) in Azure."""
        try:
            start_poller = self.compute_client.virtual_machines.begin_start(
                resource_group_name, vm_name)
            start_poller.result()
            print(f"VM '{vm_name}' started successfully.")
        except Exception as e:
            print(f"Failed to start VM '{vm_name}'. Error: {e}")

    def stop_vm(self, resource_group_name, vm_name):
        """Stop a virtual machine (VM) in Azure."""
        try:
            stop_poller = self.compute_client.virtual_machines.begin_power_off(
                resource_group_name, vm_name)
            stop_poller.result()
            print(f"VM '{vm_name}' stopped successfully.")
        except Exception as e:
            print(f"Failed to stop VM '{vm_name}'. Error: {e}")

    def get_vm_details(self, resource_group_name, vm_name):
        """Retrieve details of an existing virtual machine (VM) in Azure."""
        try:
            vm_details = self.compute_client.virtual_machines.get(
                resource_group_name, vm_name)
            print(f"Details of VM '{vm_name}' retrieved successfully.")
            return vm_details
        except Exception as e:
            print(f"Failed to retrieve details for VM '{vm_name}'. Error: {e}")
            