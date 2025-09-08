import sys
from datetime import datetime
from automated.vm.stop_vm import stop_vm_by_name
from automated.vm.stop_vm import *
from app import *
from automated.vm.storage_attach import storage_attach
from automated.vm.storage_attach import *
from automated.vm.vm_restart import vm_restart
from automated.vm.vm_restart import *
from automated.vm.scale_up import vm_scale_up
from automated.vm.scale_up import *


# Globális változók

alert_list = []             # alert logs
running_list = []           # running scripts logs
results_list = []           # results of running scripts
missing_list = []           # missing scripts logs

def detection_check(alert_json, sub_id, az_tenant_id, az_client_id, az_client_secret):
    global resourcename, alert_type, alert_status
    azure_credential_sub_id = sub_id
    azure_credential_tenant_id = az_tenant_id
    azure_credential_client_id = az_client_id
    azure_credential_secret_key = az_client_secret
    
    resourcename = alert_json["alerts"][0]["labels"]["resourceName"]
    alert_status = alert_json["alerts"][0]["labels"]["reason"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_list.append([resourcename, alert_status,time])
    
    
    # find the output in the alert_json
    alert_type = alert_json["status"]
    if alert_type == "firing":
        fault_type_choose(alert_status,azure_credential_sub_id, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key)
    return 0


def fault_type_choose(alert_status, sub_id, az_tenant_id, az_client_id, az_client_secret):
    
    ### basic variables
    alert_reason = alert_status
    azure_credential_sub_id = sub_id
    azure_credential_tenant_id = az_tenant_id
    azure_credential_client_id = az_client_id
    azure_credential_secret_key = az_client_secret
    
    ### Add the alert reason to the alert list
    if resourcename in [x[0] for x in running_list]:
        print(f"{resourcename} már fut")
        return 0

    
    ### Separator for different alert reasons - VIRTUAL MACHINES
    if alert_reason == "highcpu":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, alert_status,date_time, "stop_vm_by_name"]  # <-- elmentjük
        running_list.append(running_item)
        vm_state = stop_vm_by_name(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
        if vm_state == 0:
            running_list.remove(running_item)
            results_list.append(["stop_vm_by_name", resourcename, True])
        else:
            results_list.append(["stop_vm_by_name", resourcename, False])
            
    elif alert_reason == "lowdiskspace":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "storage_attach"]
        running_list.append(running_item)
        storage_state = storage_attach(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
        if storage_state == 0:
            running_list.remove(running_item)
            results_list.append(["storage_a ttach", resourcename, True])
        else:
            results_list.append(["storage_attach", resourcename, False])
    elif alert_reason == "memoryusage":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "scale_up"]
        running_list.append(running_item)
        memory_state = vm_scale_up(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
        if memory_state == 0:
            running_list.remove(running_item)
            results_list.append(["storage_a ttach", resourcename, True])
        else:
            results_list.append(["storage_attach", resourcename, False])
    elif alert_reason == "vmstopped":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "vm_restart"]
        running_list.append(running_item)
        vm_state2 = vm_restart()
        if vm_state2 == 0:
            running_list.remove(running_item)
            results_list.append(["vm_restart", resourcename, True])
        else:
            results_list.append(["vm_restart", resourcename, False])
    else:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "vm_restart"]
        missing_list.append(running_item)
    
    # Separator for different alert reasons - CONTAINERS
    if alert_reason == "cont_highcpu":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "stop_vm_by_name"]  # <-- elmentjük
        
        

    
    
    return 0




#def alerting(azure_credential_sub_id, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key):
#    azure_credential_sub_id = azure_credential_sub_id
#    azure_credential_tenant_id = azure_credential_tenant_id
#    azure_credential_client_id = azure_credential_client_id
#    azure_credential_secret_key = azure_credential_secret_key
#
#    if resourcename in [x[0] for x in running_list]:
#        print(f"{resourcename} már fut")
#    else:
#        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        running_item = [resourcename, date_time, "stop_vm_by_name"]  # <-- elmentjük
#        running_list.append(running_item)
#
#        vm_state = stop_vm_by_name(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
#
#        running_list.remove(running_item)  # <-- biztosan ugyanaz az objektum
#
#        if vm_state == 0:
#            results_list.append(["stop_vm_by_name", resourcename, True])
#        else:
#            results_list.append(["stop_vm_by_name", resourcename, False])
#
#            
#    return 0
#