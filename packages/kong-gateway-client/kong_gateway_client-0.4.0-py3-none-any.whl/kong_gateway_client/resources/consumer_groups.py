from typing import Optional, List, Dict, Any
from kong_gateway_client.client import KongClient
from kong_gateway_client.common import ResponseObject
from kong_gateway_client.utils.helpers import validate_id_or_name, validate_name


class KongConsumers:
    def __init__(self, data: ResponseObject):
        """Initialize the KongConsumers object.

        Args:
            data (ResponseObject): A response object containing consumer data.
        """
        self.id: str = data.get("id")
        self.username: Optional[str] = data.get("username")
        self.custom_id: Optional[str] = data.get("custom_id")
        self.tags: Optional[List[str]] = data.get("tags")

    def __repr__(self) -> str:
        """String representation of the KongConsumers object."""
        return (
            f"<KongConsumers(id={self.id}, username={self.username}, "
            f"custom_id={self.custom_id}, tags={self.tags})>"
        )


class KongConsumerGroup:
    def __init__(self, data: ResponseObject):
        """Initialize the KongConsumerGroup object.

        Args:
            data (ResponseObject): A response object containing consumer group data.
        """
        self.id: str = data.get("id")
        self.name: str = data.get("name", "")

    def __repr__(self) -> str:
        """String representation of the KongConsumerGroup object."""
        return f"<KongConsumerGroup(id={self.id}, name={self.name})>"


class KongConsumerConsumerGroups:
    def __init__(self, data: ResponseObject):
        """Initialize the KongConsumerConsumerGroups object.

        Args:
            data (ResponseObject): A response object containing the mapping of
            consumers to consumer groups.
        """
        self.consumer: Dict[str, Any] = data.get("consumer")
        self.consumer_groups: List[KongConsumerGroup] = [
            KongConsumerGroup(consumer_group_data)
            for consumer_group_data in data.get("consumer_groups", [])
        ]

    def __repr__(self) -> str:
        """String representation of the KongConsumerConsumerGroups object."""
        return f"<KongConsumerConsumerGroups(consumer_groups={self.consumer_groups}>"


class KongConsumerGroupConsumers:
    def __init__(self, data: ResponseObject):
        """Initialize the KongConsumerGroupConsumers object.

        Args:
            data (ResponseObject): A response object containing the mapping of
            consumer groups to consumers.
        """
        self.data: ResponseObject = data or ResponseObject({})
        self.consumers: List[KongConsumers] = [
            KongConsumers(consumer_data)
            for consumer_data in self.data.get("consumers", [])
        ]

    def __len__(self) -> int:
        """Return the number of consumers in the consumer group."""
        return len(self.consumers)

    def __repr__(self) -> str:
        """String representation of the KongConsumerGroupConsumers object."""
        return f"<KongConsumerGroupConsumers(consumers={self.consumers})>"


class KongConsumerGroupRateLimit:
    def __init__(self, data: ResponseObject):
        """Initialize the KongConsumerGroupRateLimit object.

        Args:
            data (ResponseObject): A response object containing rate limit data
            for a consumer group.
        """
        self.config: Dict[str, Any] = data.get("config")
        self.group: str = data.get("group")
        self.plugin: str = data.get("plugin")

    def __repr__(self) -> str:
        """String representation of the KongConsumerGroupRateLimit object."""
        return (
            f"<KongConsumerGroupRateLimit(config={self.config}, "
            f"group={self.group}, plugin={self.plugin}>"
        )


