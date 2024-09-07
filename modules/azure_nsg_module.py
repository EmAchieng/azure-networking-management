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
    def get_nsg(self, resource_group_name, nsg_name):
        """Get details of a specific Network Security Group (NSG)."""
        try:
            nsg = self.network_client.network_security_groups.get(resource_group_name, nsg_name)
            print(f"Retrieved NSG '{nsg_name}' details successfully.")
            return nsg
        except Exception as e:
            print(f"Failed to retrieve NSG '{nsg_name}'. Error: {e}")

    def list_nsgs(self, resource_group_name):
        """List all NSGs in a specific resource group."""
        try:
            nsg_list = self.network_client.network_security_groups.list(resource_group_name)
            nsgs = list(nsg_list)
            print(f"Retrieved {len(nsgs)} NSGs from resource group '{resource_group_name}'.")
            return nsgs
        except Exception as e:
            print(f"Failed to list NSGs. Error: {e}")

    def list_nsg_rules(self, resource_group_name, nsg_name):
        """List all security rules in a specific Network Security Group (NSG)."""
        try:
            rules = self.network_client.security_rules.list(resource_group_name, nsg_name)
            rule_list = list(rules)
            print(f"Retrieved {len(rule_list)} rules from NSG '{nsg_name}'.")
            return rule_list
        except Exception as e:
            print(f"Failed to list rules for NSG '{nsg_name}'. Error: {e}")

    def delete_nsg_rule(self, resource_group_name, nsg_name, rule_name):
        """Delete a specific security rule from a Network Security Group (NSG)."""
        try:
            delete_poller = self.network_client.security_rules.begin_delete(
                resource_group_name, nsg_name, rule_name)
            delete_poller.result()
            print(f"Deleted rule '{rule_name}' from NSG '{nsg_name}' successfully.")
        except Exception as e:
            print(f"Failed to delete rule '{rule_name}' from NSG '{nsg_name}'. Error: {e}")

    def update_nsg_tags(self, resource_group_name, nsg_name, tags):
        """Update tags for an existing Network Security Group (NSG)."""
        try:
            nsg_params = {
                'tags': tags
            }
            nsg_poller = self.network_client.network_security_groups.begin_create_or_update(
                resource_group_name, nsg_name, nsg_params)
            nsg_result = nsg_poller.result()
            print(f"Updated tags for NSG '{nsg_name}' successfully.")
            return nsg_result
        except Exception as e:
            print(f"Failed to update tags for NSG '{nsg_name}'. Error: {e}")
            