# -*- coding: utf-8 -*-
"""Document events for Payment Transaction DocType."""
import frappe
from frappe import _


def validate(doc, method=None):
    if not doc.amount or doc.amount <= 0:
        frappe.throw(_("Payment amount must be greater than zero."))
    if doc.payment_method == "UPI" and not doc.upi_transaction_id:
        frappe.throw(_("UPI Transaction ID is required for UPI payments."))


def on_submit(doc, method=None):
    doc.payment_status = "Completed"
    frappe.db.set_value("Payment Transaction", doc.name, "payment_status", "Completed",
                        update_modified=False)
    if doc.tutor_booking:
        frappe.db.set_value("Tutor Booking", doc.tutor_booking, "payment_status", "Paid",
                            update_modified=False)


def on_cancel(doc, method=None):
    doc.payment_status = "Cancelled"
    frappe.db.set_value("Payment Transaction", doc.name, "payment_status", "Cancelled",
                        update_modified=False)
    if doc.tutor_booking:
        frappe.db.set_value("Tutor Booking", doc.tutor_booking, "payment_status", "Unpaid",
                            update_modified=False)