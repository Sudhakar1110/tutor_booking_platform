import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "tutor_name", "label": _("Tutor"), "fieldtype": "Data", "width": 150},
        {"fieldname": "overall_rating", "label": _("Rating"), "fieldtype": "Float", "width": 80},
        {"fieldname": "subject_knowledge", "label": _("Knowledge"), "fieldtype": "Float", "width": 80},
        {"fieldname": "teaching_methodology", "label": _("Methodology"), "fieldtype": "Float", "width": 80},
        {"fieldname": "punctuality", "label": _("Punctuality"), "fieldtype": "Float", "width": 80},
        {"fieldname": "communication_skills", "label": _("Communication"), "fieldtype": "Float", "width": 80},
    ]
    data = frappe.get_all("Tutor Rating", fields=["tutor_profile", "overall_rating", "subject_knowledge", "teaching_methodology", "punctuality", "communication_skills"])
    for d in data:
        d.tutor_name = frappe.db.get_value("Tutor Profile", d.tutor_profile, "tutor_name") or d.tutor_profile
    return columns, data
