# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import nowdate

class RefundRequest(Document):
    def validate(self):
        if not self.reason:
            frappe.throw(_("Refund reason is mandatory."))
        if self.refund_amount and self.refund_amount <= 0:
            frappe.throw(_("Refund amount must be greater than zero."))
        if self.original_amount and self.refund_amount and self.refund_amount > self.original_amount:
            frappe.throw(_("Refund amount cannot exceed original payment amount."))
    def on_submit(self):
        self.refund_status = "Processed"
        self.processed_by = frappe.session.user
        self.refund_date = nowdate()
        frappe.db.set_value("Refund Request", self.name, {
            "refund_status": "Processed",
            "processed_by": frappe.session.user,
            "refund_date": nowdate(),
        })