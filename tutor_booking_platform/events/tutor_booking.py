# -*- coding: utf-8 -*-
"""Document events for Tutor Booking DocType."""
import frappe
from frappe import _
from frappe.utils import nowdate


def validate(doc, method=None):
    """Validate Tutor Booking before save."""
    if not doc.tutor_profile:
        frappe.throw(_("Tutor Profile is mandatory."))
    if not doc.student_profile:
        frappe.throw(_("Student Profile is mandatory."))
    if doc.total_hours and doc.rate_per_hour:
        doc.total_amount = doc.total_hours * doc.rate_per_hour
    _validate_booking_dates(doc)


def after_insert(doc, method=None):
    """Actions after a new booking is created."""
    _create_notification(
        doc,
        subject=f"New Booking Created: {doc.name}",
        message=f"A new tutoring booking {doc.name} has been created for {doc.subject}.",
        notification_type="Booking Created",
        recipient=doc.tutor_profile,
    )


def on_submit(doc, method=None):
    """Actions on booking submission."""
    doc.booking_status = "Confirmed"
    frappe.db.set_value("Tutor Booking", doc.name, "booking_status", "Confirmed",
                        update_modified=False)
    _create_notification(
        doc,
        subject=f"Booking Confirmed: {doc.name}",
        message=f"Your booking {doc.name} has been confirmed.",
        notification_type="Booking Confirmed",
        recipient=doc.student_profile,
    )


def on_cancel(doc, method=None):
    """Actions on booking cancellation."""
    doc.booking_status = "Cancelled"
    frappe.db.set_value("Tutor Booking", doc.name, "booking_status", "Cancelled",
                        update_modified=False)


def _validate_booking_dates(doc):
    if doc.start_date and doc.end_date:
        if doc.start_date > doc.end_date:
            frappe.throw(_("Start Date cannot be after End Date."))
        if doc.start_date < nowdate():
            frappe.throw(_("Start Date cannot be in the past."))


def _create_notification(doc, subject, message, notification_type, recipient):
    try:
        frappe.get_doc({
            "doctype": "Notification Log",
            "reference_doctype": doc.doctype,
            "reference_name": doc.name,
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "notification_type": notification_type,
            "status": "Pending",
        }).insert(ignore_permissions=True)
    except Exception:
        pass