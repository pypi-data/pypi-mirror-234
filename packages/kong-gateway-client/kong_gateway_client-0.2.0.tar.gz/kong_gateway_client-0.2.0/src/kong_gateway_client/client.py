from typing import Any, Dict, List, Optional
import urllib3
import requests


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
            default (Any, optional): The default value to return if the key is not found. Defaults to None.

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


class KongClient:
    """
    KongClient is a client for communicating with the Kong Admin API.
    """

    def __init__(
        self,
        admin_url: str = "http://localhost:8001",
        admin_token: Optional[str] = None,
        admin_user: str = "kong_admin",
        idp_user: Optional[str] = None,
        idp_pass: Optional[str] = None,
        verify_tls: bool = False,
        workspace: str = "default",
    ) -> None:
        """
        Initialize a KongClient.

        Args:
            admin_url (str, optional): The base URL for the Kong Admin API. Defaults to "http://localhost:8001".
            admin_token (Optional[str], optional): Admin token for authentication.
                                                   Defaults to None.
            admin_user (str, optional): Admin user for authentication. Defaults to
                                       "kong_admin".
            idp_user (Optional[str], optional): IDP user for authentication.
                                                Defaults to None.
            idp_pass (Optional[str], optional): IDP password for authentication.
                                                Defaults to None.
            verify_tls (bool, optional): Whether to verify TLS or not.
                                         Defaults to False.
            workspace (str, optional): The workspace to use. Defaults to "default".
        """
        self.admin_ws_url = f"{admin_url}/{workspace}"
        self.admin_url = admin_url
        self.admin_token = admin_token
        self.admin_user = admin_user
        self.idp_user = idp_user
        self.idp_pass = idp_pass
        self.tls = verify_tls
        self.workspace = workspace
        if not self.tls:
            urllib3.disable_warnings()

        self.session = requests.Session()
        if not admin_token:
            self.configure_auth()
        else:
            self.configure_token()

    def headers(self) -> Dict[str, str]:
        """
        Construct headers based on the authentication method (token or user).

        Returns:
            Dict[str, str]: Headers for the request.
        """
        if self.admin_token:
            return {
                "Accept": "application/json",
                "Kong-Admin-Token": str(self.admin_token),
            }
        else:
            return {
                "Kong-Admin-User": self.admin_user,
            }

    def configure_auth(self) -> None:
        """
        Configure authentication using IDP user and password.

        Raises:
            ValueError: When required authentication details are missing or
                        connection fails.
        """
        if not self.idp_user or not self.idp_pass or self.admin_user == "kong_admin":
            raise ValueError(
                "idp_user, ipd_pass and admin_user should be provided and non-empty."
            )
        try:
            auth_url = f"{self.admin_url}/auth"
            self.session.get(
                auth_url,
                headers={"Kong-Admin-User": self.admin_user},
                auth=(str(self.idp_user), str(self.idp_pass)),
                verify=self.tls,
            )
            self.session.headers.update(self.headers())
        except requests.ConnectionError:
            raise ValueError(
                (
                    f"Failed to connect to {self.admin_url}/auth. Please "
                    "ensure the URL is correct and reachable."
                )
            )

    def configure_token(self) -> None:
        """
        Configure authentication using the admin token.
        """
        self.session.headers.update(self.headers())

    def fetch_all(self, endpoint: Optional[str]) -> List[Dict[str, Any]]:
        """
        Fetches all objects by paginating through the provided endpoint until no
        more objects are left.

        Args:
            endpoint (str): The API endpoint to start fetching from.

        Returns:
            List[Dict[str, Any]]: A list of all objects retrieved from the
                                  provided endpoint.
        """
        all_data: List[Dict[str, Any]] = []
        while endpoint:  # Continue fetching as long as there's an endpoint
            response = self.request("GET", endpoint)

            if hasattr(response, "data"):
                all_data.extend(response.data)

            endpoint = getattr(response, "next", None)

        return all_data

    def request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        """
        Send a request to the Kong Admin API and handle the response.

        Args:
            method (str): The HTTP method (e.g., GET, POST, PUT).
            endpoint (str): The endpoint for the request.
            **kwargs: Additional arguments passed to the requests session.

        Returns:
            Any: A ResponseObject instance wrapping the response data.

        Raises:
            ValueError: When connection to the Kong Admin API fails.
        """
        try:
            url = f"{self.admin_ws_url}{endpoint}"
            if method == "GET" or method == "DELETE":
                self.session.headers.update({"Content-Type": ""})
            else:
                self.session.headers.update(
                    {"Content-Type": "application/json;charset=utf-8"}
                )
            response = self.session.request(method, url, verify=self.tls, **kwargs)
            if not response.ok:
                print(response.text)
            response.raise_for_status()
            response_data = response.json() if response.content else {}
            result = ResponseObject(response_data)
            if hasattr(result, "is_empty") and result.is_empty:
                return None
            return result
        except requests.ConnectionError:
            raise ValueError(
                (
                    f"Failed to connect to {self.admin_ws_url}{endpoint}."
                    "Please ensure the URL is correct and reachable."
                )
            )
