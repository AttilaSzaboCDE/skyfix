import sys
from datetime import datetime
from threading import Lock
from time import sleep
from automated.vm.stop_vm import stop_vm_by_name
from automated.vm.stop_vm import *
from app import *
from automated.vm.storage_attach import storage_attach
from automated.vm.storage_attach import *
from automated.vm.vm_restart import vm_restart
from automated.vm.vm_restart import *
from automated.vm.scale_up import vm_scale_up
from automated.vm.scale_up import *
from database.skyfix_db import insert_alert, insert_script_log, insert_other_issue
from automated.containers.cont_restart import cont_restarting
from automated.containers.cont_replace import cont_replace
from automated.containers.cont_scale import cont_scale_up

alert_list = []             # alert logs
running_list = []           # running scripts logs
results_list = []           # results of running scripts
missing_list = []           # missing scripts logs

def detection_check(alert_json, sub_id, az_tenant_id, az_client_id, az_client_secret):
    azure_credential_sub_id = sub_id
    azure_credential_tenant_id = az_tenant_id
    azure_credential_client_id = az_client_id
    azure_credential_secret_key = az_client_secret

    alert_type = alert_json["status"]
    if alert_type == "firing":
        resourcename = alert_json["alerts"][0]["labels"]["resourceName"]
        alert_reason = alert_json["alerts"][0]["labels"]["reason"]

        if alert_reason in ["highcpu", "lowdiskspace", "memoryusage", "vmstopped"]:
            alert_service_type = "vm"
        else:
            alert_service_type = "container"

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        alert_list.append([resourcename, alert_service_type, alert_reason, time])
        insert_alert(resourcename, alert_service_type, alert_reason, time)
        fault_type_choose(resourcename,alert_reason,alert_service_type, azure_credential_sub_id, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key)
    return 0

