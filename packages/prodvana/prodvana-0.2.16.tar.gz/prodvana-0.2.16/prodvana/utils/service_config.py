from collections.abc import Set
from typing import NamedTuple

from prodvana.client import Client
from prodvana.proto.prodvana.desired_state import manager_pb2
from prodvana.proto.prodvana.service import service_manager_pb2


class TagDetails(NamedTuple):
    tag: str
    repository: str | None
    registry_name: str | None
    registry_id: str | None


class ImageDetails(NamedTuple):
    image_url: str | None = None
    tag: TagDetails | None = None


def get_target_images_for_desired_state(
    client: Client, summary: manager_pb2.DesiredStateSummary
) -> Set[ImageDetails]:
    class ServiceVersion(NamedTuple):
        application: str
        service: str
        version: str

    target_versions = set[ServiceVersion]()
    if summary.desired_state.HasField("service"):
        service = summary.desired_state.service
        for rc in service.release_channels:
            target_versions.add(
                ServiceVersion(
                    application=service.application,
                    service=service.service,
                    version=rc.versions[0].version,
                )
            )

    if summary.desired_state.HasField("service_group"):
        service_group = summary.desired_state.service_group
        for service in service_group.services:
            for rc in service.release_channels:
                target_versions.add(
                    ServiceVersion(
                        application=service.application,
                        service=service.service,
                        version=rc.versions[0].version,
                    )
                )

    images = set[ImageDetails]()
    for version in target_versions:
        this_images = get_images_from_service_version(
            client,
            application=version.application,
            service=version.service,
            version=version.version,
        )
        images.update(this_images)
    return images


def get_images_from_service_version(
    client: Client, application: str, service: str, version: str
) -> Set[ImageDetails]:
    resp = client.service_manager.GetMaterializedConfig(
        service_manager_pb2.GetMaterializedConfigReq(
            application=application,
            service=service,
            version=version,
        )
    )

    images = set()
    for p in resp.config.programs:
        if p.image:
            images.add(ImageDetails(image_url=p.image))
        elif p.image_tag:
            images.add(
                ImageDetails(
                    tag=TagDetails(
                        tag=p.image_tag,
                        repository=p.image_registry_info.image_repository
                        if p.image_registry_info
                        else None,
                        registry_id=p.image_registry_info.container_registry_id
                        if p.image_registry_info
                        else None,
                        registry_name=p.image_registry_info.container_registry
                        if p.image_registry_info
                        else None,
                    )
                )
            )

    for rc in resp.config.per_release_channel:
        for prc in rc.programs:
            if prc.image:
                images.add(ImageDetails(image_url=prc.image))
            elif prc.image_tag:
                images.add(
                    ImageDetails(
                        tag=TagDetails(
                            tag=prc.image_tag,
                            repository=prc.image_registry_info.image_repository
                            if prc.image_registry_info
                            else None,
                            registry_id=prc.image_registry_info.container_registry_id
                            if prc.image_registry_info
                            else None,
                            registry_name=prc.image_registry_info.container_registry
                            if prc.image_registry_info
                            else None,
                        )
                    )
                )
    return images
