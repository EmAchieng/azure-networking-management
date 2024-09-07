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

    def test_list_scale_sets(self):
        resource_group_name = 'test_rg'

        self.scale_set_module.list_scale_sets(resource_group_name)
        self.scale_set_module.compute_client.virtual_machine_scale_sets.list.assert_called_once_with(resource_group_name)

    def test_get_scale_set(self):
        resource_group_name = 'test_rg'
        scale_set_name = 'test_scale_set'

        self.scale_set_module.get_scale_set(resource_group_name, scale_set_name)
        self.scale_set_module.compute_client.virtual_machine_scale_sets.get.assert_called_once_with(resource_group_name, scale_set_name)

    def test_scale_set(self):
        resource_group_name = 'test_rg'
        scale_set_name = 'test_scale_set'
        new_capacity = 5

        self.scale_set_module.scale_set(resource_group_name, scale_set_name, new_capacity)
        self.scale_set_module.compute_client.virtual_machine_scale_sets.begin_create_or_update.assert_called_once()

    def test_start_scale_set_vms(self):
        resource_group_name = 'test_rg'
        scale_set_name = 'test_scale_set'
        instance_ids = ['instance_1', 'instance_2']

        self.scale_set_module.start_scale_set_vms(resource_group_name, scale_set_name, instance_ids)
        self.scale_set_module.compute_client.virtual_machine_scale_set_vms.begin_start.assert_called_once_with(
            resource_group_name, scale_set_name, instance_ids
        )

    def test_stop_scale_set_vms(self):
        resource_group_name = 'test_rg'
        scale_set_name = 'test_scale_set'
        instance_ids = ['instance_1', 'instance_2']

        self.scale_set_module.stop_scale_set_vms(resource_group_name, scale_set_name, instance_ids)
        self.scale_set_module.compute_client.virtual_machine_scale_set_vms.begin_power_off.assert_called_once_with(
            resource_group_name, scale_set_name, instance_ids
        )

    def test_reimage_scale_set_vms(self):
        resource_group_name = 'test_rg'
        scale_set_name = 'test_scale_set'
        instance_ids = ['instance_1', 'instance_2']

        self.scale_set_module.reimage_scale_set_vms(resource_group_name, scale_set_name, instance_ids)
        self.scale_set_module.compute_client.virtual_machine_scale_set_vms.begin_reimage.assert_called_once_with(
            resource_group_name, scale_set_name, instance_ids
        )

    def test_update_scale_set_tags(self):
        resource_group_name = 'test_rg'
        scale_set_name = 'test_scale_set'
        tags = {'env': 'test', 'department': 'IT'}

        self.scale_set_module.update_scale_set_tags(resource_group_name, scale_set_name, tags)
        self.scale_set_module.compute_client.virtual_machine_scale_sets.begin_create_or_update.assert_called_once()
        
if __name__ == '__main__':
    unittest.main()
