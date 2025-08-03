from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient

import uuid

# Inicializálás
subscription_id = "<AZURE_SUBSCRIPTION_ID>"  # pl. 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

def clone_vm(resource_group, vm_name):
    print(f"🛠 Klónozás indítása: {vm_name} a(z) {resource_group} RG-ben")

    # 1️⃣ Eredeti VM lekérése
    vm = compute_client.virtual_machines.get(resource_group, vm_name)

    # 2️⃣ Új VM neve
    new_vm_name = f"{vm_name}-clone-{str(uuid.uuid4())[:4]}"

    # 3️⃣ Image + storage + NIC + méret megtartása
    vm_params = {
        "location": vm.location,
        "hardware_profile": vm.hardware_profile,
        "storage_profile": vm.storage_profile,
        "os_profile": {
            "computer_name": new_vm_name,
            "admin_username": vm.os_profile.admin_username,
            "admin_password": "<AZURE_ADMIN_PASSWORD>"  # vagy SSH key
        },
        "network_profile": vm.network_profile,
    }

    # 4️⃣ VM létrehozása
    creation_result = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name=resource_group,
        vm_name=new_vm_name,
        parameters=vm_params
    )

    result = creation_result.result()
    print(f"✅ Új VM létrehozva: {new_vm_name}")
    return new_vm_name