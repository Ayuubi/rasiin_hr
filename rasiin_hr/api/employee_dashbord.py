import frappe

@frappe.whitelist(allow_guest = 1)
def get_e_dash():
    
    # frappe.msgprint(patient)
    volunteer = volunteer_d()
    employee = employee_d()
    

    all_his =  [employee , employee ]
    data = {}
    all_his_key =  ["employee" , "volunteer" ]
    columns = {}
    for   index , history in enumerate(all_his):
        # frappe.errprint(history)
        columns[all_his_key[index]] = []
        data[all_his_key[index]] = []
        if history:
            for idx, h in enumerate(history):
                data_inner = {}
                for key , val in h.items():
                   
                    if idx == 0:
                        columns[all_his_key[index]].append(
                            
                            {"title":key, "field":key.replace(' ', '_').lower()  ,  "formatter":"html"},
                            
                        )
                    data_inner[key.replace(' ', '_').lower()] = val
                data[all_his_key[index]].append(
                    data_inner
                )

    frappe.errprint(data)
    # frappe.errprint(columns)
    return columns, data


@frappe.whitelist()
def volunteer_d():
    emp = frappe.db.sql(f""" 
    
        select name ,employee_name, department, 
        designation, cell_number, 
        amount, gender, status 
        from `tabEmployee` where volunteer =1 

    
  
    
    """ , as_dict = True)
    for index, row in enumerate(emp):
        row['no'] = index + 1

    return emp

 

@frappe.whitelist()
def employee_d():
    emp = frappe.db.sql(f""" 
    
        select name ,employee_name,
        department, designation,
        cell_number, amount, gender,
        status from `tabEmployee` where volunteer =0

    
  
    
    """ , as_dict = True)
    for index, row in enumerate(emp):
        row['no'] = index + 1

    return emp
