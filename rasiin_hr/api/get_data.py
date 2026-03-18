import frappe
@frappe.whitelist()
def get_data(user):
    if frappe.db.exists("User" ,user):
        return frappe.get_doc("User" , user)
    return False