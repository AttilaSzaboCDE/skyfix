from app import *
from azure.identity import ClientSecretCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient

def cont_restarting(container_name: str, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
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
        # --- Leállítás
        container_client.container_groups.begin_stop(resource_group, container_name).wait()

        # --- Újraindítás
        container_client.container_groups.begin_start(resource_group, container_name).wait()

        return 0, f"Container {container_name} restarted successfully"
    except Exception as e:
        return 1, str(e)
