# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
class Course(Document):
    def validate(self):
        if self.fee and self.fee < 0:
            frappe.throw(_("Course fee cannot be negative."))