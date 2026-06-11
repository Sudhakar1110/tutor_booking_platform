import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "student_name", "label": _("Student"), "fieldtype": "Data", "width": 150},
        {"fieldname": "tutor_name", "label": _("Tutor"), "fieldtype": "Data", "width": 150},
        {"fieldname": "subject", "label": _("Subject"), "fieldtype": "Link", "options": "Subject", "width": 120},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "preferred_date", "label": _("Date"), "fieldtype": "Date", "width": 100},
    ]
    data = frappe.get_all("Demo Class Request", fields=["student_profile", "tutor_profile", "subject", "status", "preferred_date"])
    for d in data:
        d.student_name = frappe.db.get_value("Student Profile", d.student_profile, "student_name") or d.student_profile
        d.tutor_name = frappe.db.get_value("Tutor Profile", d.tutor_profile, "tutor_name") or d.tutor_profile
    return columns, data
