"""The Fathom API client for querying flood and related data.
"""
import logging
from datetime import datetime, timedelta
from typing import Any, MutableMapping

import grpc

from proto.fathom import fathom_pb2, fathom_pb2_grpc

from .common import FathomException

FATHOM_GRPC_CHANNEL_MSG_SIZE = 10 * 1024 * 1024  # default 10MB

log = logging.getLogger(__name__)


class BaseClient:
    """A Client for interacting with the Fathom API."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        api_address: str = "api.fathom.global",
        msg_channel_size: int = FATHOM_GRPC_CHANNEL_MSG_SIZE,
    ) -> None:
        """Constructs a new Client, connected to a remote server.

        Args:
            api_address: Address of the Fathom API server.
            client_id: Client ID to identify a registered client on the
                    authorization server.
            client_secret: Client Secret used with client_id to get an
                    access token.
            msg_channel_size: gRPC message channel size, it is 10MB by
                default but if you will be dealing with data size larger than
                the default, you can configure the size.
        """
        log.info("fathom.Client: connecting to {}".format(api_address))

        if not client_id:
            raise FathomException("Client ID can not be empty")
        if not client_secret:
            raise FathomException("Client secret can not be empty")
        if not api_address:
            raise FathomException("API Address can not be empty")

        self._api_addr = api_address
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_conn = None
        self._message_size = msg_channel_size

        # expired at creation.
        self._token_expiry = datetime.utcnow() + timedelta(seconds=-0.5)
        self._channel = None

        self._stub_cache: MutableMapping[Any, Any] = {}

        # Check auth and initialise the channel
        _, _ = self._get_channel()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if channel := getattr(self, "_channel", None):
            channel.close()
            log.info("fathom.Client: closed gRPC channel")
            del self._channel

    def _get_channel(self) -> (grpc.Channel, bool):
        """Checks that the api credentials are still valid using an
        expiration time, creates a new grpc channel or use the previously
        created grpc channel depending on the condition.
        """
        channel_opt = [
            ("grpc.max_send_message_length", self._message_size),
            ("grpc.max_receive_message_length", self._message_size),
        ]

        new = False

        if self._token_expiry <= datetime.utcnow() or self._channel is None:
            call_creds = grpc.access_token_call_credentials(self._api_access_token())
            creds = grpc.composite_channel_credentials(
                grpc.ssl_channel_credentials(), call_creds
            )
            self._channel = grpc.secure_channel(
                self._api_addr, creds, options=channel_opt
            )
            new = True

        return self._channel, new

    def _get_stub(self, stub_type):
        """Gets a new stub for the given type from a new or cached channel"""
        channel, new = self._get_channel()

        if new or stub_type not in self._stub_cache:
            # Always create a new one if we had to create a new channel
            stub = stub_type(self._channel)
            self._stub_cache[stub_type] = stub

        return self._stub_cache[stub_type]

    def _api_access_token(self) -> str:
        """Returns an access token to authenticate with the Fathom API."""
        try:
            request = fathom_pb2.CreateAccessTokenRequest(
                client_id=self._client_id, client_secret=self._client_secret
            )
            channel = grpc.secure_channel(
                self._api_addr, grpc.ssl_channel_credentials()
            )
            stub = fathom_pb2_grpc.FathomServiceStub(channel)
            response = stub.CreateAccessToken(request)
            channel.close()
            self._token_expiry = datetime.utcnow() + timedelta(
                seconds=response.expire_secs
            )
            return response.access_token
        except Exception as err:
            raise Exception("Could not obtain access token from auth server") from err
