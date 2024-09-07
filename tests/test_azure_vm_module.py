import unittest
from modules.azure_vm_module import AzureVMModule
from unittest.mock import MagicMock

class TestAzureVMModule(unittest.TestCase):
    def setUp(self):
        self.subscription_id = 'test_subscription_id'
        self.vm_module = AzureVMModule(self.subscription_id)
        self.vm_module.compute_client = MagicMock()

    def test_create_vm(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'
        location = 'switzerlandnorth'
        nic_id = 'test_nic_id'
        vm_size = 'Standard_DS1_v2'

        self.vm_module.create_vm(resource_group_name, vm_name, location, nic_id)
        self.vm_module.compute_client.virtual_machines.begin_create_or_update.assert_called_once()

    def test_delete_vm(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'

        self.vm_module.delete_vm(resource_group_name, vm_name)
        self.vm_module.compute_client.virtual_machines.begin_delete.assert_called_once()

    def test_stop_vm(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'

        self.vm_module.stop_vm(resource_group_name, vm_name)
        self.vm_module.compute_client.virtual_machines.begin_power_off.assert_called_once_with(
            resource_group_name, vm_name
        )

    def test_get_vm_details(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'

        self.vm_module.get_vm_details(resource_group_name, vm_name)
        self.vm_module.compute_client.virtual_machines.get.assert_called_once_with(
            resource_group_name, vm_name
        )

if __name__ == '__main__':
    unittest.main()
