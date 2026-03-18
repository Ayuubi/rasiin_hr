import itertools
from datetime import datetime, timedelta

import frappe
from frappe.model.document import Document
from frappe.utils import cint, get_datetime, get_time, getdate

from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import daterange
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday

from hrms.hr.doctype.attendance.attendance import mark_attendance
from hrms.hr.doctype.employee_checkin.employee_checkin import (
	calculate_working_hours,
	mark_attendance_and_link_log,
)
from hrms.hr.doctype.shift_assignment.shift_assignment import get_employee_shift, get_shift_details

from hrms.hr.doctype.shift_type.shift_type import ShiftType
class CustomShiftType(ShiftType):
	@frappe.whitelist()
	def process_auto_attendance(self):
		
		if (
			not cint(self.enable_auto_attendance)
			or not self.process_attendance_after
			or not self.last_sync_of_checkin
		):
			return

		filters = {
			"skip_auto_attendance": 0,
			"attendance": ("is", "not set"),
			"time": (">=", self.process_attendance_after),
			"shift_actual_end": ("<", self.last_sync_of_checkin),
			"shift": self.name,
		}
		logs = frappe.db.get_list(
			"Employee Checkin", fields="*", filters=filters, order_by="employee,time"
		)

		for key, group in itertools.groupby(
			logs, key=lambda x: (x["employee"], x["shift_actual_start"])
		):
			single_shift_logs = list(group)
			(
				attendance_status,
				working_hours,
				late_entry,
				early_exit,
				in_time,
				out_time,
			) = self.get_attendance(single_shift_logs)

			mark_attendance_and_link_log(
				single_shift_logs,
				attendance_status,
				key[1].date(),
				working_hours,
				late_entry,
				early_exit,
				in_time,
				out_time,
				self.name,
			)
		for date in daterange(getdate(self.process_attendance_after), frappe.utils.add_to_date(getdate() , days = -1)):

			for employee in self.get_assigned_employee(date, True):
				# frappe.msgprint(str(employee))
				em_status = frappe.db.get_value("Employee" , employee , "status")
				if em_status == "Active" : 
					self.mark_absent_for_dates_with_no_attendance(employee)

	def mark_absent_for_dates_with_no_attendance(self, employee):
		
			# frappe.errprint("in this place")
			"""Marks Absents for the given employee on working days in this shift which have no attendance marked.
			The Absent is marked starting from 'process_attendance_after' or employee creation date.
			"""
			start_date, end_date = self.get_start_and_end_dates(employee)
			# frappe.msgprint(str(start_date))

			# no shift assignment found, no need to process absent attendance records
			if start_date is None:
				return
			
			holiday_list_name = self.holiday_list
			if not holiday_list_name:
				holiday_list_name = get_holiday_list_for_employee(employee, False)

			start_time = get_time(self.start_time)

			for date in daterange(getdate(start_date), getdate(end_date)):
				yes_dat = frappe.utils.add_to_date(date , days = -1)
				yester_atte = frappe.db.exists("Attendance" , {"employee" : employee , "attendance_date" : yes_dat})
				if is_holiday(holiday_list_name, date):
					# skip marking absent on a holiday
					continue
				if self.day_off and yester_atte:
					# frappe.errprint(date)
					continue
				if frappe.db.exists("Attendance" , {"employee" : employee , "attendance_date" : getdate(date)}):
					continue
				special_holiday = frappe.db.get_value("Special Holiday" , {"from_date" : ["<=", getdate(date)] , "to_date" : [">=", getdate(date)]})
				if special_holiday:
					continue
				timestamp = datetime.combine(date, start_time)
				shift_details = get_employee_shift(employee, timestamp, True)
				# frappe.errprint(shift_details)
				# if shift_details and shift_details.shift_type.name == self.name:
				
				free_schedule = frappe.db.get_value("Employee Schedulling" , {"employee" : employee , "from_date" : date , "shift" : "Free"} , "shift")
				sc_shift = frappe.db.get_value("Employee Schedulling" , {"employee" : employee , "from_date" : date} , "shift")
				shift = ''
				if sc_shift:
					shift = sc_shift
				if not shift:
					shift = sc_shift = frappe.db.get_value("Employee Schedulling" , {"employee" : employee , "from_date" :frappe.utils.add_to_date(date , days = 1)} , "shift")
				
				
				if shift  and shift != "Free":
					
					self.name = shift
				# if exists contineu
				if not shift:
					shift = frappe.db.get_value("Employee" ,employee , "default_shift" )
				
				if free_schedule:
					# frappe.msgprint(employee)
					# attendance = mark_attendance(employee, date, "On Leave", free_schedule)
					# frappe.errprint(attendance)
					continue
				else:
					# frappe.msgprint(employee)
					attendance = mark_attendance(employee, date, "Absent" , shift = shift)
					# frappe.errprint(attendance)
				
				
					if attendance:
						frappe.get_doc(
							{
								"doctype": "Comment",
								"comment_type": "Comment",
								"reference_doctype": "Attendance",
								"reference_name": attendance,
								"content": frappe._("Employee was marked Absent due to missing Employee Checkins."),
							}
						).insert(ignore_permissions=True)
	
	
	def get_assigned_employee(self, from_date=None, consider_default_shift=True):
		filters = {"shift": self.name}
		if from_date:
			filters["from_date"] =  from_date

		assigned_employees = frappe.get_all("Employee Schedulling", filters=filters, pluck="employee")

		if consider_default_shift:
			
			filters = {"default_shift": self.name, "status":  "Active" , "volunteer": ["!=", 1]}
			default_shift_employees = frappe.get_all("Employee", filters=filters, pluck="name")

			return list(set(assigned_employees + default_shift_employees))
		return assigned_employees


	def get_start_and_end_dates(self, employee):
		"""Returns start and end dates for checking attendance and marking absent
		return: start date = max of `process_attendance_after` and DOJ
		return: end date = min of shift before `last_sync_of_checkin` and Relieving Date
		"""
		date_of_joining, relieving_date, employee_creation = frappe.db.get_value(
			"Employee", employee, ["date_of_joining", "relieving_date", "creation"]
		)

		if not date_of_joining:
			date_of_joining = employee_creation.date()

		start_date = max(getdate(self.process_attendance_after), date_of_joining)
		end_date = None

		shift_details = get_shift_details(self.name, get_datetime(self.last_sync_of_checkin))
		last_shift_time = (
			shift_details.actual_start if shift_details else get_datetime(self.last_sync_of_checkin)
		)
		end_date = frappe.utils.add_to_date(getdate() , days = -1)

		# check if shift is found for 1 day before the last sync of checkin
		# absentees are auto-marked 1 day after the shift to wait for any manual attendance records
		# prev_shift = get_employee_shift(employee, last_shift_time - timedelta(days=1), True, "reverse")
		# if prev_shift:
		# 	end_date = (
		# 		min(prev_shift.start_datetime.date(), relieving_date)
		# 		if relieving_date
		# 		else prev_shift.start_datetime.date()
		# 	)
		# else:
		# 	# no shift found
		# 	return None, None
		return start_date, end_date