def fault_type_choose(resourcename, alert_reason, alert_service_type, sub_id, az_tenant_id, az_client_id, az_client_secret):
    alert_reason = alert_reason
    azure_credential_sub_id = sub_id
    azure_credential_tenant_id = az_tenant_id
    azure_credential_client_id = az_client_id
    azure_credential_secret_key = az_client_secret
    scripts_name_list = ["stop_vm_by_name", "storage_attach", "vm_scale_up", "vm_restart"]
    cont_scripts_name_list = ["cont_replace", "cont_restarting", "cont_scale_up"]
    stop_result = ""
    cont_state = 2

    if resourcename in [x[0] for x in running_list]:
        return 0

    if alert_service_type == "vm":
        if alert_reason == "highcpu":
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            running_item = [resourcename, alert_reason, scripts_name_list[0]]  # <-- elmentjük
            running_list.append(running_item)
            sleep(5)  # <-- szimuláljuk a futást
            vm_state, stop_result = stop_vm_by_name(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
            if vm_state == 0:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, scripts_name_list[0],  True])
                insert_script_log(resourcename, alert_service_type, scripts_name_list[0], date_time, "success")
            else:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, scripts_name_list[0],  False])
                insert_script_log(resourcename, alert_service_type, scripts_name_list[0], date_time, "fail")
                missing_list.append([resourcename, alert_service_type, stop_result, "fail"])
                insert_other_issue(resourcename, alert_service_type, stop_result, date_time, "fail")

        elif alert_reason == "lowdiskspace":
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            running_item = [resourcename, alert_reason, scripts_name_list[1]]
            running_list.append(running_item)
            sleep(5)
            storage_state, stop_result = storage_attach(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
            if storage_state == 0:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, scripts_name_list[1],  True])
                insert_script_log(resourcename, alert_service_type, scripts_name_list[1], date_time, "success")
            else:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, scripts_name_list[1],  False])
                insert_script_log(resourcename, alert_service_type, scripts_name_list[1], date_time, "fail")
                missing_list.append([resourcename, alert_service_type, stop_result, "fail"])
                insert_other_issue(resourcename, alert_service_type, stop_result, date_time, "fail")

        elif alert_reason == "memoryusage":
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            running_item = [resourcename, alert_reason, scripts_name_list[2]]
            running_list.append(running_item)
            sleep(5)
            memory_state, stop_result = vm_scale_up(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
            if memory_state == 0:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, scripts_name_list[2],  True])
                insert_script_log(resourcename, alert_service_type, scripts_name_list[2], date_time, "success")
            else:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, scripts_name_list[2],  False])
                insert_script_log(resourcename, alert_service_type, scripts_name_list[2], date_time, "fail")
                missing_list.append([resourcename, alert_service_type, stop_result, "fail"])
                insert_other_issue(resourcename, alert_service_type, stop_result, date_time, "fail")

        elif alert_reason == "vmstopped":
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            running_item = [resourcename, alert_reason, scripts_name_list[3]]
            running_list.append(running_item)
            sleep(5)
            vm_state2, stop_result = vm_restart(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
            if vm_state2 == 0:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, scripts_name_list[3],  True])
                insert_script_log(resourcename, alert_service_type, scripts_name_list[3], date_time, "success")

            else:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, scripts_name_list[3],  False])
                insert_script_log(resourcename, alert_service_type, scripts_name_list[3], date_time, "fail")
                missing_list.append([resourcename, alert_service_type, stop_result, "fail"])
                insert_other_issue(resourcename, alert_service_type, stop_result, date_time, "fail")
        else:
            missing_list.append([resourcename, alert_service_type, "Unknown alert reason", "fail"])
    elif alert_service_type == "container":
        if alert_reason == "contdown":
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            running_item = [resourcename, alert_reason, cont_scripts_name_list[1]]
            running_list.append(running_item)
            sleep(5)
            cont_state, stop_result = cont_restarting(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
            if cont_state == 0:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, cont_scripts_name_list[1],  True])
                insert_script_log(resourcename, alert_service_type, cont_scripts_name_list[1], date_time, "success")
            else:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, cont_scripts_name_list[1],  False])
                insert_script_log(resourcename, alert_service_type, cont_scripts_name_list[1], date_time, "fail")
                missing_list.append([resourcename, alert_service_type, stop_result, "fail"])
                insert_other_issue(resourcename, alert_service_type, stop_result, date_time, "fail")
        elif alert_reason == "conthighmem":
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            running_item = [resourcename, alert_reason, cont_scripts_name_list[2]]
            running_list.append(running_item)
            sleep(5)
            cont_state, stop_result = cont_scale_up(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
            if cont_state == 0:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, cont_scripts_name_list[2],  True])
                insert_script_log(resourcename, alert_service_type, cont_scripts_name_list[2], date_time, "success")
            else:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, cont_scripts_name_list[2],  False])
                insert_script_log(resourcename, alert_service_type, cont_scripts_name_list[2], date_time, "fail")
                missing_list.append([resourcename, alert_service_type, stop_result, "fail"])
                insert_other_issue(resourcename, alert_service_type, stop_result, date_time, "fail")
        elif alert_reason == "contmiss":
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            running_item = [resourcename, alert_reason, cont_scripts_name_list[0]]
            running_list.append(running_item)
            sleep(5)
            cont_state, stop_result = cont_replace(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id) 
            if cont_state == 0:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, cont_scripts_name_list[0],  True])
                insert_script_log(resourcename, alert_service_type, cont_scripts_name_list[0], date_time, "success")
            else:
                running_list.remove(running_item)
                results_list.append([resourcename, alert_service_type, cont_scripts_name_list[0],  False])
                insert_script_log(resourcename, alert_service_type, cont_scripts_name_list[0], date_time, "fail")
                missing_list.append([resourcename, alert_service_type, stop_result, "fail"])
                insert_other_issue(resourcename, alert_service_type, stop_result, date_time, "fail")
        else:
            missing_list.append([resourcename, alert_service_type, "Unknown alert reason", "fail"])
    else:
        return 0
