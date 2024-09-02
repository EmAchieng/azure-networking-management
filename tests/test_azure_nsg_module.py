import unittest
from modules.azure_nsg_module import AzureNSGModule
from unittest.mock import MagicMock

class TestAzureNSGModule(unittest.TestCase):
    def setUp(self):
        self.subscription_id = 'test_subscription_id'
        self.nsg_module = AzureNSGModule(self.subscription_id)
        self.nsg_module.network_client = MagicMock()

    def test_create_nsg(self):
        resource_group_name = 'test_rg'
        nsg_name = 'test_nsg'
        location = 'switzerlandnorth'

        self.nsg_module.create_nsg(resource_group_name, nsg_name, location)
        self.nsg_module.network_client.network_security_groups.begin_create_or_update.assert_called_once()

    def test_delete_nsg(self):
        resource_group_name = 'test_rg'
        nsg_name = 'test_nsg'

        self.nsg_module.delete_nsg(resource_group_name, nsg_name)
        self.nsg_module.network_client.network_security_groups.begin_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()
