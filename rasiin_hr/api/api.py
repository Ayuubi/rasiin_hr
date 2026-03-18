import frappe
import json
from frappe.utils.pdf import get_pdf
from frappe.utils import getdate
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
@frappe.whitelist()
def get_print_html(data ,days , daynames , curMonth , month_number , designation) :

	report_html_data = frappe.render_template(
		"rasiin_hr/templates/report/emp_schedule.html",
		{
			"data": json.loads(data),
			"days" : json.loads(days),
			"daynames" : json.loads(daynames),
			"curMonth" : curMonth,
			"month_number" : month_number,
			"designation" : json.loads(designation)

		  
		  
		},
	)
	# pdf_content = get_pdf(report_html_data)
	# file_doc = frappe.get_doc({
	# 'doctype': 'File',
	# 'file_name': 'MyPDF3.pdf',
   
	
	# 'file_url': '',
	# 'file_size': len(pdf_content),
	# 'content': pdf_content
	# })
	# file_doc.save()
	# frappe.db.commit()
	

	return report_html_data


@frappe.whitelist()
def get_print_html_weaky(data ,days , daynames , curMonth , month_number , designation) :

	report_html_data = frappe.render_template(
		"rasiin_hr/templates/report/emp_schedule_weakly.html",
		{
			"data": json.loads(data),
			"days" : json.loads(days),
			"daynames" : json.loads(daynames),
			"curMonth" : curMonth,
			"month_number" : month_number,
			"designation" : json.loads(designation)

		  
		  
		},
	)
	# pdf_content = get_pdf(report_html_data)
	# file_doc = frappe.get_doc({
	# 'doctype': 'File',
	# 'file_name': 'MyPDF3.pdf',
   
	
	# 'file_url': '',
	# 'file_size': len(pdf_content),
	# 'content': pdf_content
	# })
	# file_doc.save()
	# frappe.db.commit()
	

	return report_html_data
