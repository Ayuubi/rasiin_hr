# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data
def get_data(filters):
	volunteer = filters.get('volunteer')
	data = frappe.db.sql(f"""

		select 
		employee,
	
		employee_name ,
						
		department,
		designation,
		cell_number,
	
		
		amount

		from `tabEmployee`

		where volunteer = "{volunteer}"
	
	
	""" , as_dict = 1)


	return data 
def get_columns():
	columns = [
		{
			"label": _("ID"),
			"fieldtype": "Data",
			"fieldname": "employee",
			
			"width": 100,
		},
	
		{
			"label": _("Name"),
			"fieldtype": "Data",
			"fieldname": "employee_name",
			
			"width": 250,
		},
		
		
		# {
		# 	"label": _("Department"),
		# 	"fieldtype": "Data",
		# 	"fieldname": "department",
			
		# 	"width": 200,
		# },

		{
			"label": _("Designation"),
			"fieldtype": "Data",
			"fieldname": "designation",
			
			"width": 200,
		},

		{
			"label": _("Mobile"),
			"fieldtype": "Data",
			"fieldname": "cell_number",
			
			"width": 100,
		},

	


	

		{
			"label": _("Salary"),
			"fieldtype": "Currency",
			"fieldname": "amount",
			
			"width": 100,
		},


	
	
	]
	return columns
