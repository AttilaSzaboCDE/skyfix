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
from database.skyfix_db import *


# Globális változók

alert_list = []             # alert logs
running_list = []           # running scripts logs
results_list = []           # results of running scripts
missing_list = []           # missing scripts logs


# database connection
conn2 = connect(database_name)
cur1 = conn2.cursor()


def detection_check(alert_json, sub_id, az_tenant_id, az_client_id, az_client_secret):
    global resourcename, alert_type, alert_status
    azure_credential_sub_id = sub_id
    azure_credential_tenant_id = az_tenant_id
    azure_credential_client_id = az_client_id
    azure_credential_secret_key = az_client_secret
    
    resourcename = alert_json["alerts"][0]["labels"]["resourceName"]
    alert_status = alert_json["alerts"][0]["labels"]["reason"]
    
    
    # find the output in the alert_json
    alert_type = alert_json["status"]
    if alert_type == "firing":
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_list.append([resourcename, alert_status, time])
        cur1.execute("INSERT INTO alerts_list (service_name, issue_type, timestamp) VALUES (?, ?, ?)", (resourcename, alert_status, time))
        conn2.commit()
        #### TEST #####
        cur.execute("SELECT * FROM alerts_list")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        ###############
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
            # cur.execute("INSERT INTO scripts_log_list (script_id, service_name, status) VALUES (?, ?, ?)", ("stop_vm_by_name", resourcename, "success"))
        else:
            results_list.append(["stop_vm_by_name", resourcename, False])
            #cur.execute("INSERT INTO other_issues_list (script_id, description, status) VALUES (?, ?, ?)", ("stop_vm_by_name", resourcename, "failed"))
            
    elif alert_reason == "lowdiskspace":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "storage_attach"]
        running_list.append(running_item)
        storage_state = storage_attach(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
        if storage_state == 0:
            running_list.remove(running_item)
            results_list.append(["storage_attach", resourcename, True])
            #cur.execute("INSERT INTO scripts_log_list (script_id, service_name, status) VALUES (?, ?, ?)", ("storage_attach", resourcename, "success"))
        else:
            results_list.append(["storage_attach", resourcename, False])
            #cur.execute("INSERT INTO other_issues_list (script_id, description, status) VALUES (?, ?, ?)", ("storage_attach", resourcename, "failed"))
    elif alert_reason == "memoryusage":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "scale_up"]
        running_list.append(running_item)
        memory_state = vm_scale_up(resourcename, azure_credential_tenant_id, azure_credential_client_id, azure_credential_secret_key, azure_credential_sub_id)
        if memory_state == 0:
            running_list.remove(running_item)
            results_list.append(["storage_a ttach", resourcename, True])
            #cur.execute("INSERT INTO scripts_log_list (script_id, service_name, status) VALUES (?, ?, ?)", ("scale_up", resourcename, "success"))
        else:
            results_list.append(["storage_attach", resourcename, False])
            #cur.execute("INSERT INTO other_issues_list (script_id, description, status) VALUES (?, ?, ?)", ("scale_up", resourcename, "failed"))
    elif alert_reason == "vmstopped":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "vm_restart"]
        running_list.append(running_item)
        vm_state2 = vm_restart()
        if vm_state2 == 0:
            running_list.remove(running_item)
            results_list.append(["vm_restart", resourcename, True])
            #cur.execute("INSERT INTO scripts_log_list (script_id, service_name, status) VALUES (?, ?, ?)", ("vm_restart", resourcename, "success"))
        else:
            results_list.append(["vm_restart", resourcename, False])
            #cur.execute("INSERT INTO other_issues_list (script_id, description, status) VALUES (?, ?, ?)", ("vm_restart", resourcename, "failed"))
    else:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "vm_restart"]
        missing_list.append(running_item)
        #cur.execute("INSERT INTO other_issues_list (script_id, description, status) VALUES (?, ?, ?)", ("unknown_alert", resourcename, "unknown alert reason"))
        
    ### End of VM alert reasons
    
    
    # Separator for different alert reasons - CONTAINERS
    if alert_reason == "cont_highcpu":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_item = [resourcename, date_time, "stop_vm_by_name"]  # <-- elmentjük
              
    return 0



