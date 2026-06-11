# -*- coding: utf-8 -*-
"""Document events for Tutor Session DocType."""
import frappe
from frappe import _


def validate(doc, method=None):
    if doc.start_time and doc.end_time:
        if str(doc.start_time) >= str(doc.end_time):
            frappe.throw(_("Start Time must be before End Time."))
    if doc.tutor_booking:
        booking = frappe.db.get_value("Tutor Booking", doc.tutor_booking,
                                       ["booking_status", "tutor_profile", "student_profile"],
                                       as_dict=True)
        if booking and booking.booking_status == "Cancelled":
            frappe.throw(_("Cannot create session for a cancelled booking."))


def after_insert(doc, method=None):
    pass


def on_submit(doc, method=None):
    doc.status = "Completed"
    frappe.db.set_value("Tutor Session", doc.name, "status", "Completed",
                        update_modified=False)