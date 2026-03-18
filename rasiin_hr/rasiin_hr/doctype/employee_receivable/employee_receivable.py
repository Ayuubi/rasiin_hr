# Copyright (c) 2024, Rasiin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeReceivable(Document):
	pass
@frappe.whitelist()
def create_return_through_additional_salary(doc):
	import json

	if isinstance(doc, str):
		doc = frappe._dict(json.loads(doc))

	additional_salary = frappe.new_doc("Additional Salary")
	additional_salary.employee = doc.employee
	# additional_salary.currency = doc.currency
	additional_salary.amount = doc.balance
	additional_salary.payroll_date = doc.date
	additional_salary.ref_doctype = doc.doctype
	additional_salary.ref_docname = doc.name

	return additional_salary