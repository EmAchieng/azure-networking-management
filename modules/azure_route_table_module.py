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
    def get_route_table(self, resource_group_name, route_table_name):
        """Get details of a specific route table in Azure."""
        try:
            route_table = self.network_client.route_tables.get(resource_group_name, route_table_name)
            print(f"Retrieved Route Table '{route_table_name}' details successfully.")
            return route_table
        except Exception as e:
            print(f"Failed to retrieve Route Table '{route_table_name}'. Error: {e}")

    def list_route_tables(self, resource_group_name):
        """List all route tables in a specific resource group."""
        try:
            route_tables = self.network_client.route_tables.list(resource_group_name)
            route_table_list = list(route_tables)
            print(f"Retrieved {len(route_table_list)} route tables from resource group '{resource_group_name}'.")
            return route_table_list
        except Exception as e:
            print(f"Failed to list route tables. Error: {e}")

    def list_routes(self, resource_group_name, route_table_name):
        """List all routes in a specific route table in Azure."""
        try:
            routes = self.network_client.routes.list(resource_group_name, route_table_name)
            route_list = list(routes)
            print(f"Retrieved {len(route_list)} routes from Route Table '{route_table_name}'.")
            return route_list
        except Exception as e:
            print(f"Failed to list routes for Route Table '{route_table_name}'. Error: {e}")

    def delete_route(self, resource_group_name, route_table_name, route_name):
        """Delete a specific route from a route table in Azure."""
        try:
            delete_poller = self.network_client.routes.begin_delete(
                resource_group_name, route_table_name, route_name)
            delete_poller.result()
            print(f"Route '{route_name}' deleted successfully from Route Table '{route_table_name}'.")
        except Exception as e:
            print(f"Failed to delete route '{route_name}' from Route Table '{route_table_name}'. Error: {e}")

    def update_route_table_tags(self, resource_group_name, route_table_name, tags):
        """Update tags for an existing route table in Azure."""
        try:
            route_table_params = {
                'tags': tags
            }
            route_table_poller = self.network_client.route_tables.begin_create_or_update(
                resource_group_name, route_table_name, route_table_params)
            route_table_result = route_table_poller.result()
            print(f"Updated tags for Route Table '{route_table_name}' successfully.")
            return route_table_result
        except Exception as e:
            print(f"Failed to update tags for Route Table '{route_table_name}'. Error: {e}")
            