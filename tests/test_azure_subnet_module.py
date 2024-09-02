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

if __name__ == '__main__':
    unittest.main()
