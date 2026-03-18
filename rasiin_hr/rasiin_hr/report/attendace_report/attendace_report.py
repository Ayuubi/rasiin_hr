# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
from frappe import _
from datetime import timedelta, date
from frappe.utils import getdate
from datetime import datetime, time 
from dateutil.relativedelta import relativedelta
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday

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
	att_che = sorted(get_em_checking(filters)[0], key=lambda x: x["status"] , reverse=True)
	columns, data = get_columns(), att_che
	if holiday:
		columns.insert(4 , holiday)
	return columns, data



def is_time_between(start_time, end_time, check_time):
    # Convert the time strings to time objects
    start_time = datetime.strptime(start_time, "%H:%M").time()
    end_time = datetime.strptime(end_time, "%H:%M").time()
    check_time = datetime.strptime(check_time, "%H:%M").time()

    # Check if the check_time is between start_time and end_time
    if start_time <= check_time <= end_time:
        return True
    else:
        return False


def get_em_checking(filters , emp = None):
	from_date ,to_date , worked_on_holiday = filters.get('from_date'), filters.get('to_date') , filters.get('worked_on_holiday')
	roles = frappe.get_roles(frappe.session.user)
	# check_logs = frappe.db.get_list("Employee Checkin" , filters = [['date', 'between', [from_date, to_date] ]], fields = ['employee' , 'time' , 'employee_name'] )
	first_log = ''
	last_log = ''
	emp_log = []
	emp_list = frappe.db.get_list("Employee" , filters = {'status' : 'Active'}, fields = ['employee' ,  'employee_name'] )
	if emp:
		emp_list = [{"employee":emp , "employee_name" : frappe.db.get_value("Employee" , emp , "employee_name")}]
	late_out_min = 0
	early_out_min =0
	late_in_min = 0
	early_in_min = 0
	for em in emp_list:
	
		# to_date = from_date
		check_out = -1
		check_in = 0
		
		em_id = em['employee']
		

		shift = ''
		check_logs = ''
		time_out_str = ""
		time_in_str = ""
		time_out = ""
		time_in = ""
		pre_che = []
		# if pre_shift == "Free":
		# pre_shift = frappe.db.get_value("Employee Schedulling" , {"employee": em_id, "from_date":  frappe.utils.add_to_date(getdate(from_date) , days = -1)} ,"shift")

		assigned_shift = frappe.db.get_value("Employee Schedulling" , {"employee":em_id , "from_date":  frappe.utils.getdate(from_date)} ,"shift")
		
		if assigned_shift:
			shift = assigned_shift
		else:
			shift = frappe.db.get_value('Employee',   em_id , 'default_shift')
		# if shift == "Free":
		# 	shift_date =  frappe.utils.add_to_date(getdate(from_date) , days = -1)
		# 	shift = frappe.db.get_value("Employee Schedulling" , {"employee":em_id , "from_date":  frappe.utils.getdate(shift_date)} ,"shift")
		

		if shift :
			check_logs = frappe.db.sql(f"""

				select * from `tabEmployee Checkin` 
				where employee = '{em_id}' and CONVERT(time  , DATE) = '{from_date}' order by time

			""", as_dict = 1)
		

			che_shift = frappe.get_doc("Shift Type" , shift)
			
			if che_shift.two_date_shift:
				to_date =  frappe.utils.add_to_date(getdate(from_date) , days = 1)
				
				check_out = 0
				check_in = -1
			
				check_logs = frappe.db.sql(f"""
				
					select * from `tabEmployee Checkin` 
					where employee = '{em_id}' and CONVERT(time  , DATE) = '{to_date}' order by time

				""", as_dict = 1)
				pre_che = frappe.db.sql(f"""

				select * from `tabEmployee Checkin` 
				where employee = '{em_id}' and CONVERT(time  , DATE) = '{from_date}' order by time

			""" , as_dict = 1)
			

				# frappe.errprint(check_logs)
		# for log in check_logs:

			
			if check_logs:
			
				time_in = check_logs[0]['time']
				time_out = check_logs[check_out]['time']
				

				



			if pre_che:
				time_in = pre_che[-1]['time']
			frappe.errprint(time_out)
			frappe.errprint(time_in)
			if (check_logs or pre_che) and che_shift.name != "Free":
				if not check_logs:
					check_logs = pre_che
				if time_in:
					time_in_str = str(time_in)
					time_in_str = time_in_str.split(" ")[1]
				if time_out:
					time_out_str = str(time_out).split(" ")[1]	
				time_in_time_out_diff = 0
				if time_in and time_out:
					time_in_time_out_diff = abs(frappe.utils.time_diff_in_hours(str(time_in), str(time_out)))
				if time_in_time_out_diff < 2:
					time_out_str = ""
					time_out = ""
				if time_out_str or time_in_str:
					
					# if not che_shift.two_date_shift:
					# st = che_shift.start_time
					# st = "08:00:00"
					# start_time = datetime.strptime(str(st), "%H:%M:%S")
					# shift_str = start_time + timedelta(hours=3)
					# shift_end = start_time + timedelta(hours=-3)
					shift_str = "05:00"
					shift_end = "10:00"
				# if time_in_str:

					check_time_out = time_out_str[:-3]
					check_time_in = time_in_str[:-3]
					# frappe.msgprint(check_time_out)
					if  time_out_str and che_shift.two_date_shift:
					
						if not is_time_between(shift_str , shift_end , check_time_out) :
							
							time_out_str = ""
							time_out = ""
						# else:
					if check_time_in and che_shift.two_date_shift:
						if  is_time_between(shift_str , shift_end , check_time_in) :
							time_in_str = ""
							time_in = ""
					# if pre_che and check_in and che_shift.day_off:
					# 	time_in_str = ""
					# if check_logs and pre_che:
					# 	if check_logs[check_in]['time'] == pre_che[check_out]['time']:
					# 		time_in_str = ""
					if time_in_str and not  che_shift.two_date_shift and not che_shift.name != "Canteen":
						check_time_in = time_in_str[:-3]
						if not is_time_between(shift_str , shift_end , check_time_in) :
							time_out_str =  time_in_str
							time_out = time_in
							time_in = ""
							time_in_str = ""
				status = "Present"
				pre_hour = ""
				late_out = ""
				early_out =""
				late_in = ""
				early_in = ""

				

				

				if getdate(from_date) != getdate():
					if (not time_in_str) ^  (not time_out_str):
						status = "Half Day"
					if time_in and time_out:
						# working_hours = frappe.utils.time_diff_in_hours( , attend.in_time)
						hours = frappe.utils.time_diff_in_seconds(time_out , time_in)
						pre_hour = frappe.utils.format_duration(hours , hide_days=True) # '11d 13h 46m 40s'
				if time_out_str:
					o_time = frappe.utils.to_timedelta(time_out_str)
					early = frappe.utils.time_diff_in_seconds(che_shift.end_time , o_time)
					
					early_min = float(early)
					
					if o_time > che_shift.end_time:
						late_out =frappe.utils.format_duration(abs(early) , hide_days=True)
						late_out_min = early_min
					if o_time < che_shift.end_time:
						early_out =frappe.utils.format_duration(abs(early) , hide_days=True)
						early_out_min = early_min
				if time_in_str:
					in_time = frappe.utils.to_timedelta(time_in_str)
					late = frappe.utils.time_diff_in_seconds(in_time,che_shift.start_time )
					late_min = float(late)
				
				
					if in_time >che_shift.start_time:
						late_in = frappe.utils.format_duration(abs(late) , hide_days=True)
						late_in_min = late_min
					if  in_time < che_shift.start_time:
						early_in = frappe.utils.format_duration(abs(late) , hide_days=True)
						early_in_min = late_min
				if time_in_str or time_out_str:
					if che_shift.name == "Night Shift":
						ni_start = "15:00"
						ni_end = "21:00"
						if from_date != getdate():
							if not is_time_between(ni_start , ni_end , check_time_in) :
								status = "Absent"
							


					emp_log.append(

					{
					"employee_name"  : check_logs[0]['employee_name'] ,
					'department'  : frappe.db.get_value("Employee" , em_id , 'department'),
					'shift' : che_shift.name	,		# absent['status'] = "<span class='bg-danger text-white'>Absent</span>"
					'attendance_date' : from_date,
					"status" : status,
					"in_time_string" : time_in_str,
					
					"out_time_string" : time_out_str,
					
					'in_time' : time_in,
					'out_time' : time_out,
					"hourse"  : pre_hour,

					"early_in" : early_in,
					"late_in" : late_in,
					"early_out" :  early_out ,
					"late_out" : late_out,

			
					}
				)
					if em_id == "HR-EMP-00034":
						frappe.errprint(str(emp_log))

				else: 
					

					emp_log.append(

					{
					"employee_name"  : check_logs[0]['employee_name'] ,
					'department'  : frappe.db.get_value("Employee" , em_id , 'department'),
					'shift' : che_shift.name	,		# absent['status'] = "<span class='bg-danger text-white'>Absent</span>"
					'attendance_date' : from_date,
					"status" : "",
					"in_time_string" : time_in_str,
					
					"out_time_string" : time_out_str,
					
					'in_time' : time_in,
					'out_time' : time_out,
					"hourse"  : pre_hour,

					"early_in" : early_in,
					"late_in" : late_in,
					"early_out" :  early_out ,
					"late_out" : late_out,

			
					}
				)
					


			else:
				status = ""
				holiday_list_name = get_holiday_list_for_employee(em_id, False)
				em_st = frappe.db.get_value("Employee" , em_id , 'status')
				em_type = frappe.db.get_value("Employee" , em_id , 'employment_type')
				if che_shift.name == "Free" or (che_shift.enable_auto_attendance and em_st == "Active" and em_type != "Intern"):
					status = ""
					if getdate(from_date) != getdate() and che_shift.name != "Free":
						status = "Absent"
					if is_holiday(holiday_list_name, from_date):
						status = "Holiday"
						sh_shif = frappe.db.get_value("Employee Schedulling" , {"employee" :  em_id ,"from_date" : getdate(from_date) } , "shift")
						if sh_shif and sh_shif != "Free":
							status = "Absent"

		
						
					if che_shift.name == "Free":
						status = "Holiday"
					
			
					leaves = frappe.db.get_list("Leaves Assigment" , {"employee":em_id, "from_date": ("<=", from_date ) , "to_date": (">=", from_date )})
					
					if leaves:
						status = "On Leave"
					tr_ev = frappe.db.get_value("Training Event" , {"location_type" : "External" , "start_date" : ["<=", getdate(from_date)], "last" : [">=", getdate(from_date)]} , "name")
					# employees= tr_ev.employees
					if tr_ev:
						tr_ev_doc = frappe.get_doc("Training Event" , tr_ev)
						
						for emp in tr_ev_doc.employees:
							if emp.employee == em_id and emp.attendance == "Present":
								# frappe.errprint(em_id)
								emp_log.append(

								{
									"employee_name"  : em['employee_name'] ,
									'department'  : frappe.db.get_value("Employee" , em_id , 'department'),
									'shift' : "Training"	,		# absent['status'] = "<span class='bg-danger text-white'>Absent</span>"
									'attendance_date' : from_date,
									"status" : "Present",
									# "in_time_string" : time_in_str,
									
									# "out_time_string" : time_out_str
									}
								)
	
							
						
				search_dict = {'employee_name': em['employee_name'], 'attendance_date': from_date}
				found = any(all(item in d.items() for item in search_dict.items()) for d in emp_log)
				if not found:
					# continue
			
					emp_log.append(

						{
						"employee_name"  : em['employee_name'] ,
						'department'  : frappe.db.get_value("Employee" , em_id , 'department'),
						'shift' : che_shift.name	,		# absent['status'] = "<span class='bg-danger text-white'>Absent</span>"
						'attendance_date' : from_date,
						"status" : status,
						# "in_time_string" : time_in_str,
						
						# "out_time_string" : time_out_str
						}
					)
	
	totals = {
	"total_earyl_in": early_in_min,
	"total_late_out" : late_out_min,
	"total_ealy_out" : early_out_min,
	"total_late_in" : late_in_min,
		}
	
	return emp_log , totals


