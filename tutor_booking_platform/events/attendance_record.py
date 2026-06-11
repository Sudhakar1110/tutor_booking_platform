# -*- coding: utf-8 -*-
"""Document events for Attendance Record DocType."""
import frappe
from frappe import _


def validate(doc, method=None):
    if not doc.tutor_session:
        frappe.throw(_("Tutor Session reference is mandatory."))


def on_submit(doc, method=None):
    _update_learning_progress(doc)


def _update_learning_progress(doc):
    try:
        progress = frappe.db.get_value("Learning Progress", {
            "student_profile": doc.student_profile,
            "subject": doc.subject,
        }, "name")
        if progress:
            pdoc = frappe.get_doc("Learning Progress", progress)
            pdoc.sessions_completed = (pdoc.sessions_completed or 0) + 1
            pdoc.save(ignore_permissions=True)
    except Exception as e:
        frappe.log_error(str(e), "Update Learning Progress Error")