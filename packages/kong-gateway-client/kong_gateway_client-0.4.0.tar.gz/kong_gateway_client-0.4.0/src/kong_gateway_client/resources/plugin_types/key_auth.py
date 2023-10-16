from typing import Optional, List
from kong_gateway_client.resources.plugins import (
    PluginResource,
    KongPlugin,
    KongPluginList,
)


class KeyAuthPlugin:
    """A class to manage the 'key-auth' plugin in the Kong Gateway."""

    PLUGIN_NAME = "key-auth"

    def __init__(self, plugin_resource: PluginResource) -> None:
        """Initialize the KeyAuthPlugin class.

        Args:
            plugin_resource (PluginResource): An instance of the PluginResource to
                                              communicate with the Kong Gateway.
        """
        self.plugin_resource = plugin_resource

    def create(
        self,
        service_id: Optional[str] = None,
        route_id: Optional[str] = None,
        key_names: List[str] = ["apikey"],
        hide_credentials: bool = False,
        anonymous: Optional[str] = None,
        key_in_header: bool = True,
        key_in_query: bool = True,
        key_in_body: bool = False,
        run_on_preflight: bool = True,
        enabled: bool = True,
    ) -> KongPlugin:
        """Create a key authentication plugin instance for a service or route.

        Args:
            service_id (Optional[str]): The ID of the service associated with
                                        the plugin.
            route_id (Optional[str]): The ID of the route associated with the plugin.
            key_names (List[str]): A list of key names for authentication.
            hide_credentials (bool): Whether to hide the credentials in the request.
            anonymous (Optional[str]): The ID of the anonymous consumer.
            key_in_header (bool): Whether to include the key in the header for
                                  authentication.
            key_in_query (bool): Whether to include the key in the query for
                                 authentication.
            key_in_body (bool): Whether to include the key in the body for
                                authentication.
            run_on_preflight (bool): Whether to run the plugin during the preflight
                                     request.
            enabled (bool): Whether the plugin is enabled or not.

        Returns:
            KongPlugin: The created key authentication plugin instance.
        """
        config = {
            "key_names": key_names,
            "hide_credentials": hide_credentials,
            "anonymous": anonymous,
            "key_in_header": key_in_header,
            "key_in_query": key_in_query,
            "key_in_body": key_in_body,
            "run_on_preflight": run_on_preflight,
        }

        data = {"config": config, "enabled": enabled}

        if service_id:
            data["service"] = {"id": service_id}
        elif route_id:
            data["route"] = {"id": route_id}

        return self.plugin_resource.create(self.PLUGIN_NAME, **data)

    def retrieve(self, plugin_id: str) -> KongPlugin:
        """Retrieve a key authentication plugin instance by its ID.

        Args:
            plugin_id (str): The ID of the key authentication plugin to retrieve.

        Returns:
            KongPlugin: The retrieved key authentication plugin instance.
        """
        return self.plugin_resource.get(plugin_id)

    def update(self, plugin_id: str, **kwargs) -> KongPlugin:
        """Update a key authentication plugin instance by its ID.

        Args:
            plugin_id (str): The ID of the key authentication plugin to update.

        Returns:
            KongPlugin: The updated key authentication plugin instance.
        """
        return self.plugin_resource.create_or_update(plugin_id, **kwargs)

    def delete(self, plugin_id: str) -> None:
        """Delete a key authentication plugin instance by its ID.

        Args:
            plugin_id (str): The ID of the key authentication plugin to delete.
        """
        self.plugin_resource.delete(plugin_id)

    def list_for_service(self, service_id: str) -> KongPluginList:
        """List all key authentication plugin instances for a given service.

        Args:
            service_id (str): The ID of the service to list key authentication
                              plugins for.

        Returns:
            KongPluginList: A list of key authentication plugin instances for the
                            specified service.
        """
        return self.plugin_resource.list_for_service(service_id)

    def list_for_route(self, route_id: str) -> KongPluginList:
        """List all key authentication plugin instances for a given route.

        Args:
            route_id (str): The ID of the route to list key authentication plugins for.

        Returns:
            KongPluginList: A list of key authentication plugin instances for the
                            specified route.
        """
        return self.plugin_resource.list_for_route(route_id)
