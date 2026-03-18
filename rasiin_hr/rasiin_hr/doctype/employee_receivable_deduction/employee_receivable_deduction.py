# Copyright (c) 2025, Rasiin and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.utils import get_balance_on
from frappe.utils import today
from frappe.model.document import Document
from frappe.utils import today, get_first_day, get_last_day
from datetime import datetime

class EmployeeReceivableDeduction(Document):
	def on_submit(self):
		doc=self
		for i in self.employee_receivable_details:
			if i.payment>0:
				additional_salary = frappe.new_doc("Additional Salary")
				additional_salary.employee = i.employee
				# additional_salary.currency = doc.currency
				additional_salary.amount = i.payment
				additional_salary.salary_component = self.component
				additional_salary.payroll_date = self.posting_date
				additional_salary.overwrite_salary_structure_amount=1
				additional_salary.ref_doctype = "Employee Receivable Deduction"
				additional_salary.ref_docname = self.name
				additional_salary.insert(ignore_permissions=True)
				additional_salary.submit()
	
	def on_cancel(self):
		self.ignore_linked_doctypes = ["GL Entry", "Payment Ledger Entry"]
		# self.set_status(update=True)

@frappe.whitelist()
def get_employees_with_balances(employee=None, department=None, account=None):
	filters = {"status": "Active"}
	if employee:
		filters["name"] = employee   # Employee doctype uses "name", not "employee"
	if department:
		filters["department"] = department

	start_date = get_first_day(today())
	end_date = get_last_day(today())

	employees = frappe.get_all("Employee", filters=filters, fields=["name", "employee_name", "department"])

	result = []
	for emp in employees:
		balance = get_balance_on(
			party_type="Employee",
			party=emp.name,
			date=today(),
			account=account
		) or 0

		# latest/base salary (avoid None)
		salary = frappe.db.get_value(
			"Salary Structure Assignment",
			{"employee": emp.name, "docstatus": 1},
			"base",
			order_by="from_date desc"
		) or 0

		deduction = frappe.db.sql(
			"""
			SELECT COALESCE(SUM(amount), 0)
			FROM `tabAdditional Salary`
			WHERE employee = %s
			  AND type = 'Deduction'
			  AND docstatus = 1
			  AND (
					(is_recurring = 1
					 AND %s BETWEEN from_date AND COALESCE(to_date, %s))
				 OR
					(is_recurring = 0
					 AND payroll_date BETWEEN %s AND %s)
			  )
			""",
			(emp.name, today(), today(), start_date, end_date),
		)[0][0] or 0

		if balance > 0:
			result.append({
				"employee": emp.name,
				"employee_name": emp.employee_name,
				"department": emp.department,
				"salary": round(float(salary), 2),
				"deduction": round(float(deduction), 2),
				"amount": round(float(balance), 2),
			})

	return result


# @frappe.whitelist()
# def get_employees_with_balances(employee=None, department=None, account=None):
# 	filters = {}
# 	filters = {"status": "Active"}
# 	if employee:
# 		filters["employee"] = employee
# 	if department:
# 		filters["department"] = department

# 	start_date = get_first_day(today())
# 	end_date = get_last_day(today())
# 	employees = frappe.get_all("Employee", filters=filters, fields=["name", "employee_name", "department"])
	
# 	result = []
# 	for emp in employees:
# 		balance = get_balance_on(
# 			party_type="Employee",
# 			party=emp.name,
# 			date=today(),
# 			account = account
   
			
# 		)
# 		salary = frappe.db.get_value("Salary Structure Assignment", {"employee": emp.name},"base")
# 		# Sum of all approved *Additional Salary* deductions for this employee
# 				 # Sum of all approved *Additional Salary* deductions for the employee in the current month.
# 		#  - If the entry is **recurring** (is_recurring = 1), we check that *today* falls between
# 		#    the recurring window (`from_date` – `to_date`).
# 		#  - Otherwise we use the single `payroll_date` and restrict it to the current month window.
# 		#  - We use COALESCE to protect against NULL sums.
# 		deduction = frappe.db.sql(
# 			"""
# 			SELECT COALESCE(SUM(amount), 0)
# 			FROM `tabAdditional Salary`
# 			WHERE employee = %s
# 			  AND type = 'Deduction'
# 			  AND docstatus = 1
# 			  AND (
# 					-- recurring window check
# 					(is_recurring = 1
# 					 AND %s BETWEEN from_date AND COALESCE(to_date, %s))
# 				 OR -- single‑date entry inside current month
# 					(is_recurring = 0
# 					 AND payroll_date BETWEEN %s AND %s)
# 			  )
# 			""",
# 			(emp.name, today(), today(), start_date, end_date),
# 		)[0][0]
# 		if balance>0:
# 			result.append({
# 				"employee": emp.name,
# 				"employee_name": emp.employee_name,
# 				"department": emp.department,
#     			"salary": round(salary,2),
# 				"deduction": round(deduction, 2),
# 				"amount": round(balance,2) or 0
# 			})

# 	return result
