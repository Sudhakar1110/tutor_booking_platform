# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import nowdate

class TutorVerification(Document):
    def validate(self):
        if self.verification_status in ["Verified", "Rejected"] and not self.verified_by:
            self.verified_by = frappe.session.user
        if self.verification_status == "Verified":
            self.verification_date = nowdate()

    def on_submit(self):
        self._update_tutor_status()

    def _update_tutor_status(self):
        if self.tutor_profile and self.verification_status in ["Verified", "Rejected"]:
            frappe.db.set_value("Tutor Profile", self.tutor_profile,
                                "verification_status", self.verification_status)
            frappe.db.commit()