from kong_gateway_client.client import KongClient
from kong_gateway_client.common import ResponseObject
from kong_gateway_client.utils.helpers import validate_id_or_name, validate_id
from typing import Optional, List, Dict, Any


class KongPlugin:
    """Represents a plugin object returned from the Kong API."""

    def __init__(self, data: ResponseObject) -> None:
        """Initialize a KongPlugin object.

        Args:
            data (ResponseObject): Data fetched from Kong API for a plugin.
        """
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.created_at: int = data.get("created_at")
        self.route: Optional[Dict[str, Any]] = data.get("route")
        self.service: Optional[Dict[str, Any]] = data.get("service")
        self.consumer: Optional[Dict[str, Any]] = data.get("consumer")
        self.config: Dict[str, Any] = data.get("config")
        self.protocols: List[str] = data.get("protocols")
        self.enabled: bool = data.get("enabled")
        self.tags: List[str] = data.get("tags")

    def __repr__(self) -> str:
        return f"<KongPlugin(id={self.id}, name={self.name}, enabled={self.enabled})>"


class KongPluginList:
    """Represents a list of plugin objects returned from the Kong API."""

    def __init__(self, data: ResponseObject) -> None:
        """Initialize a KongPluginList object.

        Args:
            data (ResponseObject): List of plugin data fetched from Kong API.
        """
        self.data = [KongPlugin(plugin_data) for plugin_data in data.get("data", [])]

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return f"<KongPluginList(data={self.data})>"


