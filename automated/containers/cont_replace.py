from app import *
from azure.identity import ClientSecretCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient

def cont_replace(container_name: str, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    container_client = ContainerInstanceManagementClient(credential, subscription_id)

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

        if hasattr(group_def, 'diagnostics') and group_def.diagnostics and hasattr(group_def.diagnostics, 'log_analytics'):
            group_def.diagnostics.log_analytics = None

        container_client.container_groups.begin_delete(resource_group, container_name).wait()
        async_create = container_client.container_groups.begin_create_or_update(
            resource_group,
            container_name,
            group_def
        )
        async_create.wait()
        return 0, ""
    except Exception as e:
        return 1, str(e)
