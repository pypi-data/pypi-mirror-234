import mock

from prodvana.client import Client
from prodvana.proto.prodvana.common_config import program_pb2
from prodvana.proto.prodvana.desired_state import manager_pb2
from prodvana.proto.prodvana.desired_state.model import desired_state_pb2
from prodvana.proto.prodvana.service import (
    service_config_pb2,
    service_manager_pb2,
    service_manager_pb2_grpc,
)
from prodvana.utils.service_config import (
    ImageDetails,
    TagDetails,
    get_target_images_for_desired_state,
)


def test_get_target_commits_with_image_urls() -> None:
    def fake_get_service_config(
        req: service_manager_pb2.GetMaterializedConfigReq,
    ) -> service_manager_pb2.GetMaterializedConfigResp:
        return service_manager_pb2.GetMaterializedConfigResp(
            config=service_config_pb2.ServiceConfig(
                programs=[
                    program_pb2.ProgramConfig(
                        image={
                            "pvn-service-1": "pvn-service:1",
                            "pvn-service-2": "pvn-service:2",
                        }[req.version],
                    )
                ],
            ),
        )

    client = mock.Mock(spec=Client)
    client.service_manager = mock.Mock(spec=service_manager_pb2_grpc.ServiceManagerStub)
    client.service_manager.GetMaterializedConfig = mock.Mock()
    client.service_manager.GetMaterializedConfig.side_effect = fake_get_service_config

    images = get_target_images_for_desired_state(
        client,
        manager_pb2.DesiredStateSummary(
            desired_state=desired_state_pb2.State(
                service=desired_state_pb2.ServiceState(
                    release_channels=[
                        desired_state_pb2.ServiceInstanceState(
                            versions=[
                                desired_state_pb2.Version(
                                    version="pvn-service-1",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ),
    )
    assert images == set[ImageDetails]([ImageDetails(image_url="pvn-service:1")])

    images = get_target_images_for_desired_state(
        client,
        manager_pb2.DesiredStateSummary(
            desired_state=desired_state_pb2.State(
                service=desired_state_pb2.ServiceState(
                    release_channels=[
                        desired_state_pb2.ServiceInstanceState(
                            release_channel="staging",
                            versions=[
                                desired_state_pb2.Version(
                                    version="pvn-service-2",
                                ),
                            ],
                        ),
                        desired_state_pb2.ServiceInstanceState(
                            release_channel="production",
                            versions=[
                                desired_state_pb2.Version(
                                    version="pvn-service-1",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ),
    )
    assert images == set[ImageDetails](
        [
            ImageDetails(image_url="pvn-service:2"),
            ImageDetails(image_url="pvn-service:1"),
        ]
    )


def test_get_target_commits_with_image_tag() -> None:
    def fake_get_service_config(
        req: service_manager_pb2.GetMaterializedConfigReq,
    ) -> service_manager_pb2.GetMaterializedConfigResp:
        return service_manager_pb2.GetMaterializedConfigResp(
            config=service_config_pb2.ServiceConfig(
                programs=[
                    program_pb2.ProgramConfig(
                        image_tag={
                            "pvn-service-1": "1",
                            "pvn-service-2": "2",
                        }[req.version],
                        image_registry_info=program_pb2.ImageRegistryInfo(
                            image_repository="pvn-service",
                            container_registry="pvn-registry",
                        ),
                    )
                ],
            ),
        )

    client = mock.Mock(spec=Client)
    client.service_manager = mock.Mock(spec=service_manager_pb2_grpc.ServiceManagerStub)
    client.service_manager.GetMaterializedConfig = mock.Mock()
    client.service_manager.GetMaterializedConfig.side_effect = fake_get_service_config

    images = get_target_images_for_desired_state(
        client,
        manager_pb2.DesiredStateSummary(
            desired_state=desired_state_pb2.State(
                service=desired_state_pb2.ServiceState(
                    release_channels=[
                        desired_state_pb2.ServiceInstanceState(
                            versions=[
                                desired_state_pb2.Version(
                                    version="pvn-service-1",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ),
    )
    assert images == set[ImageDetails](
        [
            ImageDetails(
                tag=TagDetails(
                    tag="1",
                    repository="pvn-service",
                    registry_name="pvn-registry",
                    registry_id="",
                ),
            )
        ]
    )

    images = get_target_images_for_desired_state(
        client,
        manager_pb2.DesiredStateSummary(
            desired_state=desired_state_pb2.State(
                service=desired_state_pb2.ServiceState(
                    release_channels=[
                        desired_state_pb2.ServiceInstanceState(
                            release_channel="staging",
                            versions=[
                                desired_state_pb2.Version(
                                    version="pvn-service-2",
                                ),
                            ],
                        ),
                        desired_state_pb2.ServiceInstanceState(
                            release_channel="production",
                            versions=[
                                desired_state_pb2.Version(
                                    version="pvn-service-1",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ),
    )
    assert images == set[ImageDetails](
        [
            ImageDetails(
                tag=TagDetails(
                    tag="2",
                    repository="pvn-service",
                    registry_name="pvn-registry",
                    registry_id="",
                ),
            ),
            ImageDetails(
                tag=TagDetails(
                    tag="1",
                    repository="pvn-service",
                    registry_name="pvn-registry",
                    registry_id="",
                ),
            ),
        ]
    )
