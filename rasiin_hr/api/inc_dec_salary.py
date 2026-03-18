import frappe
import calendar
@frappe.whitelist()
def inc_dec_salary(doc , method =None):
    current_date = frappe.utils.getdate(doc.start_date)
    # Get current month name
    # month_name = frappe.utils.data.month_name(current_date.month)

    salary_name = frappe.db.get_value("Salary Percentage" , {"month" : "April" } , "name")
    if salary_name:
    
        salary_doc = frappe.get_doc("Salary Percentage" , salary_name)
        list_emp = salary_doc.applied_employee
        for emp in list_emp:
            if not emp.exclude:
                if emp.employee == doc.employee:
                    
                    salary = frappe.db.get_value("Employee" , doc.employee , "amount")
                    # frappe.msgprint(str( emp.percentage * salary))
                    amount = float(emp.percentage) * float(salary) / 100
                    if doc.net_pay :
                        if salary_doc.type == "Earning":
                            
                            doc.salary_descrease = 0
                            doc.salary_increase  = amount
                            doc.net_pay = doc.net_pay + float(amount)
                        else:
                            doc.salary_descrease = amount
                            doc.salary_increase  = 0
                            doc.net_pay = doc.net_pay - float(amount)