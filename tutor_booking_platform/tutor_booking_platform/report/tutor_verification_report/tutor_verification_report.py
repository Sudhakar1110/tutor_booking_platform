import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "tutor_name", "label": _("Tutor"), "fieldtype": "Data", "width": 150},
        {"fieldname": "verification_status", "label": _("Status"), "fieldtype": "Data", "width": 120},
        {"fieldname": "verification_type", "label": _("Type"), "fieldtype": "Data", "width": 150},
        {"fieldname": "verified_by", "label": _("Verified By"), "fieldtype": "Link", "options": "User", "width": 150},
        {"fieldname": "verification_date", "label": _("Date"), "fieldtype": "Date", "width": 100},
    ]
    data = frappe.get_all("Tutor Verification", fields=["tutor_profile", "verification_status", "verification_type", "verified_by", "verification_date"], order_by="creation desc")
    for d in data:
        d.tutor_name = frappe.db.get_value("Tutor Profile", d.tutor_profile, "tutor_name") or d.tutor_profile
    return columns, data
