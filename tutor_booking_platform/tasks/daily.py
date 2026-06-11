# -*- coding: utf-8 -*-
"""Daily scheduled tasks for Tutor Booking Platform."""
import frappe
from frappe.utils import today, add_days, now_datetime


def send_session_reminders():
    """Send reminders for sessions scheduled tomorrow."""
    try:
        tomorrow = add_days(today(), 1)
        sessions = frappe.get_all("Tutor Session", filters={
            "session_date": tomorrow,
            "status": "Scheduled",
            "docstatus": 1,
        }, fields=["name", "student_profile", "tutor_profile", "session_date", "start_time"])

        for session in sessions:
            _log_notification(
                reference_doctype="Tutor Session",
                reference_name=session.name,
                recipient=session.student_profile,
                subject="Reminder: Upcoming Session Tomorrow",
                message=f"Your session is scheduled for tomorrow {session.session_date} at {session.start_time}.",
                notification_type="Session Reminder",
            )
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "send_session_reminders Error")


def auto_close_expired_bookings():
    """Auto-close bookings that have passed without action."""
    try:
        past_date = add_days(today(), -7)
        expired = frappe.get_all("Tutor Booking", filters={
            "booking_status": "Pending",
            "booking_date": ["<", past_date],
            "docstatus": 0,
        }, fields=["name"])

        for booking in expired:
            doc = frappe.get_doc("Tutor Booking", booking.name)
            doc.booking_status = "Expired"
            doc.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "auto_close_expired_bookings Error")


def send_demo_class_reminders():
    """Send reminders for demo classes scheduled today."""
    try:
        demos = frappe.get_all("Demo Class Schedule", filters={
            "scheduled_date": today(),
            "status": "Scheduled",
            "docstatus": 1,
        }, fields=["name", "student_profile", "tutor_profile"])

        for demo in demos:
            _log_notification(
                reference_doctype="Demo Class Schedule",
                reference_name=demo.name,
                recipient=demo.student_profile,
                subject="Reminder: Demo Class Today",
                message="Your demo class is scheduled for today. Please be on time.",
                notification_type="Demo Reminder",
            )
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "send_demo_class_reminders Error")


def update_tutor_ratings():
    """Recalculate and update average ratings for all active tutors."""
    try:
        tutors = frappe.get_all("Tutor Profile", filters={"verification_status": "Verified"},
                                fields=["name"])
        for tutor in tutors:
            result = frappe.db.sql("""
                SELECT AVG(overall_rating) as avg
                FROM \`tabTutor Rating\`
                WHERE tutor_profile = %s AND docstatus = 1
            """, tutor.name, as_dict=True)
            avg = round(result[0].avg or 0, 2) if result else 0
            frappe.db.set_value("Tutor Profile", tutor.name, "average_rating", avg,
                                update_modified=False)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "update_tutor_ratings Error")


def _log_notification(reference_doctype, reference_name, recipient, subject, message, notification_type):
    """Create a Notification Log record."""
    try:
        doc = frappe.get_doc({
            "doctype": "Notification Log",
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "notification_type": notification_type,
            "status": "Pending",
        })
        doc.insert(ignore_permissions=True)
    except Exception:
        pass