from typing import Any, Dict, Optional, List
from kong_gateway_client.resources.plugins import (
    PluginResource,
    KongPlugin,
    KongPluginList,
)


class ACLPlugin:
    """A class to manage the 'acl' plugin in the Kong Gateway."""

    PLUGIN_NAME = "acl"

    def __init__(self, plugin_resource: PluginResource) -> None:
        """Initialize the ACLPlugin class.

        Args:
            plugin_resource (PluginResource): An instance of the PluginResource
            to communicate with the Kong Gateway.
        """
        self.plugin_resource = plugin_resource

    def create(
        self,
        service_id: Optional[str] = None,
        route_id: Optional[str] = None,
        allow: Optional[List[str]] = None,
        deny: Optional[List[str]] = None,
        hide_groups_header: bool = False,
        enabled: bool = True,
    ) -> KongPlugin:
        """Create an ACL plugin instance for a service or route.

        Args:
            service_id (Optional[str]): The ID of the service associated with
                                        the plugin.
            route_id (Optional[str]): The ID of the route associated with the plugin.
            allow (Optional[List[str]]): A list of allowed groups for the ACL.
            deny (Optional[List[str]]): A list of denied groups for the ACL.
            hide_groups_header (bool): Whether to hide the ACL groups header or not.
            enabled (bool): Whether the plugin is enabled or not.

        Raises:
            ValueError: If both 'allow' and 'deny' lists are provided or both are empty.

        Returns:
            KongPlugin: The created ACL plugin instance.
        """
        if bool(allow) == bool(deny):
            raise ValueError("Either allow or deny must be provided, but not both.")

        config: Dict[str, Any] = {
            "hide_groups_header": hide_groups_header,
        }
        data = {"config": config, "enabled": enabled}

        if service_id:
            data["service"] = {"id": service_id}
        elif route_id:
            data["route"] = {"id": route_id}
        if allow:
            config["allow"] = allow
        if deny:
            config["deny"] = deny

        return self.plugin_resource.create(self.PLUGIN_NAME, **data)

    def retrieve(self, plugin_id: str) -> KongPlugin:
        """Retrieve an ACL plugin instance by its ID.

        Args:
            plugin_id (str): The ID of the ACL plugin to retrieve.

        Returns:
            KongPlugin: The retrieved ACL plugin instance.
        """
        return self.plugin_resource.get(plugin_id)

    def update(self, plugin_id: str, **kwargs) -> KongPlugin:
        """Update an ACL plugin instance by its ID.

        Args:
            plugin_id (str): The ID of the ACL plugin to update.

        Returns:
            KongPlugin: The updated ACL plugin instance.
        """
        return self.plugin_resource.create_or_update(plugin_id, **kwargs)

    def delete(self, plugin_id: str) -> None:
        """Delete an ACL plugin instance by its ID.

        Args:
            plugin_id (str): The ID of the ACL plugin to delete.
        """
        self.plugin_resource.delete(plugin_id)

    def list_for_service(self, service_id: str) -> KongPluginList:
        """List all ACL plugin instances for a given service.

        Args:
            service_id (str): The ID of the service to list ACL plugins for.

        Returns:
            KongPluginList: A list of ACL plugin instances for the specified service.
        """
        return self.plugin_resource.list_for_service(service_id)

    def list_for_route(self, route_id: str) -> KongPluginList:
        """List all ACL plugin instances for a given route.

        Args:
            route_id (str): The ID of the route to list ACL plugins for.

        Returns:
            KongPluginList: A list of ACL plugin instances for the specified route.
        """
        return self.plugin_resource.list_for_route(route_id)