0
@frappe.whitelist()
def create_attendance(doc , mothod  = None):
	
	try:
		pre_shift = frappe.db.get_value("Employee Schedulling" , {"employee":doc.employee , "from_date":  frappe.utils.add_to_date(frappe.utils.getdate(doc.time) , days = -1)} ,"shift")
		shift = ''
		if pre_shift == "Free":
			pre_shift = frappe.db.get_value("Employee Schedulling" , {"employee":doc.employee , "from_date":  frappe.utils.add_to_date(frappe.utils.getdate(doc.time) , days = -2)} ,"shift")

		assigned_shift = frappe.db.get_value("Employee Schedulling" , {"employee":doc.employee , "from_date":  frappe.utils.getdate(doc.time)} ,"shift")
		if assigned_shift:
			shift = assigned_shift
		else:
			shift = frappe.db.get_value('Employee',   doc.employee , 'default_shift')
		doc.date = frappe.utils.getdate(doc.time)
		if not shift:
			shift = frappe.db.get_value("Employee Schedulling" , {"employee":doc.employee , "from_date":  frappe.utils.add_to_date(frappe.utils.getdate(doc.time) , days = 1)} ,"shift")
		
		if shift:
			two_date_shift = frappe.db.get_value("Shift Type" , shift , "two_date_shift")	
			
			# if  doc.date != "":
				# previous = frappe.db.exists("Employee Checkin", {"employee": doc.employee ,"date" : doc.date , 'log_type' : 'IN'}  )
			if two_date_shift:
				# if doc.date != frappe.utils.getdate(): 
				pre_date = frappe.utils.add_to_date(doc.date, days=-1, as_string=True)
				
				doc.date = pre_date
			if shift == "Free":
				is_pre_sh_two_date = frappe.db.get_value("Shift Type" , pre_shift , "two_date_shift")
				if is_pre_sh_two_date:
				# if doc.date != frappe.utils.getdate(): 
					pre_date = frappe.utils.add_to_date(doc.date, days=-1, as_string=True)
					
					doc.date = pre_date
					shift = pre_shift
			doctype = "Attendance"
			special_holiday = frappe.db.get_value("Special Holiday" , {"from_date" : ["<=", getdate(doc.date)] , "to_date" : [">=", getdate(doc.date)]})
			if special_holiday:
				
				sp_h = frappe.get_doc("Special Holiday"  , special_holiday)

				doctype = "Special Holiday Worked"
			attendance = ""
			previous = False
			if doctype == "Attendance":
				attendance = frappe.db.get_value('Employee Checkin', {"employee":  doc.employee ,"date" : doc.date , 'log_type' : 'IN' ,'attendance' : ['!=', ''] } , 'attendance')
				previous = frappe.db.exists("Employee Checkin", {"employee": doc.employee ,"date" : doc.date , 'log_type' : 'IN' , 'attendance' : ['!=', ''] } ,"name" )
			else:
				attendance = frappe.db.get_value('Employee Checkin', {"employee":  doc.employee ,"date" : doc.date , 'log_type' : 'IN' ,'special_attendance' : ['!=', ''] } , 'special_attendance')
				previous = frappe.db.exists("Employee Checkin", {"employee": doc.employee ,"date" : doc.date , 'log_type' : 'IN' , 'special_attendance' : ['!=', ''] } ,"name" )


			doc.log_type = "IN"
			
			shift_end = frappe.db.get_value("Shift Type" , shift , "end_time")
			# last_time = frappe.utils.time_diff_in_hours(doc.time, shift_end)
			em_time_chec = str(doc.time)
			em_time_chec_ti = em_time_chec.split(" ")[1]
			exact_time = frappe.utils.to_timedelta(em_time_chec_ti)
			last_time = frappe.utils.time_diff_in_hours(em_time_chec_ti, str(shift_end))
			
			if frappe.db.exists(doctype , {"name" :attendance , "docstatus" :0}) and abs(last_time) < 4:
				
				if previous:
					
					pr_log_type = frappe.db.get_value('Employee Checkin', {"employee":  doc.employee ,"date" : doc.date , 'log_type' : 'IN' , 'attendance' : ['!=', '']  } , 'log_type')
					my_time = frappe.db.get_value('Employee Checkin', {"employee":  doc.employee ,"date" : doc.date , 'log_type' : 'IN' } , 'time')
					in_time_diff = frappe.utils.time_diff_in_hours(doc.time , my_time)
					doc.log_type = ''
					if in_time_diff > 3:
						

						if shift:
							# attendance = frappe.db.get_value('Employee Checkin', {"employee":  doc.employee ,"date" : doc.date , 'log_type' : 'IN' , 'attendance' : ['!=', ''] } , 'attendance')
							
							# if pr_log_type == "IN":
							
							doc.log_type = "OUT"
							emp_shift = frappe.get_doc("Shift Type" , shift)
							b = str(doc.time)
							ts = b.split(" ")[1]
							o_time = frappe.utils.to_timedelta(ts)
							early = frappe.utils.time_diff_in_seconds(emp_shift.end_time , o_time)
							early_min = float(early)/60
							early_exit = 0
							early_out = 0
							late_out = 0
							if o_time > emp_shift.end_time:
								late_out =frappe.utils.format_duration(abs(early) , hide_days=True)
							if o_time < emp_shift.end_time:
								early_out =frappe.utils.format_duration(abs(early) , hide_days=True)
							if early_min > emp_shift.early_exit_grace_period:
								early_exit = 1
							if attendance:
								attend = frappe.get_doc(doctype , attendance)
								
								working_hours = frappe.utils.time_diff_in_hours(doc.time , attend.in_time)
								hours = frappe.utils.time_diff_in_seconds(doc.time , attend.in_time)
								pre_hour = frappe.utils.format_duration(hours , hide_days=True) # '11d 13h 46m 40s'
								sts  = "Present"
								half_d = frappe.db.get_value("Shift Type" , shift  , "working_hours_threshold_for_half_day")
								absent_d = frappe.db.get_value("Shift Type" , shift  , "working_hours_threshold_for_absent")
								if absent_d and working_hours < absent_d :
									sts = "Absent"
								if half_d and working_hours < half_d :
									sts = "Half Day"
								
								if doctype != "Attendance":
									sts = "Worked On Eid"

								attend.out_time = doc.time
								attend.working_hours = working_hours
								attend.early_exit = early_exit
								attend.hourse = pre_hour
								attend.status = sts
								attend.early_out = early_out
								attend.late_out = late_out
								attend.out_time_string =  ts
						
								attend.save()
								# # attend.submit()
								if doctype == "Attendance":
									doc.attendance = attend.name
								else:
									doc.special_attendance = attend.name

								doc.shift = shift
						
								
					
				
						
			else:	
					holiday_list_name = get_holiday_list_for_employee(doc.employee, False)
					doc.date = frappe.utils.getdate(doc.time)
					doc.shift = shift
			# 		frappe.get_doc("Employee" , "0000erf")
					my_time = frappe.db.get_value('Employee Checkin', {"employee":  doc.employee ,"date" : doc.date} , 'time')
					in_time_diff = frappe.utils.time_diff_in_hours(doc.time , my_time)
					doc.log_type = ''
					
					# if abs(in_time_diff) > 3:
					emp_shift = frappe.get_doc("Shift Type" , shift)
					b = str(doc.time)
					doc.log_type = "IN"
					ts = b.split(" ")[1]
					in_time = frappe.utils.to_timedelta(ts)
					late = frappe.utils.time_diff_in_seconds(in_time,emp_shift.start_time )
					late_min = float(late)/60
					late_entry = 0
					late_in = 0
					early_in = 0
					if in_time >emp_shift.start_time:
						late_in = frappe.utils.format_duration(abs(late) , hide_days=True)
					if  in_time < emp_shift.start_time:
						early_in = frappe.utils.format_duration(abs(late) , hide_days=True)
						
					
					if int(late_min) > emp_shift.late_entry_grace_period:
						late_entry = 1
					special_holiday = frappe.db.get_value("Special Holiday" , {"from_date" : ["<=", getdate(doc.date)] , "to_date" : [">=", getdate(doc.date)]})
					holiday = ''
					worked_on_holiday = 0
					no_atte_in_sp_holiday = False
					sts = "Present"
			
					doctype = "Attendance"
					if special_holiday:
						sp_h = frappe.get_doc("Special Holiday"  , special_holiday)
						holiday = sp_h.holiday
						worked_on_holiday = 1
						no_atte_in_sp_holiday =True
						field = "special_attendance"
						doctype = "Special Holiday Worked"
						sts = "Worked On Eid"
						
					elif  is_holiday(holiday_list_name, doc.date):
						
						holiday = holiday_list_name
						worked_on_holiday = 1

					attend = frappe.get_doc(
						{
							"doctype" : doctype,
							"employee" : doc.employee,
							"status" : sts,
							"in_time_string" :  ts ,
							"late_in" : late_in,
							"early_in" : early_in,
							
							
							"late_entry" : late_entry,
							"attendance_date" : doc.date,
							"in_time" : doc.time,
							"shift" :shift,
							"worked_on_holiday" : worked_on_holiday,
							"holiday" : holiday
							# "company" : emp_d.company
							
						
						})
					# if not no_atte_in_sp_holiday:
					
					attend.insert()
					if doctype == "Attendance":
						doc.attendance = attend.name
					else:
						doc.special_attendance = attend.name
					doc.shift = shift
	
		else:
			doc.erro_log = f"{doc.employee}{doc.employee_name} has no Schedule Shift and Also has no Default Shift"
	except Exception as e: doc.erro_log = str(e)
