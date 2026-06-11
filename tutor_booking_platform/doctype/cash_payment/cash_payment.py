# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
class CashPayment(Document):
    def validate(self):
        if self.amount and self.amount <= 0:
            frappe.throw(_("Amount must be greater than zero."))
    def on_submit(self):
        self.payment_status = "Received"
        frappe.db.set_value("Cash Payment", self.name, "payment_status", "Received")