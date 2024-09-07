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

    def test_get_nsg(self):
        resource_group_name = 'test_rg'
        nsg_name = 'test_nsg'

        self.nsg_module.get_nsg(resource_group_name, nsg_name)
        self.nsg_module.network_client.network_security_groups.get.assert_called_once_with(resource_group_name, nsg_name)

    def test_list_nsgs(self):
        resource_group_name = 'test_rg'

        self.nsg_module.list_nsgs(resource_group_name)
        self.nsg_module.network_client.network_security_groups.list.assert_called_once_with(resource_group_name)

    def test_list_nsg_rules(self):
        resource_group_name = 'test_rg'
        nsg_name = 'test_nsg'

        self.nsg_module.list_nsg_rules(resource_group_name, nsg_name)
        self.nsg_module.network_client.security_rules.list.assert_called_once_with(resource_group_name, nsg_name)

    def test_delete_nsg_rule(self):
        resource_group_name = 'test_rg'
        nsg_name = 'test_nsg'
        rule_name = 'test_rule'

        self.nsg_module.delete_nsg_rule(resource_group_name, nsg_name, rule_name)
        self.nsg_module.network_client.security_rules.begin_delete.assert_called_once_with(resource_group_name, nsg_name, rule_name)

    def test_update_nsg_tags(self):
        resource_group_name = 'test_rg'
        nsg_name = 'test_nsg'
        tags = {'environment': 'production'}

        self.nsg_module.update_nsg_tags(resource_group_name, nsg_name, tags)
        self.nsg_module.network_client.network_security_groups.begin_create_or_update.assert_called_once()

if __name__ == '__main__':
    unittest.main()
