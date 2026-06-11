# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class TutorSession(Document):
    def validate(self):
        if self.start_time and self.end_time:
            if str(self.start_time) >= str(self.end_time):
                frappe.throw(_("Start Time must be before End Time."))
        if self.tutor_booking:
            booking = frappe.db.get_value("Tutor Booking", self.tutor_booking, "booking_status")
            if booking == "Cancelled":
                frappe.throw(_("Cannot create session for a cancelled booking."))
    def on_submit(self):
        self.status = "Completed"
        frappe.db.set_value("Tutor Session", self.name, "status", "Completed")