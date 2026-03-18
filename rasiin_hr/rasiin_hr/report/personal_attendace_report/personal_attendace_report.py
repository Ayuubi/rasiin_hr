# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
from frappe import _
from datetime import timedelta, date
from frappe.utils import getdate
import collections
from rasiin_hr.rasiin_hr.report.attendace_report.attendace_report import get_personal_report


status_map = {
	"Present": "P",
	"Absent": "A",
	"Half Day": "HD",
	
	"On Leave": "L",
	"Holiday": "H"
	
}


def execute(filters=None):
	worked_on_holiday = filters.get('worked_on_holiday')
	holiday = {}
	if worked_on_holiday:
		
		holiday=	{
			"label": _("Holiday"),
			"fieldtype": "Data",
			"fieldname": "holiday",
			
			"width": 100,
		}

	columns, data = get_columns(), get_data(filters)
	message = get_message(filters) 
	if holiday:
		columns.insert(4 , holiday)
	return columns, data , message



def get_message(filters) -> str:
	key = 'status'
	grouped = collections.defaultdict(int)
	status_dt = {}
	for d in get_data(filters):
		# frappe.errprint(d)
		if "status" in d:
			grouped[d[key]] += 1

	for value, count in grouped.items():
		status_dt[value] = count
		print(value, count)

   

	message = ""
	colors = ["green", "red", "orange", "green", "#318AD8", "", ""]

	count = 0
	
	

	# frappe.errprint(status_dt)
	for status, abbr in status_map.items():
		sts = 0
		if status in status_dt:
			sts = status_dt[status]
		message += f"""
			<span style='border-left: 2px solid {colors[count]}; padding-right: 12px; padding-left: 5px; margin-right: 3px;'>
				
				{status} - {sts} 
			</span>
		"""
		count += 1

	return message



def daterange(start_date, end_date):
		for n in range(int ((end_date - start_date).days)+1):
			yield start_date + timedelta(n)



