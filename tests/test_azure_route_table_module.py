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
    def test_get_route_table(self):
        resource_group_name = 'test_rg'
        route_table_name = 'test_route_table'

        self.route_table_module.get_route_table(resource_group_name, route_table_name)
        self.route_table_module.network_client.route_tables.get.assert_called_once_with(
            resource_group_name, route_table_name
        )

    def test_list_route_tables(self):
        resource_group_name = 'test_rg'

        self.route_table_module.list_route_tables(resource_group_name)
        self.route_table_module.network_client.route_tables.list.assert_called_once_with(resource_group_name)

    def test_list_routes(self):
        resource_group_name = 'test_rg'
        route_table_name = 'test_route_table'

        self.route_table_module.list_routes(resource_group_name, route_table_name)
        self.route_table_module.network_client.routes.list.assert_called_once_with(resource_group_name, route_table_name)

    def test_add_route(self):
        resource_group_name = 'test_rg'
        route_table_name = 'test_route_table'
        route_name = 'test_route'
        address_prefix = '10.0.0.0/16'
        next_hop_type = 'VirtualNetworkGateway'

        self.route_table_module.add_route(resource_group_name, route_table_name, route_name, address_prefix, next_hop_type)
        self.route_table_module.network_client.routes.begin_create_or_update.assert_called_once_with(
            resource_group_name, route_table_name, route_name, {
                'address_prefix': address_prefix,
                'next_hop_type': next_hop_type
            }
        )

    def test_delete_route(self):
        resource_group_name = 'test_rg'
        route_table_name = 'test_route_table'
        route_name = 'test_route'

        self.route_table_module.delete_route(resource_group_name, route_table_name, route_name)
        self.route_table_module.network_client.routes.begin_delete.assert_called_once_with(
            resource_group_name, route_table_name, route_name
        )

    def test_update_route_table_tags(self):
        resource_group_name = 'test_rg'
        route_table_name = 'test_route_table'
        tags = {'environment': 'production'}

        self.route_table_module.update_route_table_tags(resource_group_name, route_table_name, tags)
        self.route_table_module.network_client.route_tables.begin_create_or_update.assert_called_once_with(
            resource_group_name, route_table_name, {'tags': tags}
        )

if __name__ == '__main__':
    unittest.main()
