# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
from frappe import _
from datetime import timedelta, date
from frappe.utils import getdate
def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_cities(filters):
    employee = filters.get("employee")
   

    employee_name = frappe.db.sql_list(
        """
        SELECT employee_name
        FROM `tabEmployee`
        WHERE employee=%s
        """,
        employee
    )

    return employee_name

def get_data(filters):
	from_date ,to_date = filters.get('from_date'), filters.get('to_date')
	data = frappe.db.sql(f"""
		select 
	
	
		employee_name ,
		net_pay ,
		bank_account_no,
		mobile
	


		from `tabSalary Slip`

		where start_date between "{from_date}" and "{to_date}" 
	
	
	""" , as_dict = 1)


	
	return data
def get_columns():
	columns = [
	
	
		{
			"label": _("Name"),
			"fieldtype": "Data",
			"fieldname": "employee_name",
			
			"width": 200,
		},
		{
			"label": _("Amount"),
			"fieldtype": "Currency",
			"fieldname": "net_pay",
			
			"width": 180,
		},

			{
			"label": _("Account"),
			"fieldtype": "Data",
			"fieldname": "bank_account_no",
			
			"width": 200,
		},
			{
			"label": _("Tell"),
			"fieldtype": "Data",
			"fieldname": "mobile",
			
			"width": 200,
		},
		# out_time_string ,
		# hourse ,

		# early_in,
		# late_in ,
		# early_out ,
		# late_out

		


	
	
	]
	return columns