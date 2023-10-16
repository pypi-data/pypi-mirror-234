from typing import Dict, Any, List


class ResponseObject:
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a ResponseObject.

        Args:
            data (Dict[str, Any]): The response data to encapsulate.
        """
        self.data = data
        if not self.data:
            self.is_empty = True
            return
        for key, value in self.data.items():
            sanitized_key = self._sanitize_key(key)
            setattr(self, sanitized_key, value)

    def _sanitize_key(self, key: str) -> str:
        """
        Sanitize a given key by replacing spaces and hyphens with underscores.

        Args:
            key (str): The key to sanitize.

        Returns:
            str: The sanitized key.
        """
        sanitized = key.replace(" ", "_").replace("-", "_")
        return sanitized

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve the value of a given key if it exists, otherwise return the
        default value.

        Args:
            key (str): The key whose value needs to be retrieved.
            default (Any, optional): The default value to return if the key is
                                     not found. Defaults to None.

        Returns:
            Any: The value associated with the key or the default.
        """
        sanitized_key = self._sanitize_key(key)
        return getattr(self, sanitized_key, default)

    def __repr__(self) -> str:
        """Represent the ResponseObject as a string."""
        attributes = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"ResponseObject({attributes})"

    def to_list(self) -> List:
        """
        Convert the internal data to a list.

        Returns:
            List: A list containing the internal data.
        """
        if isinstance(self.data, list):
            return self.data
        else:
            return [self.data]
