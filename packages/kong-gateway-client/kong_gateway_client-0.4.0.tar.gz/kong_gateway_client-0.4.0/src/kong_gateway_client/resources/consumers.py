from typing import Any, Dict, List, Optional
from kong_gateway_client.client import KongClient
from kong_gateway_client.common import ResponseObject
from kong_gateway_client.utils.helpers import validate_id_or_name


class ConsumerACL:
    def __init__(self, data: Dict[str, Any]):
        self.group: Optional[str] = data.get("group")
        self.created_at: Optional[int] = data.get("created_at")
        self.id: Optional[str] = data.get("id")
        self.consumer: Optional[Dict[str, str]] = data.get("consumer")

    def __repr__(self) -> str:
        return (
            f"<ConsumerACL(id={self.id}, group={self.group}, "
            f"created_at={self.created_at}, consumer={self.consumer})>"
        )


class KongConsumer:
    def __init__(self, data: ResponseObject):
        self.id: str = data.get("id")
        self.username: Optional[str] = data.get("username")
        self.custom_id: Optional[str] = data.get("custom_id")
        self.tags: Optional[List[str]] = data.get("tags")

    def __repr__(self) -> str:
        return (
            f"<KongConsumer(id={self.id}, username={self.username}, "
            f"custom_id={self.custom_id}, tags={self.tags})>"
        )


class Consumer:
    """
    Consumer class to interact with Kong's Consumer entities.
    """

    ENTITY_PATH = "/consumers"

    def __init__(self, client: KongClient):
        """
        Initializes the consumer instance with a KongClient.

        Args:
        - client (KongClient): The client to send requests to Kong.
        """
        self.client = client

    def create(
        self, username: str, custom_id: str, tags: List[str] = []
    ) -> KongConsumer:
        """
        Create a new consumer in Kong.

        Args:
        - name (str): The name of the consumer.
        - custom_id (str): The custom_id of the consumer.
        - tags (List[str]): A list of tags for the consumer.

        Returns:
        - KongConsumer: Response from Kong.
        """
        if not username and not custom_id:
            raise ValueError(
                "At least one of username or custom_id should be provided."
            )

        data = {"username": username, "custom_id": custom_id, "tags": tags}

        response_data: ResponseObject = self.client.request(
            "POST", self.ENTITY_PATH, json=data
        )
        return KongConsumer(response_data)

    @validate_id_or_name
    def get(self, id_or_name: str) -> KongConsumer:
        """
        Retrieve a consumer by its ID or name

        Args:
        - id_or_name (str): The ID or name of the consumer

        Returns:
        - KongConsumer: Response from Kong.
        """

        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("GET", endpoint)
        return KongConsumer(response_data)

    def get_all(self) -> List[KongConsumer]:
        """
        Retrieve all consumers

        Returns:
        - List[KongConsumer]: A list of kong consumers.
        """

        response_data = self.client.fetch_all(self.ENTITY_PATH)
        return [KongConsumer(item) for item in response_data]

    @validate_id_or_name
    def patch(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongConsumer:
        """
        Partially update a consumer by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the consumer.
        - **kwargs: Other parameters to update.

        Returns:
        - KongConsumer: The Kong consumer object.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PATCH", endpoint, json=kwargs)
        return KongConsumer(response_data)

    @validate_id_or_name
    def put(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongConsumer:
        """
        Update (or potentially create) a consumer by its ID or name.

        Args:
        - id_or_name (str): The ID of the consumer.
        - **kwargs: Parameters for the consumer.

        Returns:
        - KongConsumer: The Kong consumer object.
        """
        if not id_or_name:
            raise ValueError("Either the consumer id or name must be provided.")

        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongConsumer(response_data)

    @validate_id_or_name
    def delete(self, id_or_name: str) -> None:
        """
        Delete a consumer by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the consumer

        Returns:
        -
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("DELETE", endpoint)
        return response_data

    @validate_id_or_name
    def add_key_auth(
        self,
        username_or_id: str,
        key: Optional[str] = None,
        ttl: Optional[int] = None,
        tags: Optional[List[str]] = None,
    ) -> ResponseObject:
        """
        Add key-auth credentials for a consumer.

        Args:
            username_or_id (str): The ID or username of the consumer.
            key (Optional[str]): The unique key to authenticate the client. If
                                 missing, the plugin will generate one.
            ttl (Optional[int]): The number of seconds the key will be valid.
            tags (Optional[List[str]]): List of tags for the key.

        Returns:
            ResponseObject: The response from Kong containing the created key-auth
                            credentials.
        """

        endpoint = f"{self.ENTITY_PATH}/{username_or_id}/key-auth"
        data: Dict[str, Any] = {}

        if key:
            data["key"] = key
        if ttl:
            data["ttl"] = ttl
        if tags:
            data["tags"] = tags

        response_data: ResponseObject = self.client.request("POST", endpoint, json=data)
        return response_data

    @validate_id_or_name
    def get_acls_by_consumer(self, consumer: str) -> List[ConsumerACL]:
        endpoint = f"/consumers/{consumer}/acls"
        response_data = self.client.fetch_all(endpoint)
        return [ConsumerACL(item) for item in response_data]

    @validate_id_or_name
    def get_acl(self, consumer: str, acl_id: str) -> ConsumerACL:
        endpoint = f"/consumers/{consumer}/acls/{acl_id}"
        response_data = self.client.request("GET", endpoint)
        return ConsumerACL(response_data)

    @validate_id_or_name
    def get_consumer_by_acl(self, acl_id: str) -> Dict[str, Any]:
        endpoint = f"/acls/{acl_id}/consumer"
        response_data = self.client.request("GET", endpoint)
        return (
            response_data.data
        )  # Assuming consumer data is the root level of the response

    @validate_id_or_name
    def update_or_insert_acl(
        self, consumer: str, acl_id: str, group: str
    ) -> ConsumerACL:
        endpoint = f"/consumers/{consumer}/acls/{acl_id}"
        response_data = self.client.request("PUT", endpoint, json={"group": group})
        return ConsumerACL(response_data)

    @validate_id_or_name
    def update_acl_group(self, consumer: str, group: str) -> ConsumerACL:
        endpoint = f"/consumers/{consumer}/acls"
        response_data = self.client.request("POST", endpoint, json={"group": group})
        return ConsumerACL(response_data)

    @validate_id_or_name
    def delete_acl(self, consumer: str, identifier: str) -> None:
        # The identifier can be either the ID or the GROUP name
        endpoint = f"/consumers/{consumer}/acls/{identifier}"
        self.client.request("DELETE", endpoint)
