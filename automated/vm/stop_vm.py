from app import *
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential

def stop_vm_by_name(vm_name: str, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    subscription_id = subscription_id 
    resource_client = ResourceManagementClient(credential, subscription_id)

    resources = list(resource_client.resources.list())

    vm_resource = None
    for res in resources:
        if res.name.lower() == vm_name.lower():
            vm_resource = res
            break

    if not vm_resource:
        return 1, str("VM not found")

    resource_group = vm_resource.id.split("/")[4]
    subscription_id = vm_resource.id.split("/")[2]

    compute_client = ComputeManagementClient(credential, subscription_id)

    try:
        async_vm_deallocate = compute_client.virtual_machines.begin_deallocate(resource_group_name=resource_group, vm_name=vm_name)
        async_vm_deallocate.wait()
        return 0, "" 
    except Exception as e:
        return 1, str(e) 
    