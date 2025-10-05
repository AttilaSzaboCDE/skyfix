from app import *
from azure.identity import ClientSecretCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient

def cont_scale_up(container_name: str, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
    cpu_increase: float = 0.5
    mem_increase: float = 0.5

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    container_client = ContainerInstanceManagementClient(credential, subscription_id)

    # --- Konténer keresése
    groups = list(container_client.container_groups.list())
    target_group = None
    for g in groups:
        if g.name.lower() == container_name.lower():
            target_group = g
            break

    if not target_group:
        return 1, "Container not found"

    resource_group = target_group.id.split("/")[4]

    try:
        group_def = container_client.container_groups.get(resource_group, container_name)

        container = group_def.containers[0]

        old_volumes = getattr(group_def, "volumes", None)
        old_volume_mounts = getattr(container, "volume_mounts", None)

        if hasattr(group_def, 'diagnostics') and group_def.diagnostics and hasattr(group_def.diagnostics, 'log_analytics'):
            group_def.diagnostics.log_analytics = None

        container_client.container_groups.begin_delete(resource_group, container_name).wait()

        from azure.mgmt.containerinstance.models import (
            ContainerGroup,
            Container,
            ResourceRequests,
            ResourceRequirements,
            ContainerPort,
            IpAddress,
            Port,
            OperatingSystemTypes
        )

        new_container = Container(
            name=container.name,
            image=container.image,
            resources=ResourceRequirements(
                requests=ResourceRequests(cpu=cpu_increase, memory_in_gb=mem_increase)
            ),
            ports=container.ports,
            environment_variables=container.environment_variables,
            volume_mounts=old_volume_mounts
        )

        new_group = ContainerGroup(
            location=group_def.location,
            os_type=group_def.os_type or OperatingSystemTypes.linux,
            containers=[new_container],
            restart_policy=group_def.restart_policy,
            ip_address=group_def.ip_address
        )

        async_create = container_client.container_groups.begin_create_or_update(
            resource_group,
            container_name,
            new_group
        )
        async_create.wait()

        return 0, ""
    except Exception as e:
        return 1, str(e)
