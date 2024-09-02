import unittest
from modules.azure_route_table_module import AzureRouteTableModule
from unittest.mock import MagicMock

class TestAzureRouteTableModule(unittest.TestCase):
    def setUp(self):
        self.subscription_id = 'test_subscription_id'
        self.route_table_module = AzureRouteTableModule(self.subscription_id)
        self.route_table_module.network_client = MagicMock()

    def test_create_route_table(self):
        resource_group_name = 'test_rg'
        route_table_name = 'test_route_table'
        location = 'switzerlandnorth'

        self.route_table_module.create_route_table(resource_group_name, route_table_name, location)
        self.route_table_module.network_client.route_tables.begin_create_or_update.assert_called_once()

    def test_delete_route_table(self):
        resource_group_name = 'test_rg'
        route_table_name = 'test_route_table'

        self.route_table_module.delete_route_table(resource_group_name, route_table_name)
        self.route_table_module.network_client.route_tables.begin_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()