class PluginResource:
    """Resource handler for Kong plugins."""

    ENTITY_PATH = "/plugins"

    def __init__(self, client: KongClient) -> None:
        """Initialize the PluginResource object.

        Args:
            client (KongClient): An instance of the KongClient to make requests.
        """
        self.client = client

    def create(self, name: str, **kwargs) -> KongPlugin:
        """Create a new plugin.

        Args:
            name (str): Name of the plugin.
            **kwargs: Additional keyword arguments to configure the plugin.

        Returns:
            KongPlugin: An object representing the created plugin.
        """
        data = {"name": name, **kwargs}
        response_data = self.client.request("POST", self.ENTITY_PATH, json=data)
        return KongPlugin(response_data)

    @validate_id_or_name
    def create_for_route(
        self, route_id_or_name: str, name: str, **kwargs
    ) -> KongPlugin:
        """Create a new plugin for a specific route.

        Args:
            route_id_or_name (str): ID or name of the route.
            name (str): Name of the plugin.
            **kwargs: Additional keyword arguments to configure the plugin.

        Returns:
            KongPlugin: An object representing the created plugin.
        """
        if not route_id_or_name:
            raise ValueError("Either the route id or name must be provided.")
        endpoint = f"/routes/{route_id_or_name}/plugins"
        data = {"name": name, **kwargs}
        response_data = self.client.request("POST", endpoint, json=data)
        return KongPlugin(response_data)

    @validate_id_or_name
    def create_for_service(
        self, service_id_or_name: str, name: str, **kwargs
    ) -> KongPlugin:
        """Create a new plugin for a specific service.

        Args:
            service_id_or_name (str): ID or name of the service.
            name (str): Name of the plugin.
            **kwargs: Additional keyword arguments to configure the plugin.

        Returns:
            KongPlugin: An object representing the created plugin.
        """
        endpoint = f"/services/{service_id_or_name}/plugins"
        data = {"name": name, **kwargs}
        response_data = self.client.request("POST", endpoint, json=data)
        return KongPlugin(response_data)

    @validate_id_or_name
    def create_for_consumer(
        self, consumer_id_or_name: str, name: str, **kwargs
    ) -> KongPlugin:
        """Create a new plugin for a specific consumer.

        Args:
            consumer_id_or_name (str): ID or name of the consumer.
            name (str): Name of the plugin.
            **kwargs: Additional keyword arguments to configure the plugin.

        Returns:
            KongPlugin: An object representing the created plugin.
        """
        endpoint = f"/consumers/{consumer_id_or_name}/plugins"
        data = {"name": name, **kwargs}
        response_data = self.client.request("POST", endpoint, json=data)
        return KongPlugin(response_data)

    def list_all(self) -> KongPluginList:
        """List all plugins available.

        Returns:
            KongPluginList: A list of all available plugins.
        """
        response_data = self.client.request("GET", self.ENTITY_PATH)
        return KongPluginList(response_data)

    @validate_id_or_name
    def list_for_route(self, route_id_or_name: str) -> KongPluginList:
        """List all plugins associated with a specific route.

        Args:
            route_id_or_name (str): ID or name of the route.

        Returns:
            KongPluginList: A list of plugins associated with the route.
        """
        endpoint = f"/routes/{route_id_or_name}/plugins"
        response_data = self.client.request("GET", endpoint)
        return KongPluginList(response_data)

    @validate_id_or_name
    def list_for_service(self, service_id_or_name: str) -> KongPluginList:
        """List all plugins associated with a specific service.

        Args:
            service_id_or_name (str): ID or name of the service.

        Returns:
            KongPluginList: A list of plugins associated with the service.
        """
        endpoint = f"/services/{service_id_or_name}/plugins"
        response_data = self.client.request("GET", endpoint)
        return KongPluginList(response_data)

    @validate_id_or_name
    def list_for_consumer(self, consumer_id_or_name: str) -> KongPluginList:
        """List all plugins associated with a specific consumer.

        Args:
            consumer_id_or_name (str): ID or name of the consumer.

        Returns:
            KongPluginList: A list of plugins associated with the consumer.
        """
        endpoint = f"/consumers/{consumer_id_or_name}/plugins"
        response_data = self.client.request("GET", endpoint)
        return KongPluginList(response_data)

    @validate_id
    def get(self, plugin_id: str) -> KongPlugin:
        """Retrieve details of a specific plugin using its ID.

        Args:
            plugin_id (str): ID of the plugin.

        Returns:
            KongPlugin: An object representing the fetched plugin.
        """
        endpoint = f"{self.ENTITY_PATH}/{plugin_id}"
        response_data = self.client.request("GET", endpoint)
        return KongPlugin(response_data)

    @validate_id_or_name
    def get_for_route(self, route_id_or_name: str, plugin_id: str) -> KongPlugin:
        """Retrieve details of a specific plugin associated with a route using its ID.

        Args:
            route_id_or_name (str): ID or name of the route.
            plugin_id (str): ID of the plugin.

        Returns:
            KongPlugin: An object representing the fetched plugin.
        """
        endpoint = f"/routes/{route_id_or_name}/plugins/{plugin_id}"
        response_data = self.client.request("GET", endpoint)
        return KongPlugin(response_data)

    @validate_id_or_name
    def get_for_service(self, service_id_or_name: str, plugin_id: str) -> KongPlugin:
        """Retrieve details of a specific plugin associated with a service using its ID.

        Args:
            service_id_or_name (str): ID or name of the service.
            plugin_id (str): ID of the plugin.

        Returns:
            KongPlugin: An object representing the fetched plugin.
        """
        endpoint = f"/services/{service_id_or_name}/plugins/{plugin_id}"
        response_data = self.client.request("GET", endpoint)
        return KongPlugin(response_data)

    @validate_id_or_name
    def get_for_consumer(
        self, consumer_id_or_username: str, plugin_id: str
    ) -> KongPlugin:
        """Retrieve details of a specific plugin associated with a consumer using its ID.

        Args:
            consumer_id_or_username (str): ID or username of the consumer.
            plugin_id (str): ID of the plugin.

        Returns:
            KongPlugin: An object representing the fetched plugin.
        """
        endpoint = f"/consumers/{consumer_id_or_username}/plugins/{plugin_id}"
        response_data = self.client.request("GET", endpoint)
        return KongPlugin(response_data)

    @validate_id
    def update(self, plugin_id: str, **kwargs) -> KongPlugin:
        """Update details of a specific plugin using its ID.

        Args:
            plugin_id (str): ID of the plugin.
            **kwargs: Keyword arguments representing fields to update.

        Returns:
            KongPlugin: An object representing the updated plugin.
        """
        endpoint = f"{self.ENTITY_PATH}/{plugin_id}"
        response_data = self.client.request("PATCH", endpoint, json=kwargs)
        return KongPlugin(response_data)

    @validate_id_or_name
    def update_for_route(
        self, route_id_or_name: str, plugin_id: str, **kwargs
    ) -> KongPlugin:
        """Update details of a specific plugin associated with a route.

        Args:
            route_id_or_name (str): ID or name of the route.
            plugin_id (str): ID of the plugin.
            **kwargs: Keyword arguments representing fields to update.

        Returns:
            KongPlugin: An object representing the updated plugin.
        """
        endpoint = f"/routes/{route_id_or_name}/plugins/{plugin_id}"
        response_data = self.client.request("PATCH", endpoint, json=kwargs)
        return KongPlugin(response_data)

    @validate_id_or_name
    def update_for_service(
        self, service_id_or_name: str, plugin_id: str, **kwargs
    ) -> KongPlugin:
        """Update details of a specific plugin associated with a service.

        Args:
            service_id_or_name (str): ID or name of the service.
            plugin_id (str): ID of the plugin.
            **kwargs: Keyword arguments representing fields to update.

        Returns:
            KongPlugin: An object representing the updated plugin.
        """
        endpoint = f"/services/{service_id_or_name}/plugins/{plugin_id}"
        response_data = self.client.request("PATCH", endpoint, json=kwargs)
        return KongPlugin(response_data)

    @validate_id_or_name
    def update_for_consumer(
        self, consumer_id_or_username: str, plugin_id: str, **kwargs
    ) -> KongPlugin:
        """Update details of a specific plugin associated with a consumer.

        Args:
            consumer_id_or_username (str): ID or username of the consumer.
            plugin_id (str): ID of the plugin.
            **kwargs: Keyword arguments representing fields to update.

        Returns:
            KongPlugin: An object representing the updated plugin.
        """
        endpoint = f"/consumers/{consumer_id_or_username}/plugins/{plugin_id}"
        response_data = self.client.request("PATCH", endpoint, json=kwargs)
        return KongPlugin(response_data)

    @validate_id
    def create_or_update(self, plugin_id: str, **kwargs) -> KongPlugin:
        """Create or update a plugin based on its ID.

        If the plugin doesn't exist, it's created. If it does, it's updated.

        Args:
            plugin_id (str): ID of the plugin.
            **kwargs: Keyword arguments representing fields to create or update.

        Returns:
            KongPlugin: An object representing the created or updated plugin.
        """
        endpoint = f"{self.ENTITY_PATH}/{plugin_id}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongPlugin(response_data)

    @validate_id_or_name
    def create_or_update_for_route(
        self, route_id_or_name: str, plugin_id: str, **kwargs
    ) -> KongPlugin:
        """Create or update a plugin associated with a route based on its ID.

        If the plugin doesn't exist, it's created. If it does, it's updated.

        Args:
            route_id_or_name (str): ID or name of the route.
            plugin_id (str): ID of the plugin.
            **kwargs: Keyword arguments representing fields to create or update.

        Returns:
            KongPlugin: An object representing the created or updated plugin.
        """
        endpoint = f"/routes/{route_id_or_name}/plugins/{plugin_id}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongPlugin(response_data)

    @validate_id_or_name
    def create_or_update_for_service(
        self, service_id_or_name: str, plugin_id: str, **kwargs
    ) -> KongPlugin:
        """Create or update a plugin associated with a service based on its ID.

        If the plugin doesn't exist, it's created. If it does, it's updated.

        Args:
            service_id_or_name (str): ID or name of the service.
            plugin_id (str): ID of the plugin.
            **kwargs: Keyword arguments representing fields to create or update.

        Returns:
            KongPlugin: An object representing the created or updated plugin.
        """
        endpoint = f"/services/{service_id_or_name}/plugins/{plugin_id}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongPlugin(response_data)

    @validate_id_or_name
    def create_or_update_for_consumer(
        self, consumer_id_or_username: str, plugin_id: str, **kwargs
    ) -> KongPlugin:
        """Create or update a plugin associated with a consumer based on its ID.

        If the plugin doesn't exist, it's created. If it does, it's updated.

        Args:
            consumer_id_or_username (str): ID or username of the consumer.
            plugin_id (str): ID of the plugin.
            **kwargs: Keyword arguments representing fields to create or update.

        Returns:
            KongPlugin: An object representing the created or updated plugin.
        """
        endpoint = f"/consumers/{consumer_id_or_username}/plugins/{plugin_id}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongPlugin(response_data)

    @validate_id
    def delete(self, plugin_id: str) -> None:
        """Delete a specific plugin using its ID.

        Args:
            plugin_id (str): ID of the plugin.
        """
        endpoint = f"{self.ENTITY_PATH}/{plugin_id}"
        self.client.request("DELETE", endpoint)

    @validate_id_or_name
    def delete_for_route(self, route_id_or_name: str, plugin_id: str) -> None:
        """Delete a specific plugin associated with a route using its ID.

        Args:
            route_id_or_name (str): ID or name of the route.
            plugin_id (str): ID of the plugin.
        """
        endpoint = f"/routes/{route_id_or_name}/plugins/{plugin_id}"
        self.client.request("DELETE", endpoint)

    @validate_id_or_name
    def delete_for_service(self, service_id_or_name: str, plugin_id: str) -> None:
        """Delete a specific plugin associated with a service using its ID.

        Args:
            service_id_or_name (str): ID or name of the service.
            plugin_id (str): ID of the plugin.
        """
        endpoint = f"/services/{service_id_or_name}/plugins/{plugin_id}"
        self.client.request("DELETE", endpoint)

    @validate_id_or_name
    def delete_for_consumer(self, consumer_id_or_username: str, plugin_id: str) -> None:
        """Delete a specific plugin associated with a consumer using its ID.

        Args:
            consumer_id_or_username (str): ID or username of the consumer.
            plugin_id (str): ID of the plugin.
        """
        endpoint = f"/consumers/{consumer_id_or_username}/plugins/{plugin_id}"
        self.client.request("DELETE", endpoint)
