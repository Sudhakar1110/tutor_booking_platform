# -*- coding: utf-8 -*-
"""Document events for Demo Class Request DocType."""
import frappe
from frappe import _


def validate(doc, method=None):
    if not doc.subject:
        frappe.throw(_("Subject is mandatory for a demo class request."))


def after_insert(doc, method=None):
    _notify_tutor(doc)


def on_submit(doc, method=None):
    doc.status = "Approved"
    frappe.db.set_value("Demo Class Request", doc.name, "status", "Approved",
                        update_modified=False)


def _notify_tutor(doc):
    try:
        frappe.get_doc({
            "doctype": "Notification Log",
            "reference_doctype": doc.doctype,
            "reference_name": doc.name,
            "recipient": doc.tutor_profile,
            "subject": f"New Demo Class Request: {doc.name}",
            "message": f"You have received a demo class request for {doc.subject}.",
            "notification_type": "Demo Request",
            "status": "Pending",
        }).insert(ignore_permissions=True)
    except Exception:
        pass