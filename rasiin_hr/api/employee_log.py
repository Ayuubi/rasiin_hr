import frappe
from datetime import datetime, timedelta, time as dtime

def normalize_shift_time(value):
    """
    Converts Shift Type start_time / end_time into a proper datetime.time object.
    Handles:
      - datetime.time
      - timedelta (duration)
      - string "08:00:00"
    """
    from datetime import datetime as _dt, time as _time, timedelta as _td

    if isinstance(value, _time):
        return value

    if isinstance(value, _td):
        total_seconds = int(value.total_seconds())
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return _dt.strptime(f"{hours:02d}:{minutes:02d}:{seconds:02d}", "%H:%M:%S").time()

    if isinstance(value, str):
        return _dt.strptime(value, "%H:%M:%S").time()

    raise ValueError(f"Unsupported shift time format: {value!r} ({type(value)})")


def detect_log_type(ts, shift_start_time, shift_end_time):
    """
    Unified IN/OUT detection that handles day, night, 24h, multi-day shifts.
    """
    shift_start = datetime.combine(ts.date(), shift_start_time)
    shift_end = datetime.combine(ts.date(), shift_end_time)

    # Night shift: end <= start -> end is next day
    if shift_end <= shift_start:
        shift_end += timedelta(days=1)

    # windows (adjustable)
    IN_WINDOW_HOURS = 3
    OUT_WINDOW_HOURS = 3

    IN_window_start = shift_start - timedelta(hours=IN_WINDOW_HOURS)
    IN_window_end = shift_start + timedelta(hours=IN_WINDOW_HOURS)
    OUT_window_start = shift_end - timedelta(hours=OUT_WINDOW_HOURS)
    OUT_window_end = shift_end + timedelta(hours=OUT_WINDOW_HOURS)

    if IN_window_start <= ts <= IN_window_end:
        return "IN"
    if OUT_window_start <= ts <= OUT_window_end:
        return "OUT"

    # fallback: whichever boundary is closer
    start_diff = abs((ts - shift_start).total_seconds())
    end_diff = abs((ts - shift_end).total_seconds())
    return "IN" if start_diff < end_diff else "OUT"

@frappe.whitelist(allow_guest=True)
def add_employee_checkin(user_id, timestamp):
    try:
        emp = frappe.db.get_value(
            "Employee",
            {"attendance_device_id": user_id},
            ["name", "company", "default_shift", "attendance_device_id"],
            as_dict=True
        )

        if not emp:
            return {"status": "error", "message": f"No employee for user_id={user_id}"}

        # parse timestamp
        try:
            ts = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return {"status": "error", "message": "Invalid timestamp format"}

        # timezone correction (same as Flask)
        TZ_OFFSET_HOURS = 0
        ts = ts + timedelta(hours=TZ_OFFSET_HOURS)

        # get shift (Shift Assignment preferred)
        shift_name = frappe.db.get_value("Shift Assignment",
            {"employee": emp.name, "docstatus": 1},
            "shift_type")

        if not shift_name:
            shift_name = emp.default_shift or emp.shift

        if not shift_name:
            log_type = "IN"
        else:
            shift_doc = frappe.get_doc("Shift Type", shift_name)
            shift_start_time = normalize_shift_time(shift_doc.start_time)
            shift_end_time = normalize_shift_time(shift_doc.end_time)
            log_type = detect_log_type(ts, shift_start_time, shift_end_time)

        # duplicate prevention
        if frappe.db.exists("Employee Checkin", {"employee": emp.name, "time": ts}):
            return {"status": "duplicate", "message": "Record already exists"}

        doc = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": emp.name,
            "time": ts,
            "log_type": log_type,
            "company": emp.company
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "employee": emp.name,
            "log_type": log_type,
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception:
        frappe.log_error(frappe.get_traceback(), "ZKTeco Checkin Error")
        return {"status": "error", "message": "Internal error"}
