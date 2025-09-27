from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential
from azure.mgmt.compute.models import DiskCreateOption, CreationData, Disk
from app import *


def storage_attach(vm_name: str, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
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
        disk = list(compute_client.disks.list_by_resource_group(resource_group))
        existing_disk_names = [d.name for d in disk]

        disk_size = 50  # GB
        disk_name = f"{vm_name}-data-disk"
        if disk_name not in existing_disk_names:
            pass
        
        i = 1
        while f"{disk_name}-{i}" in existing_disk_names:
            i += 1
            disk_name = f"{vm_name}-data-disk-{i}"

        async_disk_creation = compute_client.disks.begin_create_or_update(
            resource_group_name=resource_group,
            disk_name=disk_name,
            parameters=Disk(
                location=vm_resource.location,
                disk_size_gb=disk_size,
                creation_data=CreationData(
                    create_option=DiskCreateOption.empty
                )
            )
        )

        disk = async_disk_creation.result()

        vm = compute_client.virtual_machines.get(resource_group, vm_name)

        lun = 0
        if vm.storage_profile.data_disks:
            lun = len(vm.storage_profile.data_disks)

        vm.storage_profile.data_disks.append({
            "lun": lun,
            "name": disk_name,
            "create_option": DiskCreateOption.attach,
            "managed_disk": {
                "id": disk.id
            }
        })

        async_vm_update = compute_client.virtual_machines.begin_create_or_update(
            resource_group_name=resource_group,
            vm_name=vm_name,
            parameters=vm
        )
        async_vm_update.wait()
        return 0, "" 
    except Exception as e:
        return 1, str(e)

    