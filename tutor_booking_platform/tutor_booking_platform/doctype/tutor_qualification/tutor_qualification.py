# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class TutorQualification(Document):
    def validate(self):
        if self.passing_year and self.passing_year > frappe.utils.getdate().year:
            frappe.throw(_("Passing year cannot be in the future."))
        if self.grade_percentage and (self.grade_percentage < 0 or self.grade_percentage > 100):
            frappe.throw(_("Grade percentage must be between 0 and 100."))
