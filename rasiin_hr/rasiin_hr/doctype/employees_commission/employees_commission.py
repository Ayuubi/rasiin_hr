import frappe
from frappe.model.document import Document
from frappe.desk.query_report import run

class EmployeesCommission(Document):
	def on_submit(self):
		doc=self
		for i in self.commission_payments:
			if i.payment>0:
				additional_salary = frappe.new_doc("Additional Salary")
				additional_salary.employee = i.employee
				# additional_salary.currency = doc.currency
				additional_salary.amount = i.payment
				additional_salary.salary_component = self.component
				additional_salary.payroll_date = self.posting_date
				additional_salary.overwrite_salary_structure_amount=1
				additional_salary.custom_reference_document_type = "Employees Commission"
				additional_salary.custom_reference_document = self.name
				additional_salary.insert(ignore_permissions=True)
				additional_salary.submit()
@frappe.whitelist()
def employee_commision(from_date,to_date):
	company = frappe.defaults.get_global_default("company")
	report_gl = frappe.get_doc("Report", "Sales Partner Summary")
	report_gl_filters = {
		
		"company": company,
		

		"from_date": from_date,
		"to_date": to_date,
		"doctype": "Sales Invoice",
		"show_return_entries": 1
	   
	}
	   
	columns_gl, data_gl = report_gl.get_data(
		limit=1000, user="Administrator", filters=report_gl_filters, as_dict=True
	)
	# frappe.errprint(data_gl)
	result=[]
	for i in data_gl:
		if i.employee_ids != "Total":
			result.append({
				"employee": i.employee_ids,
				"employee_name": i.sales_partner,
				"amount": i.commission
			})
	return result


@frappe.whitelist()
def doctor_commision(from_date,to_date):
	company = frappe.defaults.get_global_default("company")
	report_gl = frappe.get_doc("Report", "Doctors Net Commission")
	report_gl_filters = {
		
		"company": company,
		"from_date": from_date,
		"to_date": to_date,
	   
	}
	   
	columns_gl, data_gl = report_gl.get_data(
		limit=1000, user="Administrator", filters=report_gl_filters, as_dict=True
	)
	frappe.errprint(data_gl)
	result=[]
	for i in data_gl:
		if i.employee_commisison != "Total":
			result.append({
				"employee": i.employee_commisison,
				"employee_name": i.ref_practitioner,
				"amount": i.net_commission
			})
	return result