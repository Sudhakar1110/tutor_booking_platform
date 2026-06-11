# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class StudentRequirement(Document):
    def validate(self):
        if self.budget_per_hour and self.budget_per_hour < 0:
            frappe.throw(_("Budget cannot be negative."))
    def on_submit(self):
        self.status = "Open"
        frappe.db.set_value("Student Requirement", self.name, "status", "Open")
