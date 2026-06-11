# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import getdate

class TutorCertification(Document):
    def validate(self):
        if self.issue_date and self.expiry_date and not self.is_lifetime_valid:
            if getdate(self.issue_date) > getdate(self.expiry_date):
                frappe.throw(_("Issue Date cannot be after Expiry Date."))
