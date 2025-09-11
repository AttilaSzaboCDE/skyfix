from app import *
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential

def vm_scale_up(vm_name: str, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
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
        print(f"Nem található VM a '{vm_name}' névvel.")
        return 5
    
    resource_group = vm_resource.id.split("/")[4]
    subscription_id = vm_resource.id.split("/")[2]
    
    compute_client = ComputeManagementClient(credential, subscription_id)
    
    async_vm_deallocate = compute_client.virtual_machines.begin_deallocate(resource_group_name=resource_group, vm_name=vm_name)
    async_vm_deallocate.wait()
    
    vm = compute_client.virtual_machines.get(resource_group_name=resource_group, vm_name=vm_name)
    current_size = vm.hardware_profile.vm_size
    location = vm.location
    
    # Lekérjük az elérhető méreteket az adott régióban
    available_sizes = compute_client.virtual_machine_sizes.list(location)
    size_list = [s.name for s in available_sizes]  # lista a nevekkel
    
    current_size = vm.hardware_profile.vm_size
    try:
        current_index = size_list.index(current_size)
    except ValueError:
        print("A jelenlegi VM méret nincs a listában.")
        return
    
    if current_index + 1 < len(size_list):
        new_size = size_list[current_index + 1]
    else:
        print("Nincs nagyobb VM méret a listában.")
        return
    
    # VM méretének módosítása
    vm.hardware_profile.vm_size = new_size
    async_vm_update = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name=resource_group,
        vm_name=vm_name,
        parameters=vm
    )
    async_vm_update.wait()
    print(f"{vm_name} mérete {new_size}-re módosítva.")

    # VM újraindítása
    async_vm_start = compute_client.virtual_machines.begin_start(
        resource_group_name=resource_group,
        vm_name=vm_name
    )
    async_vm_start.wait()
    print(f"{vm_name} újraindítva.")
    
    power_state = compute_client.virtual_machines.instance_view(resource_group_name=resource_group, vm_name=vm_name).statuses[1].code
    
    if power_state == "PowerState/running":
        return 0 # VM deallocated
    else:
        return 3 # doesnt stopped
    
    