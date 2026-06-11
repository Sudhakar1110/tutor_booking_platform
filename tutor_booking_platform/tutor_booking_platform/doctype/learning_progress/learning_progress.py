# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe.utils import today

class LearningProgress(Document):
    def before_save(self):
        self.last_updated = today()
        if self.sessions_completed and self.sessions_attended:
            total = frappe.db.count("Tutor Session", {
                "tutor_booking": self.tutor_booking,
                "docstatus": 1,
            }) or self.sessions_completed
            if total > 0:
                self.completion_percentage = min(100, (self.sessions_completed / total) * 100)
