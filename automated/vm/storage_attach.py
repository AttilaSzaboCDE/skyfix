from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential
from azure.mgmt.compute.models import DiskCreateOption, CreationData, Disk
from app import *

global storage_status

def storage_attach(vm_name: str, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Subscription ID
    subscription_id = subscription_id  # Írd ide a subscription id-t
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

    compute_client = ComputeManagementClient(credential, subscription_id)

    # Storage paraméterek
    disk_size = 50 # GB
    disk_name = f"{vm_name}-data-disk"
    
    # Létrehozzuk a lemezt
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
    print(f"Disk létrehozva: {disk.id}")
    
    # VM lekérése
    vm = compute_client.virtual_machines.get(resource_group, vm_name)
    
    
    # LUN megadása
    lun = 0
    if vm.storage_profile.data_disks:
        lun = len(vm.storage_profile.data_disks)

    # Új lemez hozzácsatolása
    vm.storage_profile.data_disks.append({
        "lun": lun,
        "name": disk_name,
        "create_option": DiskCreateOption.attach,
        "managed_disk": {
            "id": disk.id
        }
    })

    # VM frissítése
    async_vm_update = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name=resource_group,
        vm_name=vm_name,
        parameters=vm
    )
    result = async_vm_update.result()
    
    if result.provisioning_state == "Succeeded":
        return 0 # Storage attached successfully
    else:
        return 1 # Storage attachment failed
    