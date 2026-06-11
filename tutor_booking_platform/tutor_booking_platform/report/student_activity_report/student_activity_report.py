import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "student_name", "label": _("Student"), "fieldtype": "Data", "width": 150},
        {"fieldname": "email", "label": _("Email"), "fieldtype": "Data", "width": 150},
        {"fieldname": "current_class", "label": _("Class"), "fieldtype": "Data", "width": 100},
        {"fieldname": "budget_per_hour", "label": _("Budget"), "fieldtype": "Currency", "width": 100},
        {"fieldname": "preferred_learning_mode", "label": _("Mode"), "fieldtype": "Data", "width": 100},
    ]
    data = frappe.get_all("Student Profile", fields=["student_name", "email", "current_class", "budget_per_hour", "preferred_learning_mode"])
    return columns, data
