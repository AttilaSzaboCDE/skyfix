
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential


# Megállítjuk a virtuális gépet
def stop_vm_by_name(vm_name: str, tenant_id: str, client_id: str, client_secret: str):
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Ha tudod, add meg fixen az előfizetés ID-t, ha nem, keresd meg a VM alapján (lentebb)
    subscription_id = "0dacaab7-697f-4dc8-a0aa-227fe9c54a49"  # Írd ide a subscription id-t

    resource_client = ResourceManagementClient(credential, subscription_id)

    # Kilistázzuk az összes erőforrást az adott subscriptionben
    resources = list(resource_client.resources.list())

    vm_resource = None
    for res in resources:
        if res.name.lower() == vm_name.lower():
            vm_resource = res
            break

    if not vm_resource:
        print(f"Nem található VM a '{vm_name}' névvel.")
        return

    resource_group = vm_resource.id.split("/")[4]
    subscription_id = vm_resource.id.split("/")[2]

    print(f"VM megtalálva: {vm_resource.name}")
    print(f"Resource Group: {resource_group}")
    print(f"Subscription: {subscription_id}")

    compute_client = ComputeManagementClient(credential, subscription_id)

    # VM leállítása
    async_vm_deallocate = compute_client.virtual_machines.begin_deallocate(resource_group_name=resource_group, vm_name=vm_name)
    async_vm_deallocate.wait()

    print(f"A '{vm_name}' virtuális gép leállítva.")