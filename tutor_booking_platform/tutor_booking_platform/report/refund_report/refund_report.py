import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "student_name", "label": _("Student"), "fieldtype": "Data", "width": 150},
        {"fieldname": "refund_status", "label": _("Status"), "fieldtype": "Data", "width": 120},
        {"fieldname": "original_amount", "label": _("Original"), "fieldtype": "Currency", "width": 100},
        {"fieldname": "refund_amount", "label": _("Refund"), "fieldtype": "Currency", "width": 100},
        {"fieldname": "reason", "label": _("Reason"), "fieldtype": "Data", "width": 200},
        {"fieldname": "refund_date", "label": _("Date"), "fieldtype": "Date", "width": 100},
    ]
    data = frappe.get_all("Refund Request", fields=["student_profile", "refund_status", "original_amount", "refund_amount", "reason", "refund_date"], order_by="creation desc")
    for d in data:
        d.student_name = frappe.db.get_value("Student Profile", d.student_profile, "student_name") or d.student_profile
    return columns, data
