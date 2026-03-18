from zk import ZK, const
import frappe

# ZKTeco devices connection settings
devices = [
    {
        'device_ip': '172.16.0.250',
        'device_port': 4370,
        'device_timeout': 5,
        'device_id': 1
    },
    {
        'device_ip': '172.16.0.201',
        'device_port': 4370,
        'device_timeout': 5,
        'device_id': 2
    },
    # Add more devices as needed
]

def is_employee_registered(device, attendance_device_id):
    users = device.get_users()
    # frappe.errprint(users)
    return any(user.user_id == attendance_device_id for user in users)

def create_employee_on_device(device, employee):
    attendance_device_id = employee['attendance_device_id']
    # frappe.errprint(device)
    # Check if the employee already exists on the device
    if is_employee_registered(device, attendance_device_id):
        print(f"Employee with ID {attendance_device_id} already exists on the device.")
        return

    # Create a new user on the device
    user_id = attendance_device_id
    user_name = employee['employee_name']
    privilege = const.USER_DEFAULT
    # password = ''  # Set a password if required
    card = '0'  # Set card ID if required
    # frappe.errprint(type(user_name))
    if user_id and user_name:
        device.set_user(uid=int(user_id), name=user_name, privilege=0, card=0)
    if is_employee_registered(device, attendance_device_id):
        frappe.msgprint(f"Employee with ID {user_id} created on the device.")
    else:
        
        frappe.msgprint(f"This Employee will not registered to the Fingerprint since you are not provided ID.")
   

@frappe.whitelist()
def synchronize_employees(doc, method=None):
    for device_info in devices:
        device_ip = device_info['device_ip']
        device_port = device_info['device_port']
        device_timeout = device_info['device_timeout']
        device_id = device_info['device_id']

        # Connect to the ZKTeco device
        zk = ZK(device_ip, device_port, device_timeout)

        if zk.connect():
            frappe.errprint(f"Connected to the device at {device_ip}:{device_port}")

            # Get employee data from ERPNext
            employee = {
                'attendance_device_id': doc.attendance_device_id,
                'employee_name': doc.employee_name
            }

            # Synchronize employees with the device
            create_employee_on_device(zk, employee)

            # Disconnect from the device
            zk.disconnect()
            frappe.errprint(f"Disconnected from the device at {device_ip}:{device_port}")
        else:
            frappe.errprint(f"Unable to connect to the device at {device_ip}:{device_port}")


@frappe.whitelist()
def synchronize_employees_old():
    for device_info in devices:
        device_ip = device_info['device_ip']
        device_port = device_info['device_port']
        device_timeout = device_info['device_timeout']
        device_id = device_info['device_id']

        # Connect to the ZKTeco device
        zk = ZK(device_ip, device_port, device_timeout)

        if zk.connect():
            frappe.errprint(f"Connected to the device at {device_ip}:{device_port}")

            # Get employee data from ERPNext
            employees = frappe.get_all(
                "Employee",
                filters={},
                fields=["employee_name", "attendance_device_id"]
                )
            # Create an empty dictionary to store the employee data
            employee_dict = {}

            # Populate the dictionary with attendance device IDs and employee names
            for employee in employees:
                if not employee.attendance_device_id:
                   continue 
                employee_dict["attendance_device_id"] = employee.attendance_device_id
                employee_dict["employee_name"] = employee.employee_name
            # Synchronize employees with the device
                create_employee_on_device(zk, employee_dict)
            # Disconnect from the device
            zk.disconnect()
            frappe.errprint(f"Disconnected from the device at {device_ip}:{device_port}")
        else:
            frappe.errprint(f"Unable to connect to the device at {device_ip}:{device_port}")
