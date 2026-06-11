# -*- coding: utf-8 -*-
"""Hourly scheduled tasks."""
import frappe
from frappe.utils import now_datetime


def process_pending_notifications():
    """Process and send pending notification logs."""
    try:
        pending = frappe.get_all("Notification Log", filters={
            "status": "Pending",
            "docstatus": 0,
        }, fields=["name", "subject", "message", "recipient"], limit=50)

        for n in pending:
            try:
                frappe.db.set_value("Notification Log", n.name, "status", "Sent",
                                    update_modified=False)
            except Exception:
                frappe.db.set_value("Notification Log", n.name, "status", "Failed",
                                    update_modified=False)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "process_pending_notifications Error")


def check_session_status():
    """Mark sessions as completed if their end time has passed."""
    try:
        now = now_datetime()
        overdue = frappe.get_all("Tutor Session", filters={
            "status": "Scheduled",
            "docstatus": 1,
        }, fields=["name", "session_date", "end_time"])

        for s in overdue:
            if s.session_date and s.end_time:
                import datetime
                session_end = datetime.datetime.combine(
                    s.session_date,
                    datetime.time(*map(int, str(s.end_time).split(":")[:2]))
                )
                if now > session_end:
                    frappe.db.set_value("Tutor Session", s.name, "status", "Completed",
                                        update_modified=False)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "check_session_status Error")