from typing import List, Optional, Dict
from kong_gateway_client.client import KongClient
from kong_gateway_client.common import ResponseObject
from kong_gateway_client.utils.helpers import validate_id_or_name, validate_name


class KongRoute:
    """Represents a Route entity in the Kong Gateway."""

    def __init__(self, data: ResponseObject) -> None:
        """Initializes the KongRoute object.

        Args:
            data (ResponseObject): The response data containing route details.

        Raises:
            ValueError: If the `id` is not present in the data.
        """
        self.id: str = data.get("id")
        self.name: Optional[str] = data.get("name")
        self.protocols: List[str] = data.get("protocols", ["http", "https"])
        self.methods: List[str] = data.get("methods", [])
        self.hosts: List[str] = data.get("hosts", [])
        self.paths: List[str] = data.get("paths", [])
        self.headers: Dict[str, List[str]] = data.get("headers", {})
        self.https_redirect_status_code: int = data.get(
            "https_redirect_status_code", 426
        )
        self.regex_priority: int = data.get("regex_priority", 0)
        self.strip_path: bool = data.get("strip_path", True)
        self.path_handling: str = data.get("path_handling", "v0")
        self.preserve_host: bool = data.get("preserve_host", False)
        self.request_buffering: bool = data.get("request_buffering", True)
        self.response_buffering: bool = data.get("response_buffering", True)
        self.snis: List[str] = data.get("snis", [])
        self.sources: List[Dict[str, Optional[str]]] = data.get("sources", [])
        self.destinations: List[Dict[str, Optional[str]]] = data.get("destinations", [])
        self.tags: List[str] = data.get("tags", [])
        self.service: Dict[str, str] = data.get("service", {})

        if not self.id:
            raise ValueError("Route ID is not present in the provided data.")

    def __repr__(self) -> str:
        """Provides a string representation of the KongRoute instance.

        Returns:
            str: A string representation of the KongRoute.
        """
        return (
            f"<KongRoute(id={self.id}, name={self.name}, protocols={self.protocols}, "
            f"methods={self.methods}, hosts={self.hosts}, paths={self.paths}, "
            f"headers={self.headers}, "
            f"https_redirect_status_code={self.https_redirect_status_code}, "
            f"regex_priority={self.regex_priority}, "
            f"strip_path={self.strip_path}, path_handling={self.path_handling}, "
            f"preserve_host={self.preserve_host}, "
            f"request_buffering={self.request_buffering}, "
            f"response_buffering={self.response_buffering}, snis={self.snis}, "
            f"sources={self.sources}, "
            f"destinations={self.destinations}, tags={self.tags}, "
            f"service={self.service})>"
        )


class Route:
    """
    Route class to interact with Kong's Route entities.
    """

    ENTITY_PATH = "/routes"

    def __init__(self, client: KongClient):
        """
        Initializes the Route instance with a KongClient.

        Args:
        - client (KongClient): The client to send requests to Kong.
        """
        self.client = client

    @validate_name
    def create(self, name: str, **kwargs) -> KongRoute:
        """
        Create a new route in Kong.

        Args:
        - name: The name of the route
        - **kwargs: Parameters to define the route.

        Returns:
        - KongRoute: Response from Kong.
        """
        payload = {
            "name": name,
            **kwargs,
        }
        response_data = self.client.request("POST", self.ENTITY_PATH, json=payload)
        return KongRoute(response_data)

    @validate_id_or_name
    def create_for_service(
        self, name: str, service_id_or_name: str, **kwargs
    ) -> KongRoute:
        """Create a new route for a specific service.

        Args:
            service_id_or_name (str): ID or name of the service.
            name (str): Name of the route.
            **kwargs: Additional keyword arguments to configure the route.

        Returns:
            KongRoute: An object representing the created route.
        """
        endpoint = f"/services/{service_id_or_name}/routes"
        data = {"name": name, **kwargs}
        response_data = self.client.request("POST", endpoint, json=data)
        return KongRoute(response_data)

    @validate_id_or_name
    def get(self, id_or_name: str) -> KongRoute:
        """
        Retrieve a route by its ID or name

        Args:
        - id_or_name (str): The ID or name of the route.

        Returns:
        - KongRoute: Response from Kong.
        """

        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("GET", endpoint)
        return KongRoute(response_data)

    def get_all(self) -> List[KongRoute]:
        """
        Retrieve all routes

        Returns:
        - List[KongRoute]: A list of kong routes.
        """

        response_data = self.client.fetch_all(self.ENTITY_PATH)
        return [KongRoute(ResponseObject(item)) for item in response_data]

    @validate_id_or_name
    def patch(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongRoute:
        """
        Partially update a route by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the route.
        - **kwargs: Other parameters to update.

        Returns:
        - KongRoute: The Kong route object.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PATCH", endpoint, json=kwargs)
        return KongRoute(response_data)

    @validate_id_or_name
    def put(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongRoute:
        """
        Update (or potentially create) a route by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the route.
        - **kwargs: Parameters for the route.

        Returns:
        - KongRoute: The Kong route object.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongRoute(response_data)

    @validate_id_or_name
    def delete(self, id_or_name: str):
        """
        Delete a route by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the route.

        Returns:
        - KongRoute: Response from Kong.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("DELETE", endpoint)
        return response_data
