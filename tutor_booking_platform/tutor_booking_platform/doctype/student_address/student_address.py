# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document

class StudentAddress(Document):
    def validate(self):
        if self.is_default:
            frappe.db.set_value("Student Address",
                {"student_profile": self.student_profile, "is_default": 1, "name": ["!=", self.name or ""]},
                "is_default", 0)
