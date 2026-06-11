import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "student_name", "label": _("Student"), "fieldtype": "Data", "width": 150},
        {"fieldname": "tutor_name", "label": _("Tutor"), "fieldtype": "Data", "width": 150},
        {"fieldname": "overall_experience", "label": _("Experience"), "fieldtype": "Data", "width": 120},
        {"fieldname": "session_helpful", "label": _("Helpful?"), "fieldtype": "Data", "width": 80},
        {"fieldname": "difficulty_level", "label": _("Difficulty"), "fieldtype": "Data", "width": 100},
        {"fieldname": "feedback_date", "label": _("Date"), "fieldtype": "Date", "width": 100},
    ]
    data = frappe.get_all("Student Feedback", fields=["student_profile", "tutor_profile", "overall_experience", "session_helpful", "difficulty_level", "feedback_date"], order_by="feedback_date desc")
    for d in data:
        d.student_name = frappe.db.get_value("Student Profile", d.student_profile, "student_name") or d.student_profile
        d.tutor_name = frappe.db.get_value("Tutor Profile", d.tutor_profile, "tutor_name") or d.tutor_profile
    return columns, data