def get_data(filters):





	from_date ,to_date , employee  = filters.get('from_date'), filters.get('to_date') , filters.get('employee')
	worked_on_holiday = filters.get('worked_on_holiday')
	condition = ""

	per_data = []
	start_date = getdate(from_date)
	end_date = getdate(to_date)
	totals_in = {
			
			"early_in" : 0 ,
		
			"early_out" : 0,
			

		}
	if employee:
		for single_date in daterange(start_date, end_date):
			data = get_personal_report(single_date , employee)[0]
			totals = get_personal_report(single_date , employee)[1]
			# frappe.message(totals['total_earyl_in'] + totals['total_late_out'])
			totals_in['early_in'] += (abs(totals['total_earyl_in']) + abs(totals['total_late_out']))
			totals_in["early_out"] += (abs(totals['total_ealy_out']) + abs(totals["total_late_in"]))
			if data:
				per_data.append(data[0])
	per_data.append({})
	per_data.append({})
	per_data.append({})
	totals_ = {
			"employee_name" : "Total",
			"hourse" : "Total Early In and Late out" ,
			"early_in" : frappe.utils.format_duration(abs(totals_in["early_in"]) )  ,
			"late_in" : "Total Late In and Early out" ,
			"early_out" : frappe.utils.format_duration(abs(totals_in['early_out']) ) ,
			# "late_out" : frappe.utils.format_duration(abs(total_late_out)) 

		}
	per_data.append(totals_)
	return per_data
	# if worked_on_holiday:
	# 	condition += f'and worked_on_holiday = {worked_on_holiday}'
	# data = frappe.db.sql(f"""
	# 	select 
	# 	attendance_date,
	
	# 	employee_name ,
	# 	status ,
	# 	shift,
	# 	holiday,
	# 	in_time,
	# 	out_time,
	# 	in_time_string,
	# 	out_time_string ,
	# 	hourse ,
	# 	working_hours,
	# 	early_in,
	# 	late_in ,
	# 	early_out ,
	# 	late_out


	# 	from `tabAttendance`

	# 	where attendance_date between "{from_date}" and "{to_date}" 
	# 	and employee = "{employee}" {condition}
	
	
	# """ , as_dict = 1)

	# special_holida_data = frappe.db.sql(f"""
	# 	select 
	# 	attendance_date,
	
	# 	employee_name ,
	# 	status ,
	# 	shift, 
	# 	holiday,
	# 	in_time_string,
	# 	out_time_string ,
	# 	hourse ,

	# 	early_in,
	# 	late_in ,
	# 	early_out ,
	# 	late_out
		


	# 	from `tabSpecial Holiday Worked`

	# 	where attendance_date between "{from_date}" and "{to_date} " 
	# 	and employee = "{employee}"
	
	
	# """ , as_dict = 1)
	# for d in special_holida_data:
	# 	data.append(d)
	# def daterange(start_date, end_date):
	# 	for n in range(int ((end_date - start_date).days)+1):
	# 		yield start_date + timedelta(n)

	
	# holiday_atte_list = []
	# holiday_scheduled_list = []
	# # emp_list = frappe.db.get_all("Employee" , 
	
	# #   filters={
    # #     'status': 'Active'
    # # },
    # # fields=['name', 'employee_name'],
   
    # # page_length=1000,
	# #  )
	# # for emp in emp_list:
	# 	# frappe.errprint(d)
	# if  not worked_on_holiday:
	# 	if employee:
	# 		holiday_list_name = get_holiday_list_for_employee(employee, False)
	# 			# for single_date in daterange(start_date, end_date):
	# 			# 	print(single_date.strftime("%Y-%m-%d"))
	# 		# if holiday_list_name:	
	# 		for single_date in daterange(start_date, end_date):
	# 			special_holiday = frappe.db.get_value("Special Holiday" , {"from_date" : ["<=", getdate(single_date)] , "to_date" : [">=", getdate(single_date)]})
	# 			if 	special_holiday:
	# 				holiday_atte = {}
	# 				sp_h = frappe.get_doc("Special Holiday"  , special_holiday)
	# 				holiday = sp_h.holiday
	# 				holiday_atte['employee_name'] = frappe.db.get_value("Employee" , employee , "employee_name")
				
	# 				holiday_atte['status'] = f"<span class='bg-danger text-white'>{holiday}</span>"
	# 				holiday_atte['attendance_date']  = getdate(single_date)
					
	# 				holiday_atte_list.append(holiday_atte)
	# 			elif holiday_list_name:
	# 				if is_holiday(holiday_list_name, single_date):
	# 					holiday_atte = {}
	# 					# frappe.errprint(single_date)
	# 					# holiday_atte['employee'] = emp['name']
	# 					holiday_atte['employee_name'] = frappe.db.get_value("Employee" , employee , "employee_name")
	# 					holiday_atte['status'] = "Holiday"
	# 					holiday_atte['attendance_date']  = getdate(single_date)
						
	# 					holiday_atte_list.append(holiday_atte)
	# 			# frappe.errprint(holiday_atte_list)
	# 			# data.append({'employee' : d['employee_name']   , "status" : "Holiday"})
	# 	# # data = [{"employee" : "Home" , "name" : "full name" , "status" : 'Holiday'}]
			
	# 		holiday_scheduled = frappe.db.get_all("Employee Schedulling" , fields = ['shift','from_date'] , filters = {"employee" :  employee ,"shift" :"Free","from_date" : ("between", [from_date, to_date])})
	# 		# frappe.msgprint(str(to_date))
	# 		for hold_s in holiday_scheduled:
	# 			holiday_sc = {}
	# 			# frappe.errprint(single_date)
	# 			# holiday_atte['employee'] = emp['name']
	# 			holiday_sc['employee_name'] = frappe.db.get_value("Employee" , employee , "employee_name")
	# 			holiday_sc['status'] = "Holiday"
	# 			holiday_sc['attendance_date']  = getdate(hold_s.from_date)
	# 			holiday_sc['shift'] = frappe.db.get_value("Employee Schedulling" , {"employee" : employee ,"from_date" : frappe.utils.add_to_date(getdate(hold_s.from_date) , days = -1)} , "shift")
		
				
	# 			holiday_scheduled_list.append(holiday_sc)
	# 	for hold in holiday_atte_list:
	# 		search_dict = {'employee_name': hold['employee_name'], 'attendance_date': hold['attendance_date']}
	# 		found = any(all(item in d.items() for item in search_dict.items()) for d in data)
	# 		if found:
	# 			continue
			
	# 		data.append(hold)
		
	# 	for h in holiday_scheduled_list:
		
	# 		search_dict = {'employee_name': h['employee_name'], 'attendance_date': h['attendance_date']}
	# 		found = any(all(item in d.items() for item in search_dict.items()) for d in data)
	# 		if found:
				
	# 			continue
			
	# 		data.append(h)
		
	# data = sorted(data, key=lambda x: x['attendance_date'])


	# total_earyl_in= 0
	# total_late_out = 0
	# total_ealy_out = 0
	# total_late_in = 0
	# total_working_hourse = 0
	# late_early_list = []
	# # late_earl = {}
	# for d in data:
		
		
	# 	if 'working_hours' in d:
	# 		if d.working_hours:
	# 			total_working_hourse += d['working_hours']
	# 	if 'shift' in d:
	# 		# frappe.msgprint(str(d))
	# 		if d['shift']:
	# 			shift_start = frappe.db.get_value("Shift Type" , d['shift'] , "start_time")
	# 		if 'in_time' in d:
	# 			if d.in_time:
	# 				time_in = str(d['in_time'])
	# 				ts = time_in.split(" ")[1]
	# 				in_time = frappe.utils.to_timedelta(ts)
	# 				amout = frappe.utils.time_diff_in_seconds(ts, str(shift_start))
					

	# 				if in_time > shift_start:
						
						
	# 					total_late_in += abs(amout)
				
	# 				if in_time < shift_start:
	# 					total_earyl_in += abs(amout)
						
					
					
	# 				# late_earl['ealry_entry'] = 1
	# 		shift_end = frappe.db.get_value("Shift Type" , d['shift'] , "end_time")
	# 		if 'out_time' in d:
	# 			if d.out_time:
	# 				time_in = str(d['out_time'])
	# 				to_out = time_in.split(" ")[1]
	# 				ex_time_out = frappe.utils.to_timedelta(to_out)
	# 				# amout = frappe.utils.time_diff_in_seconds(ts, str(shift_start))
	# 				amout = frappe.utils.time_diff_in_seconds(to_out, str(shift_end))
	# 				# frappe.utils.time_diff_in_hours(ex_time_out, str(shift_end))
	# 				if ex_time_out > shift_end:
	# 					total_late_out += abs(amout)
	# 					# late_earl['late_out'] = 1
	# 				if ex_time_out < shift_end:
	# 					total_ealy_out += abs(amout)
		
	
	# 	# late_early_list.append(late_earl)
	
	# totals = {
	# 		"employee_name" : "Total",
	# 		"hourse" : frappe.utils.format_duration(abs(total_working_hourse * 3600) ) ,
	# 		"early_in" : frappe.utils.format_duration(abs(total_earyl_in) )  ,
	# 		"late_in" : frappe.utils.format_duration(abs(total_late_in) ) ,
	# 		"early_out" : frappe.utils.format_duration(abs(total_ealy_out) ) ,
	# 		"late_out" : frappe.utils.format_duration(abs(total_late_out) ) 

	# 	}
	
	# total_add = total_earyl_in + total_late_out
	# total_sub = total_ealy_out + total_ealy_out
	# totals_in = {
	# 		"employee_name" : "Total",
	# 		"hourse" : "Total Early In and Late out" ,
	# 		"early_in" : frappe.utils.format_duration(abs(total_earyl_in + total_late_out) )  ,
	# 		"late_in" : "Total Late In and Early out" ,
	# 		"early_out" : frappe.utils.format_duration(abs(total_ealy_out + total_ealy_out) ) ,
	# 		# "late_out" : frappe.utils.format_duration(abs(total_late_out)) 

	# 	}
	
	# data.append({})
	# data.append(totals)
	# data.append({})
	# data.append(totals_in)
	# return data




