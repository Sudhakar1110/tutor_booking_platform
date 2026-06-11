# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class LearningSchedule(Document):
    def validate(self):
        if self.start_time and self.end_time:
            if str(self.start_time) >= str(self.end_time):
                frappe.throw(_("Start Time must be before End Time."))