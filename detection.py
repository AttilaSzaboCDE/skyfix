
alert_list = []

def detection_check(alert_json):
    resource_name = alert_json["alerts"][0]["labels"]["resourceName"]
    time = alert_json["alerts"][0]["startsAt"]
    alert_list.append([resource_name, time])
    return resource_name