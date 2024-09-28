import unittest
from modules.azure_vm_module import AzureVMModule
from unittest.mock import MagicMock
from azure.core.exceptions import AzureError

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

        # Mocking the poller result
        mock_poller = MagicMock()
        mock_poller.result.return_value = "VM Created"
        self.vm_module.compute_client.virtual_machines.begin_create_or_update.return_value = mock_poller

        result = self.vm_module.create_vm(resource_group_name, vm_name, location, nic_id, vm_size)
        self.assertEqual(result, "VM Created")  # Verify the result
        self.vm_module.compute_client.virtual_machines.begin_create_or_update.assert_called_once()

    def test_create_vm_timeout(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'
        location = 'switzerlandnorth'
        nic_id = 'test_nic_id'
        vm_size = 'Standard_DS1_v2'

        # Mocking the poller to raise an exception for a timeout
        mock_poller = MagicMock()
        mock_poller.result.side_effect = AzureError("Timeout occurred")
        self.vm_module.compute_client.virtual_machines.begin_create_or_update.return_value = mock_poller

        with self.assertLogs(level='ERROR') as log:
            result = self.vm_module.create_vm(resource_group_name, vm_name, location, nic_id, vm_size)
            self.assertIsNone(result)  # Ensure no result is returned on failure
            self.assertIn("Azure error occurred while creating VM", log.output[0])  # Check for the log message

    def test_delete_vm(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'

        # Mocking the poller result
        mock_poller = MagicMock()
        mock_poller.result.return_value = None
        self.vm_module.compute_client.virtual_machines.begin_delete.return_value = mock_poller

        self.vm_module.delete_vm(resource_group_name, vm_name)
        self.vm_module.compute_client.virtual_machines.begin_delete.assert_called_once()

    def test_delete_vm_timeout(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'

        # Mocking the poller to raise an exception for a timeout
        mock_poller = MagicMock()
        mock_poller.result.side_effect = AzureError("Timeout occurred")
        self.vm_module.compute_client.virtual_machines.begin_delete.return_value = mock_poller

        with self.assertLogs(level='ERROR') as log:
            self.vm_module.delete_vm(resource_group_name, vm_name)
            self.assertIn("Azure error occurred while deleting VM", log.output[0])  # Check for the log message

    def test_stop_vm(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'

        # Mocking the poller result
        mock_poller = MagicMock()
        mock_poller.result.return_value = None
        self.vm_module.compute_client.virtual_machines.begin_power_off.return_value = mock_poller

        self.vm_module.stop_vm(resource_group_name, vm_name)
        self.vm_module.compute_client.virtual_machines.begin_power_off.assert_called_once_with(
            resource_group_name, vm_name
        )

    def test_get_vm_details(self):
        resource_group_name = 'test_rg'
        vm_name = 'test_vm'

        # Mocking the VM details response
        mock_details = {"name": vm_name, "status": "Running"}
        self.vm_module.compute_client.virtual_machines.get.return_value = mock_details

        result = self.vm_module.get_vm_details(resource_group_name, vm_name)
        self.assertEqual(result, mock_details)  # Ensure the correct details are returned
        self.vm_module.compute_client.virtual_machines.get.assert_called_once_with(
            resource_group_name, vm_name
        )

if __name__ == '__main__':
    unittest.main()
