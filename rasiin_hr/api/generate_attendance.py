import frappe
from rasiin_hr.rasiin_hr.report.personal_attendace_report.personal_attendace_report import get_data

@frappe.whitelist()
def generate_attendance(from_date , to_date):
   
    create_attendace(from_date , to_date)
    # frappe.enqueue(create_attendace, queue='short', from_date=from_date , to_date = to_date)




def create_attendace():
    emp = frappe.db.get_list("Employee" , pluck = 'name')
    for em in emp:
        filters = {
            "from_date" : "01-12-2023",
            "to_date" : "25-12-2023",
            "employee" : em
        }
        data = get_data(filters)
        # if data
        for d in data:
                try:
                    if d['shift'] != "Free":
                        attend = {}
                        if d['status'] == "Absent" or  d['status'] == "On Leave":
                            attend = frappe.get_doc(
                            {
                                    "doctype" : "Attendance",
                                    "employee" :em,
                                    "status" : d['status'],
                                    # "in_time_string" :  d['in_time_string'] ,
                                    # # "late_in" : late_in,
                                    # # "early_in" : early_in,
                                    
                                    
                                    # # "late_entry" : late_entry,
                                    "attendance_date" : d['attendance_date'],
                                    # "in_time" : d['time_in'],
                                    # "out_time": d['out_time'],
                                    # "shift" :d['shift'],
                                    # "worked_on_holiday" : worked_on_holiday,
                                    # "holiday" : holiday
                                    # "company" : emp_d.company
                                    
                                
                                })
                        else:
                            attend = frappe.get_doc(
                                {
                                    "doctype" : "Attendance",
                                    "employee" :em,
                                    "status" : d['status'],
                                    "in_time_string" :  d['in_time_string'] ,
                                    "out_time_string" : d["out_time_string"],
                                    # "late_in" : late_in,
                                    # "early_in" : early_in,
                                    
                                    
                                    # "late_entry" : late_entry,
                                    "attendance_date" : d['attendance_date'],
                                    "in_time" : d['in_time'],
                                    "out_time": d['out_time'],
                                    "shift" :d['shift'],
                                    # "worked_on_holiday" : worked_on_holiday,
                                    # "holiday" : holiday
                                    # "company" : emp_d.company
                                    
                                
                                })
                    attend.insert()
                    attend.submit()
                    frappe.db.commit()
                except:
                     pass



    return 