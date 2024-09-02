import unittest
from modules.azure_vnet_module import AzureVNetModule
from unittest.mock import MagicMock

class TestAzureVNetModule(unittest.TestCase):
    def setUp(self):
        self.subscription_id = 'test_subscription_id'
        self.vnet_module = AzureVNetModule(self.subscription_id)
        self.vnet_module.network_client = MagicMock()

    def test_create_vnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'
        location = 'switzerlandnorth'
        address_prefix = '10.0.0.0/16'

        self.vnet_module.create_vnet(resource_group_name, vnet_name, location, address_prefix)
        self.vnet_module.network_client.virtual_networks.begin_create_or_update.assert_called_once()

    def test_delete_vnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'

        self.vnet_module.delete_vnet(resource_group_name, vnet_name)
        self.vnet_module.network_client.virtual_networks.begin_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()
