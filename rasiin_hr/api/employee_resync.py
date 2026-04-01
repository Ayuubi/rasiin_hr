import frappe
import requests

FLASK_RESYNC_URL = "http://127.0.0.1:6000/resync"  # adjust if needed

def on_update_employee(doc, method=None):
    """
    Called whenever an Employee is updated (including via Data Import).

    We don't call Flask immediately from here, because this runs
    *before* DB commit. Instead, we schedule a callback via
    frappe.db.after_commit so the external /resync sees committed data.
    """
    device_id = (doc.get("attendance_device_id") or "").strip()
    if not device_id:
        return

    # This function will run *after* the Employee is committed
    def _after_commit():
        try:
            url = f"{FLASK_RESYNC_URL}?user_id={device_id}"
            requests.get(url, timeout=2)
        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                f"Failed to trigger /resync for device_id {device_id}",
            )

    frappe.db.after_commit.add(_after_commit)
