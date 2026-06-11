# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class PaymentTransaction(Document):
    def validate(self):
        if not self.amount or self.amount <= 0:
            frappe.throw(_("Payment amount must be greater than zero."))
        if self.payment_method == "UPI" and not self.upi_transaction_id:
            frappe.throw(_("UPI Transaction ID is required for UPI payments."))
        self._compute_commission()

    def _compute_commission(self):
        commission_pct = frappe.db.get_single_value("Tutor Booking Settings", "commission_percentage") or 10
        self.platform_commission = self.amount * (commission_pct / 100)
        self.tutor_payout = self.amount - self.platform_commission

    def on_submit(self):
        self.payment_status = "Completed"
        frappe.db.set_value("Payment Transaction", self.name, "payment_status", "Completed")
        if self.tutor_booking:
            frappe.db.set_value("Tutor Booking", self.tutor_booking, "payment_status", "Paid")

    def on_cancel(self):
        self.payment_status = "Cancelled"
        frappe.db.set_value("Payment Transaction", self.name, "payment_status", "Cancelled")