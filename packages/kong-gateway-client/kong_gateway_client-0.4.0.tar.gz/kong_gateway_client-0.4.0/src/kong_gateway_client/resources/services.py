from typing import List, Optional
from kong_gateway_client.client import KongClient
from kong_gateway_client.common import ResponseObject
from kong_gateway_client.utils.helpers import validate_id_or_name, validate_name


class KongService:
    """Represents a Service entity in the Kong Gateway."""

    def __init__(self, data: ResponseObject) -> None:
        """Initializes the KongService object.

        Args:
            data (ResponseObject): The response data containing service details.

        Raises:
            ValueError: If the `id` is not present in the data.
        """
        self.id: str = data.get("id")
        self.name: Optional[str] = data.get("name")
        self.port: Optional[int] = data.get("port")
        self.path: Optional[str] = data.get("path")
        self.host: Optional[str] = data.get("host")
        self.protocol: Optional[str] = data.get("protocol")
        self.tags: Optional[List[str]] = data.get("tags")

        if not self.id:
            raise ValueError("Service ID is not present in the provided data.")

    def __repr__(self) -> str:
        """Provides a string representation of the KongService instance.

        Returns:
            str: A string representation of the KongService.
        """
        return (
            f"<KongService(id={self.id}, name={self.name}, "
            f"host={self.host}, port={self.port}, path={self.path}, "
            f"protocol={self.protocol}, tags={self.tags})>"
        )


class Service:
    """
    Service class to interact with Kong's Service entities.
    """

    ENTITY_PATH = "/services"

    def __init__(self, client: KongClient):
        """
        Initializes the Service instance with a KongClient.

        Args:
        - client (KongClient): The client to send requests to Kong.
        """
        self.client = client

    @validate_name
    def create(self, name: str, url: str) -> KongService:
        """
        Create a new service in Kong.

        Args:
        - name (str): The name of the service.
        - url (str): The service URL.

        Returns:
        - dict: Response from Kong.
        """
        if not name or not url:
            raise ValueError(
                "Both the service name and url should be provided and non-empty."
            )

        data = {"name": name, "url": url}

        response_data = self.client.request("POST", self.ENTITY_PATH, json=data)
        return KongService(response_data)

    @validate_id_or_name
    def get(self, id_or_name: str) -> KongService:
        """
        Retrieve a service by its ID or name

        Args:
        - id_or_name (str, optional): The ID or name of the service.

        Returns:
        - KongService: Response from Kong.
        """

        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("GET", endpoint)
        return KongService(response_data)

    def get_all(self) -> List[KongService]:
        """
        Retrieve all services

        Returns:
        - List[KongService]: A list of kong services.
        """

        response_data = self.client.fetch_all(self.ENTITY_PATH)
        return [KongService(item) for item in response_data]

    @validate_id_or_name
    def patch(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongService:
        """
        Partially update a service by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the service.
        - **kwargs: Other parameters to update.

        Returns:
        - KongService: The Kong service object.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PATCH", endpoint, json=kwargs)
        return KongService(response_data)

    @validate_id_or_name
    def put(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongService:
        """
        Update (or potentially create) a service by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the service.
        - **kwargs: Parameters for the service.

        Returns:
        - KongService: The Kong service object.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongService(response_data)

    @validate_id_or_name
    def delete(self, id_or_name: str) -> KongService:
        """
        Delete a service by its ID or name.

        Args:
        - id_or_name (str, optional): The ID or name of the service.

        Returns:
        - KongService: Response from Kong.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("DELETE", endpoint)
        return response_data
