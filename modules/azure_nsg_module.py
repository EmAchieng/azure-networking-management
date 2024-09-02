from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os

class AzureNSGModule:
    def __init__(self, subscription_id):
        """Initialize the AzureNSGModule with Azure credentials and subscription ID."""
        self.subscription_id = subscription_id
        self.network_client = NetworkManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        )

    def create_nsg(self, resource_group_name, nsg_name, location):
        """Create a new Network Security Group (NSG) in Azure."""
        nsg_params = {
            'location': location
        }
        try:
            nsg_poller = self.network_client.network_security_groups.begin_create_or_update(
                resource_group_name, nsg_name, nsg_params)
            nsg_result = nsg_poller.result()
            print(f"NSG '{nsg_name}' created successfully.")
            return nsg_result
        except Exception as e:
            print(f"Failed to create NSG '{nsg_name}'. Error: {e}")

    def add_nsg_rule(self, resource_group_name, nsg_name, rule_name, priority, direction, access, protocol, source_address_prefix, destination_address_prefix, source_port_range, destination_port_range):
        """Add a security rule to an existing Network Security Group (NSG) in Azure."""
        nsg_rule_params = {
            'protocol': protocol,
            'source_address_prefix': source_address_prefix,
            'destination_address_prefix': destination_address_prefix,
            'access': access,
            'direction': direction,
            'priority': priority,
            'source_port_range': source_port_range,
            'destination_port_range': destination_port_range
        }
        try:
            rule_poller = self.network_client.security_rules.begin_create_or_update(
                resource_group_name, nsg_name, rule_name, nsg_rule_params)
            rule_result = rule_poller.result()
            print(f"NSG rule '{rule_name}' added successfully.")
            return rule_result
        except Exception as e:
            print(f"Failed to add NSG rule '{rule_name}'. Error: {e}")

    def delete_nsg(self, resource_group_name, nsg_name):
        """Delete an existing Network Security Group (NSG) in Azure."""
        try:
            delete_poller = self.network_client.network_security_groups.begin_delete(
                resource_group_name, nsg_name)
            delete_poller.result()
            print(f"NSG '{nsg_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete NSG '{nsg_name}'. Error: {e}")
