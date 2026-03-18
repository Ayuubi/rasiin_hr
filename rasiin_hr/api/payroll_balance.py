import  frappe
from erpnext.accounts.utils import get_balance_on
from hrms.hr.report.employee_advance_summary.employee_advance_summary import get_advances
from frappe.utils import getdate
@frappe.whitelist()
def get_receivable(customer):
    # frappe.msgprint(customer)
    bal= get_balance_on(company = frappe.defaults.get_user_default("Company"),
                        party_type ="Customer",
                        party =frappe.db.get_value("Customer",{"customer_name":customer}, "name"),
                        date = getdate())
    
    return bal
@frappe.whitelist()
def get_advances(emp):
    empl =frappe.db.get_value("Employee",{"employee_name":emp}, "name")
    
    advance= frappe.db.sql(
        f"""select name, employee, paid_amount, status, advance_amount, claimed_amount, company,
        posting_date, purpose
        from `tabEmployee Advance`
        where docstatus<2 and employee='{empl}' order by posting_date, name desc""",
        
        as_dict=1,
    )
    advanced=0
    for i in advance:
        advanced= i.advance_amount
        
    return advanced
