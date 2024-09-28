import unittest
from unittest.mock import patch, MagicMock
import logging
import main  

class TestMain(unittest.TestCase):

    @patch('main.AzureVNetModule')
    @patch('main.AzureVMModule')
    @patch('main.AzureNSGModule')
    @patch('main.AzureSubnetModule')
    @patch('main.AzureVNGModule')
    @patch('main.AzureRouteTableModule')
    @patch('main.AzureScaleSetModule')
    @patch('main.os.getenv')
    def test_main(self, mock_getenv, MockAzureVNetModule, MockAzureVMModule, MockAzureNSGModule, 
                  MockAzureSubnetModule, MockAzureVNGModule, MockAzureRouteTableModule, MockAzureScaleSetModule):
        
        # Mock environment variables
        mock_getenv.return_value = "test-subscription-id"

        # Mock module instances
        mock_vnet_module = MockAzureVNetModule.return_value
        mock_vm_module = MockAzureVMModule.return_value
        mock_nsg_module = MockAzureNSGModule.return_value
        mock_subnet_module = MockAzureSubnetModule.return_value
        mock_vng_module = MockAzureVNGModule.return_value
        mock_route_table_module = MockAzureRouteTableModule.return_value
        mock_scale_set_module = MockAzureScaleSetModule.return_value

        # Mock method returns for successful resource creation
        mock_vnet_module.create_vnet.return_value = None
        mock_subnet_module.create_subnet.return_value = None
        mock_nsg_module.create_nsg.return_value = None
        mock_vng_module.create_virtual_network_gateway.return_value = None
        mock_route_table_module.create_route_table.return_value = None
        mock_scale_set_module.create_scale_set.return_value = None
        mock_vm_module.create_vm.return_value = None

        # Mock the get_provisioning_state to simulate successful provisioning
        mock_vnet_module.get_provisioning_state.return_value = "Succeeded"
        mock_subnet_module.get_provisioning_state.return_value = "Succeeded"
        mock_nsg_module.get_provisioning_state.return_value = "Succeeded"
        mock_vng_module.get_provisioning_state.return_value = "Succeeded"
        mock_route_table_module.get_provisioning_state.return_value = "Succeeded"
        mock_scale_set_module.get_provisioning_state.return_value = "Succeeded"
        mock_vm_module.get_provisioning_state.return_value = "Succeeded"

        # Mock method returns for successful resource deletion
        mock_vm_module.delete_vm.return_value = None
        mock_scale_set_module.delete_scale_set.return_value = None
        mock_subnet_module.delete_subnet.return_value = None
        mock_vnet_module.delete_vnet.return_value = None

        # Mock other module methods
        mock_vng_module.list_virtual_network_gateways.return_value = []
        mock_vng_module.get_virtual_network_gateway_details.return_value = {}
        mock_vng_module.delete_virtual_network_gateway.return_value = None

        # Capture logging output
        with self.assertLogs('main.logger', level='INFO') as log:
            main.main()  # Call the main function to test

            # Check if the correct logs were created
            self.assertIn("Starting the Azure resource creation process", log.output[0])
            self.assertIn("VNet 'test-vnet' created successfully", log.output[1])
            self.assertIn("Subnet 'test-subnet' created successfully", log.output[2])
            self.assertIn("NSG 'test-nsg' created successfully", log.output[3])
            self.assertIn("Virtual Network Gateway 'test-vng' created successfully", log.output[4])
            self.assertIn("Route Table 'test-rt' created successfully", log.output[5])
            self.assertIn("Scale Set 'test-scale-set' created successfully", log.output[6])
            self.assertIn("VM 'test-vm' created successfully", log.output[7])

        # Check if the resources were created in sequence
        mock_vnet_module.create_vnet.assert_called_once_with('resource_group', 'test-vnet', 'switzerlandnorth', '10.0.0.0/16', tags=None)
        mock_subnet_module.create_subnet.assert_called_once_with('resource_group', 'test-vnet', 'test-subnet', '10.0.1.0/24', tags=None)
        mock_nsg_module.create_nsg.assert_called_once_with('resource_group', 'test-nsg', 'switzerlandnorth', tags=None)
        mock_vng_module.create_virtual_network_gateway.assert_called_once_with('resource_group', 'test-vng', 'switzerlandnorth', 'Vpn', 'RouteBased', 'subnet_id', 'public_ip_id', tags=None)
        mock_route_table_module.create_route_table.assert_called_once_with('resource_group', 'test-rt', 'switzerlandnorth', tags=None)
        mock_scale_set_module.create_scale_set.assert_called_once_with('resource_group', 'test-scale-set', 'switzerlandnorth', 'Standard_DS1_v2', 2, 'subnet_id', tags=None)
        mock_vm_module.create_vm.assert_called_once_with('resource_group', 'test-vm', 'switzerlandnorth', 'nic_id', 'Standard_DS1_v2', tags=None)

        # Verify resource deletion only if they were created
        mock_vm_module.delete_vm.assert_called_once_with('resource_group', 'test-vm')
        mock_scale_set_module.delete_scale_set.assert_called_once_with('resource_group', 'test-scale-set')
        mock_subnet_module.delete_subnet.assert_called_once_with('resource_group', 'test-vnet', 'test-subnet')
        mock_vnet_module.delete_vnet.assert_called_once_with('resource_group', 'test-vnet')

    @patch('main.AzureVNetModule')
    @patch('main.AzureVMModule')
    @patch('main.AzureScaleSetModule')
    @patch('main.AzureSubnetModule')
    @patch('main.AzureVNGModule')
    @patch('main.logger')
    def test_cleanup_on_error(self, mock_logger, MockAzureVNGModule, MockAzureSubnetModule, MockAzureScaleSetModule, MockAzureVMModule, MockAzureVNetModule):
        # This test simulates a failure during the resource creation process to verify if cleanup happens properly.
        mock_vnet_module = MockAzureVNetModule.return_value
        mock_vm_module = MockAzureVMModule.return_value
        mock_subnet_module = MockAzureSubnetModule.return_value
        mock_vng_module = MockAzureVNGModule.return_value
        mock_scale_set_module = MockAzureScaleSetModule.return_value

        # Simulate an exception during VM creation
        mock_vm_module.create_vm.side_effect = Exception("VM creation failed")

        # Call the main function
        with self.assertRaises(Exception):
            main.main()

        # Ensure only resources created before the exception are attempted to be deleted
        mock_vm_module.delete_vm.assert_not_called()  # VM wasn't created
        mock_scale_set_module.delete_scale_set.assert_called_once()  # Scale set was created
        mock_subnet_module.delete_subnet.assert_called_once()
        mock_vnet_module.delete_vnet.assert_called_once()

        # Check if logger.error was called
        mock_logger.error.assert_any_call("An error occurred during resource creation or deletion: VM creation failed")

    @patch('main.time.sleep')
    def test_rate_limiting_handling(self, mock_sleep):
        # Set up mocks to simulate rate-limiting
        mock_vnet_module = MagicMock()
        mock_vnet_module.create_vnet.side_effect = [MagicMock(status_code=429), None]
        mock_vnet_module.get_provisioning_state.return_value = "Succeeded"

        # Call the handle_rate_limiting directly
        with patch('main.AzureVNetModule', return_value=mock_vnet_module):
            main.handle_rate_limiting(mock_vnet_module.create_vnet, 'resource_group', 'test-vnet', 'switzerlandnorth', '10.0.0.0/16')

        # Check that sleep was called and the function was retried
        self.assertTrue(mock_sleep.called)
        self.assertEqual(mock_vnet_module.create_vnet.call_count, 2)  # Ensure the function was called twice (once for 429, once for success)

if __name__ == '__main__':
    unittest.main()
