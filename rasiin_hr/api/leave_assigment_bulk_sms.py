import frappe
def send_bulk_sms():
    em = frappe.db.get_list("Leaves Assigment" , filters = {"to_date" : frappe.utils.getdate()} , fields = ['employee_name', 'to_date']) 
    if em:
        for e in em:
            mobile= frappe.db.get_value("Employee",{"employee_name":e.employee_name},"cell_number")
            if mobile:
                frappe.call("frappe.core.doctype.sms_settings.sms_settings.send_sms", 
                    msg=e.employee_name+", Fadlan xasuusnow waqtigii Fasaxaagu waxa uu ku ekaaa "+str(e.to_date),  
                    receiver_list=[mobile])