# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class TutorAvailability(Document):
    def validate(self):
        if self.start_time and self.end_time:
            if str(self.start_time) >= str(self.end_time):
                frappe.throw(_("Start Time must be before End Time."))
        self._check_duplicate()

    def _check_duplicate(self):
        existing = frappe.db.exists("Tutor Availability", {
            "tutor_profile": self.tutor_profile,
            "day_of_week": self.day_of_week,
            "name": ["!=", self.name or ""],
        })
        if existing:
            frappe.throw(_(
                "Availability for {0} on {1} already exists."
            ).format(self.tutor_profile, self.day_of_week))
