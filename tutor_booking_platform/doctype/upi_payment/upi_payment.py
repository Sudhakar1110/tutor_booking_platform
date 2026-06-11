# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
class UpiPayment(Document):
    def validate(self):
        if not self.upi_id:
            frappe.throw(_("UPI ID is required."))
        if self.amount and self.amount <= 0:
            frappe.throw(_("Amount must be greater than zero."))
    def on_submit(self):
        self.payment_status = "Success"
        frappe.db.set_value("UPI Payment", self.name, "payment_status", "Success")