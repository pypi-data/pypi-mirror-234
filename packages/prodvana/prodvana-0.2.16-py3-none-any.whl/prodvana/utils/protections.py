import os
from typing import Callable

from prodvana.client import Client
from prodvana.proto.prodvana.service.service_config_pb2 import (
    CompiledServiceInstanceConfig,
)
from prodvana.proto.prodvana.service.service_manager_pb2 import GetServiceInstanceReq


class InjectedVariables:
    PVN_APPLICATION = "PVN_APPLICATION"
    PVN_RELEASE_CHANNEL = "PVN_RELEASE_CHANNEL"
    PVN_SERVICE = "PVN_SERVICE"


def must_get_env(key: str, msg: str) -> str:
    val = os.getenv(key)
    assert val, f"{key} not set. {msg}"
    return val


def service_config_protection(
    client: Client, check: Callable[[CompiledServiceInstanceConfig], None]
) -> None:
    """
    A protection that is meant to run at the service or convergence level.
    `check` is a function that should throw an exception if there is something wrong with the service configuration.
    At the service level, check is called with the current service configuration.
    At the convergence level, check is called with each unique incoming service configuration.
    """
    # TODO(naphat) support convergence protections
    app = must_get_env(
        InjectedVariables.PVN_APPLICATION,
        "Only service-instance-level protections are supported",
    )
    rc = must_get_env(
        InjectedVariables.PVN_RELEASE_CHANNEL,
        "Only service-instance-level protections are supported",
    )
    svc = must_get_env(
        InjectedVariables.PVN_SERVICE,
        "Only service-instance-level protections are supported",
    )
    resp = client.service_manager.GetServiceInstance(
        GetServiceInstanceReq(
            application=app,
            release_channel=rc,
            service=svc,
        )
    )
    check(resp.service_instance.config)
