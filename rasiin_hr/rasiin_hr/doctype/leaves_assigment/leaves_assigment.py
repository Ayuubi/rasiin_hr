# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeavesAssigment(Document):
	def after_insert(self):
		message = f""""
			<b> {self.suppervisor_name} </b> is Requesting <b>{self.leave_type}</b> For <b>{self.employee_name}</b> From <b>{self.from_date}</b> To <b>{self.to_date}</b>"""
		notif = frappe.get_doc({
			"doctype" : "Nofication",
			"date" : frappe.utils.getdate(),
			"time" : frappe.utils.now(),
			"message" : message,
			# "for" : 1,
			# "user" : 
			
			"ref_doctype" : self.doctype,
			"ref_doc" : self.name

		})
		notif.insert()
		self.notication = notif.name
		self.save()

	def on_submit(self):
		if self.notication and self.status != "Rejected":
			not_doc = frappe.get_doc("Nofication" , self.notication)
			not_doc.seen = 1
			not_doc.save()
		if self.status != "Rejected":
			self.status = "Approved"
		if self.status == "Rejected":
			if self.notication:
				not_doc = frappe.get_doc("Nofication" , self.notication)
				not_doc.message = f"Leave Request for Employee <b>{self.employee_name}</b> Rejeted by <b>{frappe.session.user}</b> "
				not_doc.save()
			
			# frappe.msgprint("Sumbitted not")

	def get_last_leave(self, doc,docname):
		leave_assignment = frappe.get_all(
		
			filters={'employee': self.employee},
			fields=['leave_type', 'to_date'],
			order_by='creation DESC',
			limit=1
									
			)

		if leave_assignment:
			last_leave = leave_assignment[0]
			leave_type = last_leave.get('leave_type')
			to_date = last_leave.get('to_date')
		else:
			leave_type = None
			to_date = None

		return {
			'leave_type': leave_type,
			'to_date': to_date
		}

@frappe.whitelist()
def get_last_leave(doc,docname):
	# leave = frappe.db.get_value(doc, filters={'employee': docname},
	#                             fieldname='to_date', order_by='creation DESC', as_dict=True)

	
	# return leave.get('to_date') if leave else 1
	# leave = frappe.db.get_value('Leaves Assignment',
	#                         filters={'employee': docname},
	#                         fieldname=['leave_type', 'to_date'],
	#                         order_by='creation DESC',
	#                         as_dict=True)

	# leave_info = {
	#     'leave_type': leave.get('leave_type') if leave else 0,
	#     'to_date': leave.get('to_date') if leave else 0
	# }

	# return leave_info.leave_type and leave_info.to_date if leave_info else 1 

	leave_assignment = frappe.get_all(doc,
								filters={'employee': docname},
								fields=['leave_type', 'to_date'],
								order_by='creation DESC',
								limit=1)

	if leave_assignment:
		last_leave = leave_assignment[0]
		leave_type = last_leave.get('leave_type')
		to_date = last_leave.get('to_date')
	else:
		leave_type = None
		to_date = None
	if leave_type:
		return {
			'leave_type': leave_type,
			'to_date': to_date
		}
	else:
		return None



