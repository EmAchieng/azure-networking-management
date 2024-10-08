import unittest
from modules.azure_vng_module import AzureVNGModule
from unittest.mock import MagicMock

class TestAzureVNGModule(unittest.TestCase):
    def setUp(self):
        self.subscription_id = 'test_subscription_id'
        self.vng_module = AzureVNGModule(self.subscription_id)
        self.vng_module.network_client = MagicMock()

    def test_create_virtual_network_gateway(self):
        resource_group_name = 'test_rg'
        vng_name = 'test_vng'
        location = 'switzerlandnorth'
        gateway_type = 'Vpn'
        vpn_type = 'RouteBased'
        subnet_id = 'test_subnet_id'
        public_ip_id = 'test_public_ip_id'

        self.vng_module.create_virtual_network_gateway(resource_group_name, vng_name, location, gateway_type, vpn_type, subnet_id, public_ip_id)
        self.vng_module.network_client.virtual_network_gateways.begin_create_or_update.assert_called_once()

    def test_delete_virtual_network_gateway(self):
        resource_group_name = 'test_rg'
        vng_name = 'test_vng'

        self.vng_module.delete_virtual_network_gateway(resource_group_name, vng_name)
        self.vng_module.network_client.virtual_network_gateways.begin_delete.assert_called_once()

    def test_update_virtual_network_gateway(self):
        resource_group_name = 'test_rg'
        vng_name = 'test_vng'
        gateway_type = 'ExpressRoute'
        vpn_type = 'PolicyBased'

        self.vng_module.update_virtual_network_gateway(
            resource_group_name, vng_name, gateway_type=gateway_type, vpn_type=vpn_type)
        self.vng_module.network_client.virtual_network_gateways.begin_create_or_update.assert_called_once_with(
            resource_group_name, vng_name, {'gateway_type': gateway_type, 'vpn_type': vpn_type}
        )

    def test_list_virtual_network_gateways(self):
        resource_group_name = 'test_rg'

        self.vng_module.list_virtual_network_gateways(resource_group_name)
        self.vng_module.network_client.virtual_network_gateways.list.assert_called_once_with(resource_group_name)

    def test_get_virtual_network_gateway_details(self):
        resource_group_name = 'test_rg'
        vng_name = 'test_vng'

        self.vng_module.get_virtual_network_gateway_details(resource_group_name, vng_name)
        self.vng_module.network_client.virtual_network_gateways.get.assert_called_once_with(
            resource_group_name, vng_name
        )

if __name__ == '__main__':
    unittest.main()
