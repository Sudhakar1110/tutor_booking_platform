# -*- coding: utf-8 -*-
"""Document events for Refund Request DocType."""
import frappe
from frappe import _


def validate(doc, method=None):
    if not doc.reason:
        frappe.throw(_("Refund reason is mandatory."))
    if doc.refund_amount and doc.refund_amount <= 0:
        frappe.throw(_("Refund amount must be greater than zero."))


def on_submit(doc, method=None):
    doc.refund_status = "Processed"
    frappe.db.set_value("Refund Request", doc.name, "refund_status", "Processed",
                        update_modified=False)