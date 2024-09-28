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
    @patch('main.call_azure_api')
    @patch('main.wait_for_provisioning')
    @patch('main.logger')
    def test_main(self, mock_logger, mock_wait_for_provisioning, mock_call_azure_api,
                   MockAzureScaleSetModule, MockAzureRouteTableModule, 
                   MockAzureVNGModule, MockAzureSubnetModule, 
                   MockAzureNSGModule, MockAzureVMModule, MockAzureVNetModule):
        
        # Mock environment variables
        os.environ['AZURE_SUBSCRIPTION_ID'] = 'test-subscription-id'
        os.environ['AZURE_RESOURCE_GROUP'] = 'test-resource-group'
        os.environ['AZURE_LOCATION'] = 'switzerlandnorth'
        os.environ['AZURE_VNET_NAME'] = 'test-vnet'
        os.environ['AZURE_SUBNET_NAME'] = 'test-subnet'
        os.environ['AZURE_NSG_NAME'] = 'test-nsg'
        os.environ['AZURE_VNG_NAME'] = 'test-vng'
        os.environ['AZURE_RT_NAME'] = 'test-rt'
        os.environ['AZURE_SCALE_SET_NAME'] = 'test-scale-set'
        os.environ['AZURE_VM_NAME'] = 'test-vm'
        
        # Create mock instances
        mock_vnet_module = MockAzureVNetModule.return_value
        mock_vm_module = MockAzureVMModule.return_value
        mock_nsg_module = MockAzureNSGModule.return_value
        mock_subnet_module = MockAzureSubnetModule.return_value
        mock_vng_module = MockAzureVNGModule.return_value
        mock_route_table_module = MockAzureRouteTableModule.return_value
        mock_scale_set_module = MockAzureScaleSetModule.return_value
        
        # Mock the calls to create resources
        mock_call_azure_api.side_effect = lambda func, *args, **kwargs: None
        mock_wait_for_provisioning.return_value = True

        # Call the main function
        main.main()

        # Check if the correct functions were called
        mock_vnet_module.create_vnet.assert_called_once()
        mock_subnet_module.create_subnet.assert_called_once()
        mock_nsg_module.create_nsg.assert_called_once()
        mock_vng_module.create_virtual_network_gateway.assert_called_once()
        mock_route_table_module.create_route_table.assert_called_once()
        mock_scale_set_module.create_scale_set.assert_called_once()
        mock_vm_module.create_vm.assert_called_once()

        # Ensure that logging was done correctly
        mock_logger.info.assert_any_call("Starting the Azure resource creation process")
        mock_logger.info.assert_any_call("VM 'test-vm' deleted successfully")

    @patch('main.AzureVMModule')
    @patch('main.AzureScaleSetModule')
    @patch('main.AzureSubnetModule')
    @patch('main.AzureVNetModule')
    @patch('main.call_azure_api')
    @patch('main.logger')
    def test_cleanup_on_error(self, mock_logger, mock_call_azure_api, 
                               MockAzureVNetModule, MockAzureSubnetModule, 
                               MockAzureScaleSetModule, MockAzureVMModule):
        # Mock environment variables
        os.environ['AZURE_SUBSCRIPTION_ID'] = 'test-subscription-id'
        os.environ['AZURE_RESOURCE_GROUP'] = 'test-resource-group'
        os.environ['AZURE_LOCATION'] = 'switzerlandnorth'
        os.environ['AZURE_VNET_NAME'] = 'test-vnet'
        os.environ['AZURE_SUBNET_NAME'] = 'test-subnet'
        os.environ['AZURE_NSG_NAME'] = 'test-nsg'
        os.environ['AZURE_VNG_NAME'] = 'test-vng'
        os.environ['AZURE_RT_NAME'] = 'test-rt'
        os.environ['AZURE_SCALE_SET_NAME'] = 'test-scale-set'
        os.environ['AZURE_VM_NAME'] = 'test-vm'

        # Create mock instances
        mock_vnet_module = MockAzureVNetModule.return_value
        mock_vm_module = MockAzureVMModule.return_value
        mock_subnet_module = MockAzureSubnetModule.return_value
        mock_scale_set_module = MockAzureScaleSetModule.return_value

        # Simulate an exception during VM creation
        mock_vm_module.create_vm.side_effect = Exception("VM creation failed")

        # Call the main function
        with self.assertRaises(Exception):
            main.main()

        # Ensure that cleanup attempts are made only for successfully created resources
        mock_vm_module.delete_vm.assert_not_called()  # VM wasn't created
        mock_scale_set_module.delete_scale_set.assert_not_called()  # Scale set wasn't created
        mock_subnet_module.delete_subnet.assert_not_called()  # Subnet wasn't created
        mock_vnet_module.delete_vnet.assert_not_called()  # VNet wasn't created

        # Check if logger.error was called
        mock_logger.error.assert_any_call("An error occurred during resource creation or deletion: VM creation failed")

if __name__ == '__main__':
    unittest.main()
    