import json
import requests


def get_current_enrollment(section):
    text = requests.get("https://stevens-scheduler.cfapps.io/p/2019F").text

    list = json.loads(text)
    for i in list:
        if (i.get('section') == section):
            return int(i.get('maxEnrollment')) - int(i.get('currentEnrollment'))

    raise ValueError("Invalid Course ID")







def write_data(section):
    f = open('data.txt', 'a')
    f.write(section)

def send_alert(section):
    request = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": "########################",
        "user": "#########################",
        "message": "Class " + section + " has an open seat!",
        "sound": "none",
        "title": "Notification"

    })


#get_current_enrollment2("PE 200G0")