def get_columns():
	columns = [
		# employee,
		# employee_name ,
		# status ,
		# shift, 
		# in_time_string,
		# out_time_string ,
		# hourse ,

		# early_in,
		# late_in ,
		# early_out ,
		# late_out
			{
			"label": _("Date"),
			"fieldtype": "Date",
			"fieldname": "attendance_date",
			
			"width": 100,
		},
	
		{
			"label": _("Name"),
			"fieldtype": "Data",
			"fieldname": "employee_name",
			
			"width": 200,
		},
		{
			"label": _("Status"),
			"fieldtype": "Data",
			"fieldname": "status",
			
			"width": 80,
		},

			{
			"label": _("Shift"),
			"fieldtype": "Data",
			"fieldname": "shift",
			
			"width": 100,
		},
			{
			"label": _("Time In"),
			"fieldtype": "Data",
			"fieldname": "in_time_string",
			
			"width": 100,
		},
		# out_time_string ,
		# hourse ,

		# early_in,
		# late_in ,
		# early_out ,
		# late_out

		{
			"label": _("Time Out"),
			"fieldtype": "Data",
			"fieldname": "out_time_string",
			
			"width": 100,
		},

		{
			"label": _("W Hours"),
			"fieldtype": "Data",
			"fieldname": "hourse",
			
			"width": 100,
		},

		{
			"label": _("Early In"),
			"fieldtype": "Data",
			"fieldname": "early_in",
			
			"width": 100,
		},

		{
			"label": _("Late In"),
			"fieldtype": "Data",
			"fieldname": "late_in",
			
			"width": 100,
		},

		# early_out ,
		# late_out
			{
			"label": _("Early Out"),
			"fieldtype": "Data",
			"fieldname": "early_out",
			
			"width": 100,
		},

		{
			"label": _("Late Out"),
			"fieldtype": "Data",
			"fieldname": "late_out",
			
			"width": 100,
		},
	
	]
	return columns