def get_personal_report(from_date , emp):
	filters = {
		"from_date" : from_date ,
		"to_date" : from_date
	}
	return get_em_checking(filters , emp)

def get_data(filters):
	

			
	from_date ,to_date , worked_on_holiday = getdate(filters.get('from_date')), getdate(filters.get('to_date')) , filters.get('worked_on_holiday')
	roles = frappe.get_roles(frappe.session.user)
	# frappe.errprint(roles)
	condition = ''
	if 'Medical Director' in roles and frappe.session.user != "Administrator":
		condition = 'and department = "Medical Department - RS"'
	if "HR Manager" not in roles and 'Medical Director' not in roles:
		condition = 'and department = "No Depart - RS'
	if worked_on_holiday:
		condition += f'and worked_on_holiday = {worked_on_holiday}'
	data = frappe.db.sql(f"""
		select 
		attendance_date,
	
		employee_name ,
		mobile , 
		department,
		status ,
		shift, 
		holiday,
		in_time_string,
		out_time_string ,
		hourse ,

		early_in,
		late_in ,
		early_out ,
		late_out
		


		from `tabAttendance`

		where attendance_date between "{from_date}" and "{to_date} " {condition}
	
	
	""" , as_dict = 1)

	special_holida_data = frappe.db.sql(f"""
		select 
		attendance_date,
	
		employee_name ,
		status ,
		shift, 
		holiday,
		in_time_string,
		out_time_string ,
		hourse ,

		early_in,
		late_in ,
		early_out ,
		late_out
		


		from `tabSpecial Holiday Worked`

		where attendance_date between "{from_date}" and "{to_date} " 
	
	
	""" , as_dict = 1)
	for d in special_holida_data:
		data.append(d)
	def daterange(start_date, end_date):
		for n in range(int ((end_date - start_date).days)+1):
			yield start_date + timedelta(n)

	start_date = getdate(from_date)
	end_date = getdate(to_date)
	
	holiday_atte_list = []
	holiday_scheduled_list = []
	emp_list = frappe.db.get_all("Employee" , 
	
	  filters={
        'status': 'Active'
    },
    fields=['name', 'employee_name','employee'],
   
    page_length=1000,
	 )
	if  not worked_on_holiday:
		for emp in emp_list:
			# frappe.errprint(d)
			holiday_list_name = get_holiday_list_for_employee(emp['name'], False)
			# for single_date in daterange(start_date, end_date):
			# 	print(single_date.strftime("%Y-%m-%d"))
			
			for single_date in daterange(start_date, end_date):
				special_holiday = frappe.db.get_value("Special Holiday" , {"from_date" : ["<=", getdate(single_date)] , "to_date" : [">=", getdate(single_date)]})
				if 	special_holiday:
					holiday_atte = {}
					sp_h = frappe.get_doc("Special Holiday"  , special_holiday)
					holiday = sp_h.holiday
					holiday_atte['employee_name'] = emp['employee_name']
					holiday_atte['status'] = f"<span class='bg-danger text-white'>{holiday}</span>"
					holiday_atte['attendance_date']  = getdate(single_date)
					
					holiday_atte_list.append(holiday_atte)
					
				elif is_holiday(holiday_list_name, single_date):
					holiday_atte = {}
					# frappe.errprint(single_date)
					# holiday_atte['employee'] = emp['name']
					holiday_atte['employee_name'] = emp['employee_name']
					holiday_atte['status'] = "<span class='bg-danger text-white'>Holiday</span>"
					holiday_atte['attendance_date']  = getdate(single_date)
					
					holiday_atte_list.append(holiday_atte)
					# frappe.errprint(holiday_atte_list)
					# data.append({'employee' : d['employee_name']   , "status" : "Holiday"})
		# # data = [{"employee" : "Home" , "name" : "full name" , "status" : 'Holiday'}]
		
			holiday_scheduled = frappe.db.get_all("Employee Schedulling" , fields = ['shift','from_date'] , filters = {"employee" :  emp['employee'] ,"shift" :"Free","from_date" : ("between", [from_date, to_date])})
			# frappe.msgprint(str(to_date))
			for hold_s in holiday_scheduled:
				holiday_sc = {}
				# frappe.errprint(single_date)
				# holiday_atte['employee'] = emp['name']
				holiday_sc['employee_name'] = emp['employee_name']
				holiday_sc['status'] = "<span class='bg-danger text-white'>Holiday</span>"
				holiday_sc['attendance_date']  = getdate(hold_s.from_date)
				holiday_sc['shift'] = frappe.db.get_value("Employee Schedulling" , {"employee" :  emp['employee'] ,"from_date" : frappe.utils.add_to_date(getdate(hold_s.from_date) , days = -1)} , "shift")
		
				
				holiday_scheduled_list.append(holiday_sc)
		for hold in holiday_atte_list:
			search_dict = {'employee_name': hold['employee_name'], 'attendance_date': hold['attendance_date']}
			found = any(all(item in d.items() for item in search_dict.items()) for d in data)
			if found:
				continue
			
			data.append(hold)
		
		for h in holiday_scheduled_list:
		
			search_dict = {'employee_name': h['employee_name'], 'attendance_date': h['attendance_date']}
			found = any(all(item in d.items() for item in search_dict.items()) for d in data)
			if found:
				continue
			data.append(h)
	
	
	all_emp = frappe.db.get_list('Employee',
		filters={
			'status': 'Active'
		},
		fields=['name', 'employee_name' , 'default_shift' , 'department'],
		
		page_length=1000,
	
	)
	em_to_mark_atte = []
	for em in all_emp:
		if not em.default_shift or frappe.db.get_value("Shift Type" , em.default_shift , "enable_auto_attendance"):
			absent = {}
			# frappe.errprint(single_date)
			# holiday_atte['employee'] = emp['name']
			absent['employee_name'] = em['employee_name']
			absent['department'] = em['department']
			absent['shift'] = frappe.db.get_value("Employee Schedulling" , {'from_date' :getdate(to_date) , 'employee' : em['name'] } , 'shift') or em['default_shift']
			# absent['status'] = "<span class='bg-danger text-white'>Absent</span>"
			absent['attendance_date']  = getdate(to_date)
					
			em_to_mark_atte.append(absent)
	for a in em_to_mark_atte:
		
			search_dict = {'employee_name': a['employee_name'], 'attendance_date': a['attendance_date']}
			found = any(all(item in d.items() for item in search_dict.items()) for d in data)
			if found:
				continue
			data.append(a)
	data = sorted(data, key=lambda x: x['attendance_date'])

	return data 
def get_columns():
	columns = [
	
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
			"label": _("Department"),
			"fieldtype": "Data",
			"fieldname": "department",
			
			"width": 200,
		},
		{
			"label": _("Status"),
			"fieldtype": "Data",
			"fieldname": "status",
			
			"width": 180,
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
