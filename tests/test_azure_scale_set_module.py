import unittest
from modules.azure_scale_set_module import AzureScaleSetModule
from unittest.mock import MagicMock

class TestAzureScaleSetModule(unittest.TestCase):
    def setUp(self):
        self.subscription_id = 'test_subscription_id'
        self.scale_set_module = AzureScaleSetModule(self.subscription_id)
        self.scale_set_module.compute_client = MagicMock()

    def test_create_scale_set(self):
        resource_group_name = 'test_rg'
        scale_set_name = 'test_scale_set'
        location = 'switzerlandnorth'
        vm_size = 'Standard_DS1_v2'
        capacity = 2
        subnet_id = 'test_subnet_id'

        self.scale_set_module.create_scale_set(resource_group_name, scale_set_name, location, vm_size, capacity, subnet_id)
        self.scale_set_module.compute_client.virtual_machine_scale_sets.begin_create_or_update.assert_called_once()

    def test_delete_scale_set(self):
        resource_group_name = 'test_rg'
        scale_set_name = 'test_scale_set'

        self.scale_set_module.delete_scale_set(resource_group_name, scale_set_name)
        self.scale_set_module.compute_client.virtual_machine_scale_sets.begin_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()
