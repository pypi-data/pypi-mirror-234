import os
from typing import Any, Callable, Optional

import grpc
from grpc_interceptor import ClientCallDetails, ClientInterceptor

from prodvana.proto.prodvana.application import application_manager_pb2_grpc
from prodvana.proto.prodvana.desired_state import manager_pb2_grpc
from prodvana.proto.prodvana.organization import organization_manager_pb2_grpc
from prodvana.proto.prodvana.release_channel import release_channel_manager_pb2_grpc
from prodvana.proto.prodvana.service import service_manager_pb2_grpc


class AuthClientInterceptor(ClientInterceptor):
    def __init__(self, api_token: str) -> None:
        self.token = api_token
        self.header_value = f"Bearer {self.token}"

    def intercept(
        self,
        method: Callable[[Any, grpc.ClientCallDetails], Any],
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ) -> Any:
        metadata = []
        if call_details.metadata is not None:
            metadata = list(call_details.metadata)
        metadata.append(("authorization", self.header_value))
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            metadata,
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request_or_iterator, new_details)


def make_channel(
    org: Optional[str] = None,
    apiserver_addr: Optional[str] = None,
    api_token: Optional[str] = None,
) -> grpc.Channel:
    """
    Make a new connection to Prodvana API.

    If `org` is provided, it is used to construct the api address automatically, i.e. api.<org>.prodvana.io.
    If `apiserver_addr` is provided, it is used. It must include both host name and port.
    Otherwise, env var PVN_APISERVER_ADDR is used.

    if `api_token` is not passed, env var PVN_TOKEN will be used.
    """
    if org is not None:
        apiserver_addr = f"api.{org}.prodvana.io:443"
    elif apiserver_addr is None:
        apiserver_addr = os.getenv("PVN_APISERVER_ADDR")
    assert (
        apiserver_addr
    ), "Must pass either `org`, `apiserver_addr`, or set env variable PVN_APISERVER_ADDR"
    if api_token is None:
        api_token = os.getenv("PVN_TOKEN")
    assert api_token, "Must pass either `api_token` or set env variabble PVN_TOKEN"
    server_name, _ = apiserver_addr.split(":")
    if server_name == "localhost":  # for testing only
        channel = grpc.insecure_channel(apiserver_addr)
    else:
        channel = grpc.secure_channel(apiserver_addr, grpc.ssl_channel_credentials())
    # use of an interceptor here instead of grpc.access_token_call_credentials is needed
    # because that function does not work with insecure_channel, see
    # https://groups.google.com/g/grpc-io/c/fFXbIXphudw
    channel = grpc.intercept_channel(channel, AuthClientInterceptor(api_token))
    return channel


class Client:
    def __init__(self, channel: grpc.Channel) -> None:
        self.application_manager = application_manager_pb2_grpc.ApplicationManagerStub(
            channel
        )
        self.organization_manager = (
            organization_manager_pb2_grpc.OrganizationManagerStub(channel)
        )
        self.release_channel_manager = (
            release_channel_manager_pb2_grpc.ReleaseChannelManagerStub(channel)
        )
        self.service_manager = service_manager_pb2_grpc.ServiceManagerStub(channel)
        self.desired_state_manager = manager_pb2_grpc.DesiredStateManagerStub(channel)
