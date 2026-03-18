import requests
import datetime
import json
import frappe



@frappe.whitelist()
def send_sms_for_all_emp(list_off_emp):
    for em in list_off_emp:
        pass

    

# print(resp_dict1)
@frappe.whitelist()
def send_sms(mobile = "0612926234" , messge = "test"):
    payload = "grant_type=password&username=Mogadishosp&password=i8wef8q2l7RH1yeCLwn6Cw=="
    response = requests.request("POST", 'https://smsapi.hormuud.com/token', data=payload,
    headers={'content-type': "application/x-www-form-urlencoded"})
    resp_dict1 = json.loads(response.text)
    payload = {
    "senderid":"MSH Hospital",
    "mobile":mobile,
    "message":messge
    }
    sendsmsResp = requests.request("POST", 'https://smsapi.hormuud.com/api/SendSMS',data= json.dumps(payload),
    headers={'Content-Type':'application/json', 'Authorization': 'Bearer ' + resp_dict1['access_token']})

    respObj = json.loads(sendsmsResp.text)
    # frappe.msgprint("Sent SMS")
    frappe.errprint(respObj)
    return respObj