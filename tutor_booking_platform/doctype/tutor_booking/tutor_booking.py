# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import nowdate, getdate

class TutorBooking(Document):
    def autoname(self):
        self.name = frappe.model.naming.make_autoname(self.naming_series or "TBKN-.YYYY.-.####")

    def validate(self):
        self._validate_dates()
        self._compute_total()

    def _validate_dates(self):
        if self.start_date and self.end_date:
            if getdate(self.start_date) > getdate(self.end_date):
                frappe.throw(_("Start Date cannot be after End Date."))

    def _compute_total(self):
        if self.total_hours and self.rate_per_hour:
            self.total_amount = self.total_hours * self.rate_per_hour

    def on_submit(self):
        self.booking_status = "Confirmed"
        frappe.db.set_value("Tutor Booking", self.name, "booking_status", "Confirmed")

    def on_cancel(self):
        self.booking_status = "Cancelled"
        frappe.db.set_value("Tutor Booking", self.name, "booking_status", "Cancelled")

    @frappe.whitelist()
    def get_dashboard_data(self):
        return {
            "transactions": [
                {"label": _("Sessions"), "items": ["Tutor Session"]},
                {"label": _("Payments"), "items": ["Payment Transaction"]},
            ],
        }