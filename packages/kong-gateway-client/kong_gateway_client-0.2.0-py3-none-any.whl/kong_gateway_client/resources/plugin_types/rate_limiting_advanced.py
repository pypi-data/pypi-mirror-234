from typing import Any, Optional, List, Dict
from kong_gateway_client.resources.plugins import (
    PluginResource,
    KongPlugin,
    KongPluginList,
)


class RateLimitingAdvancedPlugin:
    """Handles operations for the 'rate-limiting-advanced' plugin in the Kong
    Gateway."""

    PLUGIN_NAME = "rate-limiting-advanced"

    def __init__(self, plugin_resource: PluginResource) -> None:
        """Initializes the RateLimitingAdvancedPlugin.

        Args:
            plugin_resource (PluginResource): An instance to manage communication
            with the Kong Gateway.
        """
        self.plugin_resource = plugin_resource

    def create(
        self,
        service_id: Optional[str] = None,
        route_id: Optional[str] = None,
        consumer_id: Optional[str] = None,
        identifier: str = "consumer",
        window_size: List[int] = [],
        window_type: str = "sliding",
        limit: List[int] = [],
        sync_rate: Optional[int] = None,
        namespace: Optional[str] = None,
        strategy: str = "cluster",
        dictionary_name: str = "kong_rate_limiting_counters",
        hide_client_headers: bool = False,
        retry_after_jitter_max: int = 0,
        header_name: Optional[str] = None,
        path: Optional[str] = None,
        redis_config: Optional[Dict[str, Any]] = None,
        enforce_consumer_groups: bool = False,
        consumer_groups: Optional[List[str]] = None,
        enabled: bool = True,
    ) -> KongPlugin:
        """Create a new instance of the 'rate-limiting-advanced' plugin.

        Args:
            ... (various configuration parameters) ...

        Returns:
            KongPlugin: An instance representing the created plugin.
        """
        base_config = {
            "identifier": identifier,
            "window_size": window_size,
            "window_type": window_type,
            "limit": limit,
            "strategy": strategy,
            "dictionary_name": dictionary_name,
            "hide_client_headers": hide_client_headers,
            "retry_after_jitter_max": retry_after_jitter_max,
            "enforce_consumer_groups": enforce_consumer_groups,
        }
        optional_config = {
            "redis": redis_config,
            "namespace": namespace,
            "consumer_groups": consumer_groups,
            "path": path,
            "header_name": header_name,
            "sync_rate": sync_rate or (0 if strategy != "local" else None),
        }
        config = {
            **base_config,
            **{k: v for k, v in optional_config.items() if v is not None},
        }

        base_data = {
            "config": config,
            "enabled": enabled,
        }
        entity_data = {
            "service": {"id": service_id},
            "route": {"id": route_id},
            "consumer": {"id": consumer_id},
        }
        data = {
            **base_data,
            **{k: v for k, v in entity_data.items() if v["id"] is not None},
        }

        return self.plugin_resource.create(self.PLUGIN_NAME, **data)

    def retrieve(self, plugin_id: str) -> KongPlugin:
        """Retrieve a specific 'rate-limiting-advanced' plugin by its ID.

        Args:
            plugin_id (str): ID of the plugin to be retrieved.

        Returns:
            KongPlugin: An instance representing the retrieved plugin.
        """
        return self.plugin_resource.get(plugin_id)

    def update(self, plugin_id: str, **kwargs) -> KongPlugin:
        """Update a specific 'rate-limiting-advanced' plugin by its ID.

        Args:
            plugin_id (str): ID of the plugin to be updated.
            **kwargs: Arbitrary keyword arguments to update the plugin.

        Returns:
            KongPlugin: An instance representing the updated plugin.
        """
        return self.plugin_resource.create_or_update(plugin_id, **kwargs)

    def delete(self, plugin_id: str) -> None:
        """Delete a specific 'rate-limiting-advanced' plugin by its ID.

        Args:
            plugin_id (str): ID of the plugin to be deleted.
        """
        self.plugin_resource.delete(plugin_id)

    def list_for_service(self, service_id: str) -> KongPluginList:
        """List all 'rate-limiting-advanced' plugins associated with a specific service.

        Args:
            service_id (str): ID of the service.

        Returns:
            KongPluginList: A list of plugin instances associated with the service.
        """
        return self.plugin_resource.list_for_service(service_id)

    def list_for_route(self, route_id: str) -> KongPluginList:
        """List all 'rate-limiting-advanced' plugins associated with a specific route.

        Args:
            route_id (str): ID of the route.

        Returns:
            KongPluginList: A list of plugin instances associated with the route.
        """
        return self.plugin_resource.list_for_route(route_id)
