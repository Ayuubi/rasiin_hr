from dataclasses import fields
import requests
import datetime
import json
import frappe
@frappe.whitelist()
def send_sms():
    em_p = frappe.db.get_list("Employee" , filters = {"status" : "Active"} , fields = ['employee_name', 'cell_number'])
    payload = "grant_type=password&username=Mogadishosp&password=i8wef8q2l7RH1yeCLwn6Cw=="
    response = requests.request("POST", 'https://smsapi.hormuud.com/token', data=payload,
    headers={'content-type': "application/x-www-form-urlencoded"})
    resp_dict1 = json.loads(response.text)
    try:
        for em in em_p:
            # print(resp_dict1)
            # if em.employee_name == "HR-EMP-00065":

            payload = {
            "senderid":"Sender Name",
            "mobile":em.cell_phone,
            "message":"Test SMS"
            }
            sendsmsResp = requests.request("POST", 'https://smsapi.hormuud.com/api/SendSMS',data= json.dumps(payload),
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer ' + resp_dict1['access_token']})

            respObj = json.loads(sendsmsResp.text)
            frappe.errprint(em.employee_name)
    except:
        frappe.errprint(em.employee_name)