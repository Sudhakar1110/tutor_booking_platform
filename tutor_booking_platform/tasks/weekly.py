# -*- coding: utf-8 -*-
"""Weekly scheduled tasks."""
import frappe
from frappe.utils import today, add_days


def generate_weekly_report():
    """Generate weekly booking summary."""
    try:
        week_start = add_days(today(), -7)
        count = frappe.db.count("Tutor Booking", {
            "creation": [">=", week_start],
            "docstatus": 1,
        })
        frappe.log_error(f"Weekly bookings created: {count}", "Weekly Report Info")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "generate_weekly_report Error")


def send_tutor_performance_summary():
    """Send weekly performance summary to tutors."""
    try:
        tutors = frappe.get_all("Tutor Profile", filters={"verification_status": "Verified"},
                                fields=["name", "tutor_name", "email"])
        week_start = add_days(today(), -7)
        for tutor in tutors:
            sessions = frappe.db.count("Tutor Session", {
                "tutor_profile": tutor.name,
                "status": "Completed",
                "session_date": [">=", week_start],
            })
            if sessions > 0:
                frappe.log_error(
                    f"Tutor {tutor.tutor_name}: {sessions} sessions this week",
                    "Tutor Weekly Summary"
                )
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "send_tutor_performance_summary Error")