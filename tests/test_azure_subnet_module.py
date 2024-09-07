import unittest
from modules.azure_subnet_module import AzureSubnetModule
from unittest.mock import MagicMock

class TestAzureSubnetModule(unittest.TestCase):
    def setUp(self):
        self.subscription_id = 'test_subscription_id'
        self.subnet_module = AzureSubnetModule(self.subscription_id)
        self.subnet_module.network_client = MagicMock()

    def test_create_subnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'
        subnet_name = 'test_subnet'
        address_prefix = '10.0.1.0/24'

        self.subnet_module.create_subnet(resource_group_name, vnet_name, subnet_name, address_prefix)
        self.subnet_module.network_client.subnets.begin_create_or_update.assert_called_once()

    def test_delete_subnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'
        subnet_name = 'test_subnet'

        self.subnet_module.delete_subnet(resource_group_name, vnet_name, subnet_name)
        self.subnet_module.network_client.subnets.begin_delete.assert_called_once()

    def test_get_subnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'
        subnet_name = 'test_subnet'

        self.subnet_module.get_subnet(resource_group_name, vnet_name, subnet_name)
        self.subnet_module.network_client.subnets.get.assert_called_once_with(
            resource_group_name, vnet_name, subnet_name
        )

    def test_list_subnets(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'

        self.subnet_module.list_subnets(resource_group_name, vnet_name)
        self.subnet_module.network_client.subnets.list.assert_called_once_with(
            resource_group_name, vnet_name
        )

    def test_update_subnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'
        subnet_name = 'test_subnet'
        new_address_prefix = '10.0.2.0/24'

        self.subnet_module.update_subnet(resource_group_name, vnet_name, subnet_name, new_address_prefix)
        self.subnet_module.network_client.subnets.begin_create_or_update.assert_called_once_with(
            resource_group_name, vnet_name, subnet_name, {'address_prefix': new_address_prefix}
        )

if __name__ == '__main__':
    unittest.main()
