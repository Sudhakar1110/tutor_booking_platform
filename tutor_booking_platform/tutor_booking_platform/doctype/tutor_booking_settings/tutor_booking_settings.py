# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document


class TutorBookingSettings(Document):
    def validate(self):
        if self.commission_percentage and (self.commission_percentage < 0 or self.commission_percentage > 100):
            frappe.throw(frappe._("Commission percentage must be between 0 and 100."))
        if self.min_session_duration and self.min_session_duration < 15:
            frappe.throw(frappe._("Minimum session duration must be at least 15 minutes."))
