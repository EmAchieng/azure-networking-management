from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os

class AzureRouteTableModule:
    def __init__(self, subscription_id):
        """Initialize the AzureRouteTableModule with Azure credentials and subscription ID."""
        self.subscription_id = subscription_id
        self.network_client = NetworkManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription_id
        )

    def create_route_table(self, resource_group_name, route_table_name, location):
        """Create a new route table in Azure."""
        route_table_params = {
            'location': location
        }
        try:
            route_table_poller = self.network_client.route_tables.begin_create_or_update(
                resource_group_name, route_table_name, route_table_params)
            route_table_result = route_table_poller.result()
            print(f"Route Table '{route_table_name}' created successfully.")
            return route_table_result
        except Exception as e:
            print(f"Failed to create Route Table '{route_table_name}'. Error: {e}")

    def add_route(self, resource_group_name, route_table_name, route_name, address_prefix, next_hop_type):
        """Add a route to an existing route table in Azure."""
        route_params = {
            'address_prefix': address_prefix,
            'next_hop_type': next_hop_type
        }
        try:
            route_poller = self.network_client.routes.begin_create_or_update(
                resource_group_name, route_table_name, route_name, route_params)
            route_result = route_poller.result()
            print(f"Route '{route_name}' added successfully.")
            return route_result
        except Exception as e:
            print(f"Failed to add route '{route_name}'. Error: {e}")

    def delete_route_table(self, resource_group_name, route_table_name):
        """Delete an existing route table in Azure."""
        try:
            delete_poller = self.network_client.route_tables.begin_delete(
                resource_group_name, route_table_name)
            delete_poller.result()
            print(f"Route Table '{route_table_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete Route Table '{route_table_name}'. Error: {e}")
