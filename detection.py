import sys
from datetime import datetime
from automated.vm.stop_vm import stop_vm_by_name



alert_list = []

def detection_check(alert_json):
    global resourcename
    global alert_type
    resourcename = alert_json["alerts"][0]["labels"]["resourceName"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_list.append([resourcename, time])
    
    # find the output in the alert_json
    alert_type = alert_json["status"]
    if alert_type == "firing":
        alerting()
        
    elif alert_type == "resolved":
        resolving()
    return resourcename


def alerting():
    #print("büdös fos " + alert_type)
    stop_vm_by_name(resourcename, "5098f6dd-9c42-4f9a-870f-62d23eebb258", "707ee7cf-faed-4b68-ab87-31327aa13896", "qmN8Q~.83Gebg0Vl1~LNBJym1TRECydS5~FO0dBD")
    return 0

def resolving():
    # This function can be used to resolve alerts or notifications
    pass