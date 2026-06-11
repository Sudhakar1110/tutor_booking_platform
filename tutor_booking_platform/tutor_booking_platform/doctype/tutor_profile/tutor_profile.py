# -*- coding: utf-8 -*-
# Copyright (c) 2025, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class TutorProfile(Document):
    def autoname(self):
        self.name = frappe.model.naming.make_autoname(self.naming_series or "TUT-.YYYY.-.####")

    def validate(self):
        self._validate_email()
        self._validate_mobile()
        self._validate_rate()

    def before_save(self):
        if not self.user and self.email:
            user = frappe.db.get_value("User", {"email": self.email}, "name")
            if user:
                self.user = user

    def on_update(self):
        pass

    def _validate_email(self):
        if self.email:
            import re
            if not re.match(r'^[\w.+-]+@[\w-]+\.[\w.]+$', self.email):
                frappe.throw(_("Invalid email address: {0}").format(self.email))

    def _validate_mobile(self):
        if self.mobile:
            mobile = self.mobile.strip().replace(" ", "")
            if not mobile.replace("+", "").replace("-", "").isdigit():
                frappe.throw(_("Invalid mobile number: {0}").format(self.mobile))

    def _validate_rate(self):
        if self.hourly_rate and self.hourly_rate < 0:
            frappe.throw(_("Hourly rate cannot be negative."))

    @frappe.whitelist()
    def get_dashboard_data(self):
        """Return dashboard data for tutor profile."""
        return {
            "non_standard_fieldnames": {},
            "transactions": [
                {"label": _("Bookings"), "items": ["Tutor Booking"]},
                {"label": _("Sessions"), "items": ["Tutor Session"]},
                {"label": _("Reviews"), "items": ["Tutor Review", "Tutor Rating"]},
            ],
        }
