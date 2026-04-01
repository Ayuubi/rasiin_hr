from datetime import datetime
import frappe

@frappe.whitelist(allow_guest=True)
def add_employee_checkin(user_id, timestamp):
    """
    Create a new Employee Checkin record using user_id (attendance_device_id).

    Expects:
      - user_id: the device PIN / number
      - timestamp: "YYYY-MM-DD HH:MM:SS" (already adjusted by Flask)
    """
    try:
        time_in = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        new_time = time_in

        # Map device user_id -> Employee
        employee_id = frappe.db.get_value("Employee", {"attendance_device_id": user_id}, "name")
        if not employee_id:
            return {"status": "error", "message": "Employee not found for the provided user_id."}

        # DEDUP: avoid double checkins
        if frappe.db.exists("Employee Checkin", {"employee": employee_id, "time": new_time}):
            return {"status": "success", "message": "Check-in already exists."}

        doc = frappe.get_doc(
            {
                "doctype": "Employee Checkin",
                "employee": employee_id,
                "time": new_time,
            }
        )
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": "Check-in recorded successfully."}

    except Exception:
        frappe.log_error(
            title="Error in add_employee_checkin",
            message=frappe.get_traceback(),
        )
        return {"status": "error", "message": "Internal server error."}



# # import frappe

# # @frappe.whitelist(allow_guest=True)  # allow_guest=True if you want it accessible without login
# # def add_employee_checkin(employee_id, timestamp):
# #     """
# #     Create a new Employee Checkin record.
# #     """
# #     try:
# #         # Create new document in Frappe
# #         doc = frappe.get_doc({
# #             'doctype': 'Employee Checkin',
# #             'employee': employee_id,
# #             'time': timestamp
# #         })
# #         doc.insert(ignore_permissions=True)  # Use ignore_permissions if calling from external systems without user context
# #         frappe.db.commit()  # Commit to save the document
# #         return {"status": "success", "message": "Check-in recorded successfully."}
# #     except Exception as e:
# #         return {"status": "error", "message": str(e)}

# from datetime import datetime, timedelta

# import frappe

# @frappe.whitelist(allow_guest=True)
# def add_employee_checkin(user_id, timestamp):
#     time_in = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#     # new_time = time_in - timedelta(hours=5)
#     new_time = time_in 
#     """
#     Create a new Employee Checkin record using user_id instead of employee_id.
#     """
#     try:
#         # Retrieve employee_id using the user_id (attendance_device_id)
#         employee_id = frappe.db.get_value('Employee', {'attendance_device_id': user_id}, 'name')
        
#         # Check if employee_id is found
#         if not employee_id:
#             return {"status": "error", "message": "Employee not found for the provided user_id."}

#         # Create new document in Frappe
#         doc = frappe.get_doc({
#             'doctype': 'Employee Checkin',
#             'employee': employee_id,
#             'time': new_time
#         })
#         doc.insert(ignore_permissions=True)  # Use ignore_permissions if calling from external systems without user context
#         frappe.db.commit()  # Commit to save the document
#         return {"status": "success", "message": "Check-in recorded successfully."}
#     except Exception as e:
#         print(f"Error in add_employee_checkin: {str(e)}")
#         return {"status": "error", "message": str(e)}