class ConsumerGroup:
    """
    Consumer group class to interact with Kong's Consumer group entities.
    """

    ENTITY_PATH = "/consumer_groups"

    def __init__(self, client: KongClient):
        """
        Initializes the consumer group instance with a KongClient.

        Args:
        - client (KongClient): The client to send requests to Kong.
        """
        self.client = client

    @validate_name
    def create(self, name: str) -> KongConsumerGroup:
        """
        Create a new consumer group in Kong.

        Args:
        - name (str): The name of the consumer group.

        Returns:
        - KongConsumerGroup: Response from Kong.
        """
        if not name:
            raise ValueError("name should be provided.")

        data = {"name": name}

        response_data = self.client.request("POST", self.ENTITY_PATH, json=data)
        return KongConsumerGroup(response_data)

    @validate_id_or_name
    def get(self, id_or_name: str) -> KongConsumerGroup:
        """
        Retrieve a consumer group by its ID or name

        Args:
        - id_or_name (str): The ID or name of the consumer group.

        Returns:
        - KongConsumerGroup: Response from Kong.
        """

        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("GET", endpoint)
        return KongConsumerGroup(response_data)

    @validate_id_or_name
    def get_consumers(self, id_or_name: str) -> KongConsumerGroupConsumers:
        """
        Retrieve all consumers for a group by its ID or name

        Args:
        - id_or_name (str): The ID or name of the consumer group.

        Returns:
        - List[KongConsumerGroup]: Response from Kong.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}/consumers"
        response_data = self.client.request("GET", endpoint)
        return KongConsumerGroupConsumers(response_data)

    def add_consumer(
        self,
        group_id_or_name: str,
        consumer_id_or_name: str,
    ) -> KongConsumerGroupConsumers:
        """
        Add A consumer to a group

        Args:
        - group_id_or_name (str): The ID or name of the consumer group.
        - consumer_id_or_name (str): The ID or name of the consumer to add to the group.

        Returns:
        - KongConsumerGroupConsumer: Response from Kong.
        """

        if group_id_or_name and consumer_id_or_name:
            data = {"consumer": consumer_id_or_name}
            endpoint = f"{self.ENTITY_PATH}/{group_id_or_name}/consumers"
            response_data = self.client.request("POST", endpoint, json=data)
            return KongConsumerGroupConsumers(response_data)
        else:
            raise ValueError(
                (
                    "Either the consumer group id or name must be provided as the "
                    "group you want to add consumers to, and either the consumer id "
                    "or the consumer username must be provided as the entity to add "
                    "to the group."
                )
            )

    def get_all(self) -> List[KongConsumerGroup]:
        """
        Retrieve all consumer groups

        Returns:
        - List[KongConsumerGroup]: A list of kong consumers groups.
        """

        response_data = self.client.fetch_all(self.ENTITY_PATH)
        return [KongConsumerGroup(item) for item in response_data]

    @validate_id_or_name
    def put(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongConsumerGroup:
        """
        Update (or potentially create) a consumer group by its ID or name.

        Args:
        - id_or_name (str): The name of the consumer group.
        - **kwargs: Parameters for the consumer group.

        Returns:
        - KongConsumerGroup: The Kong consumer group object.
        """

        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongConsumerGroup(response_data)

    @validate_id_or_name
    def delete(self, id_or_name: str) -> None:
        """
        Delete a consumer group by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the consumer.

        Returns:
        - KongConsumer: Response from Kong.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("DELETE", endpoint)
        return response_data

    def delete_consumer(
        self,
        group_id_or_name: str,
        consumer_id_or_name: str,
    ) -> None:
        """
        Remove a consumer from a consumer group.

        Args:
        - group_id_or_name (str, optional): The ID or name of the group.
        - consumer_id_or_name (str, optional): The ID or name of the consumer.

        Returns:
        -
        """
        if not group_id_or_name and not consumer_id_or_name:
            raise ValueError(
                (
                    "Either the group id or name must be provided and a consumer id "
                    "or name must be provided"
                )
            )

        endpoint = (
            f"{self.ENTITY_PATH}/{group_id_or_name}/consumers/{consumer_id_or_name}"
        )
        response_data = self.client.request("DELETE", endpoint)
        return response_data

    @validate_id_or_name
    def delete_consumers(self, id_or_name: str) -> None:
        """
        Remove all consumers from a consumer group.

        Args:
        - id_or_name (str, optional): The ID or name of the consumer.

        Returns:
        -
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}/consumers"
        response_data = self.client.request("DELETE", endpoint)
        return response_data

    @validate_id_or_name
    def configure_rate_limit(
        self,
        group_id_or_name: str,
        config_limit: List[int],
        config_window_size: List[int],
        config_window_type: Optional[str] = "sliding",
        config_retry_after_jitter_max: Optional[int] = 0,
    ) -> KongConsumerGroupRateLimit:
        """
        Configure rate limiting for a consumer group.

        Args:
        - group_id_or_name (str): The name or UUID of the consumer group to configure.
        - config_limit (List[int]): List of request-per-window limits.
        - config_window_size (List[int]): List of window sizes (in seconds).
        - config_window_type (str, optional): Time window type ("sliding" or "fixed").
                                              Defaults to "sliding".
        - config_retry_after_jitter_max (int, optional): Upper bound of jitter in
                                                         seconds. Defaults to 0.

        Returns:
        - KongConsumerGroupRateLimit: Rate limit configuration for the consumer group.
        """

        data = {
            "config": {
                "limit": config_limit,
                "window_size": config_window_size,
                "window_type": config_window_type,
                "retry_after_jitter_max": config_retry_after_jitter_max,
            }
        }

        endpoint = (
            f"{self.ENTITY_PATH}/{group_id_or_name}"
            "/overrides/plugins/rate-limiting-advanced"
        )
        response_data = self.client.request("PUT", endpoint, json=data)

        return KongConsumerGroupRateLimit(response_data)

    @validate_id_or_name
    def get_consumer_groups_for_consumer(
        self, id_or_name: str
    ) -> KongConsumerConsumerGroups:
        """
        Retrieve a consumers consumer groups by its ID or name

        Args:
        - id_or_name (str): The ID or name of the consumer.

        Returns:
        - KongConsumerGroup: Response from Kong.
        """
        endpoint = f"/consumers/{id_or_name}/consumer_groups"
        response_data = self.client.request("GET", endpoint)
        return KongConsumerConsumerGroups(response_data)

    def add_consumer_group_for_consumer(
        self,
        consumer_id_or_name: str,
        group_id_or_name: str,
    ) -> KongConsumerConsumerGroups:
        """
        Add A consumer group to consumer

        Args:
        - consumer_id_or_name (str): The ID or name of the consumer to add the group to.
        - group_id_or_name (str): The ID or name of the consumer group.

        Returns:
        - KongConsumerConsumerGroups: Response from Kong.
        """

        if group_id_or_name and consumer_id_or_name:
            data = {"group": group_id_or_name}
            endpoint = f"/consumers/{consumer_id_or_name}/consumer_groups"
            response_data = self.client.request("POST", endpoint, json=data)
            return KongConsumerConsumerGroups(response_data)
        else:
            raise ValueError(
                (
                    "Either the consumer group id or name must be provided as the "
                    "group you want to add the consumers to, and either the "
                    "consumer id or the consumer username must be provided as the "
                    "entity to add the group to."
                )
            )

    @validate_id_or_name
    def delete_consumer_groups_for_consumer(self, id_or_name: str) -> None:
        """
        Remove a consumer from all consumer groups.

        Args:
        - id_or_name (str): The ID or name of the consumer.

        Returns:
        -
        """
        endpoint = f"/consumers/{id_or_name}/consumer_groups"
        response_data = self.client.request("DELETE", endpoint)
        return response_data

    def delete_consumer_group_for_consumer(
        self,
        consumer_id_or_name: str,
        group_id_or_name: str,
    ) -> None:
        """
        Remove a consumer from a consumer groups.

        Args:
        - consumer_id_or_name (str, optional): The ID or name of the consumer.
        - group_id_or_name (str, optional): The ID or name of the group.

        Returns:
        -
        """
        if not consumer_id_or_name or not group_id_or_name:
            raise ValueError(
                (
                    "Either the consumer id or name must be provided and a group id "
                    "or name must be provided"
                )
            )

        endpoint = (
            f"/consumers/{consumer_id_or_name}/consumer_groups/" f"{group_id_or_name}"
        )
        response_data = self.client.request("DELETE", endpoint)
        return response_data
