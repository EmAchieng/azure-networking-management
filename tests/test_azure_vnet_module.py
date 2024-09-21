import unittest
from modules.azure_vnet_module import AzureVNetModule
from unittest.mock import MagicMock

class TestAzureVNetModule(unittest.TestCase):
    def setUp(self):
        self.subscription_id = 'test_subscription_id'
        self.vnet_module = AzureVNetModule(self.subscription_id)
        self.vnet_module.network_client = MagicMock()

    @patch('time.sleep', return_value=None)  # Mocking time.sleep to avoid waiting in tests
    def test_create_vnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'
        location = 'switzerlandnorth'
        address_prefix = '10.0.0.0/16'

        poller_mock = MagicMock()
        poller_mock.done.side_effect = [False, False, True]  # Simulating polling behavior
        poller_mock.result.return_value = {'name': vnet_name}
        self.vnet_module.network_client.virtual_networks.begin_create_or_update.return_value = poller_mock

        result = self.vnet_module.create_vnet(resource_group_name, vnet_name, location, address_prefix)

        self.vnet_module.network_client.virtual_networks.begin_create_or_update.assert_called_once_with(
            resource_group_name, vnet_name, {'location': location, 'address_space': {'address_prefixes': [address_prefix]}}
        )
        self.assertEqual(result['name'], vnet_name)

    @patch('time.sleep', return_value=None)
    def test_delete_vnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'

        poller_mock = MagicMock()
        poller_mock.done.side_effect = [False, True]  # Simulating polling for delete operation
        self.vnet_module.network_client.virtual_networks.begin_delete.return_value = poller_mock

        self.vnet_module.delete_vnet(resource_group_name, vnet_name)

        self.vnet_module.network_client.virtual_networks.begin_delete.assert_called_once_with(resource_group_name, vnet_name)

    def test_update_vnet(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'
        address_prefix = '10.0.0.0/16'

        poller_mock = MagicMock()
        poller_mock.done.side_effect = [False, True]
        self.vnet_module.network_client.virtual_networks.begin_create_or_update.return_value = poller_mock

        result = self.vnet_module.update_vnet(resource_group_name, vnet_name, address_prefix)

        self.vnet_module.network_client.virtual_networks.begin_create_or_update.assert_called_once_with(
            resource_group_name, vnet_name, {'address_space': {'address_prefixes': [address_prefix]}}
        )

    def test_list_vnets(self):
        resource_group_name = 'test_rg'

        self.vnet_module.list_vnets(resource_group_name)
        self.vnet_module.network_client.virtual_networks.list.assert_called_once_with(resource_group_name)

    def test_get_vnet_details(self):
        resource_group_name = 'test_rg'
        vnet_name = 'test_vnet'

        self.vnet_module.get_vnet_details(resource_group_name, vnet_name)
        self.vnet_module.network_client.virtual_networks.get.assert_called_once_with(
            resource_group_name, vnet_name
        )
        
if __name__ == '__main__':
    unittest.main()
