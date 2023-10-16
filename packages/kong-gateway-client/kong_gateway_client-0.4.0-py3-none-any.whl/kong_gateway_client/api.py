from typing import Optional
from kong_gateway_client.client import KongClient
from kong_gateway_client.common import ResponseObject
from kong_gateway_client.resources.consumer_groups import ConsumerGroup
from kong_gateway_client.resources.services import Service
from kong_gateway_client.resources.routes import Route
from kong_gateway_client.resources.consumers import Consumer
from kong_gateway_client.resources.plugins import PluginResource
from kong_gateway_client.resources.plugin_types.key_auth import KeyAuthPlugin
from kong_gateway_client.resources.plugin_types.acl import ACLPlugin
from kong_gateway_client.resources.plugin_types.rate_limiting_advanced import (
    RateLimitingAdvancedPlugin,
)


class KongAPIClient:
    def __init__(
        self,
        admin_url: str = "http://localhost:8001",
        admin_token: Optional[str] = None,
        admin_user: str = "kong_admin",
        idp_user: Optional[str] = None,
        idp_pass: Optional[str] = None,
        verify_tls: bool = False,
        workspace: str = "default",
    ):
        self.client = KongClient(
            Service,
            Route,
            PluginResource,
            Consumer,
            ConsumerGroup,
            KeyAuthPlugin,
            ACLPlugin,
            RateLimitingAdvancedPlugin,
            ResponseObject,
            admin_url=admin_url,
            admin_token=admin_token,
            admin_user=admin_user,
            idp_user=idp_user,
            idp_pass=idp_pass,
            verify_tls=verify_tls,
            workspace=workspace,
        )

    def __getattr__(self, name):
        return getattr(self.client, name)

    def get_kong_client(self):
        return self.client
