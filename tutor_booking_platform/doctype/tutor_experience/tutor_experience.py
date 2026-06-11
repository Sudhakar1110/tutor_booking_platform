# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import date_diff, getdate

class TutorExperience(Document):
    def validate(self):
        if self.from_date and self.to_date:
            if getdate(self.from_date) > getdate(self.to_date):
                frappe.throw(_("From Date cannot be after To Date."))
        if self.from_date and not self.is_current:
            if not self.to_date:
                frappe.throw(_("To Date is required if not currently working."))
        self._compute_months()

    def _compute_months(self):
        if self.from_date:
            end = getdate(self.to_date) if self.to_date else getdate()
            diff = date_diff(end, getdate(self.from_date))
            self.total_experience_months = max(0, diff // 30)