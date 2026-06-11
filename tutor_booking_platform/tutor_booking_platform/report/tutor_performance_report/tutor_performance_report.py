import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "tutor_name", "label": _("Tutor Name"), "fieldtype": "Data", "width": 180},
        {"fieldname": "hourly_rate", "label": _("Rate (INR)"), "fieldtype": "Currency", "width": 100},
        {"fieldname": "average_rating", "label": _("Rating"), "fieldtype": "Float", "width": 80},
        {"fieldname": "total_sessions", "label": _("Sessions"), "fieldtype": "Int", "width": 80},
        {"fieldname": "total_students", "label": _("Students"), "fieldtype": "Int", "width": 80},
        {"fieldname": "verification_status", "label": _("Status"), "fieldtype": "Data", "width": 120},
    ]
    data = frappe.get_all("Tutor Profile", fields=["tutor_name", "hourly_rate", "average_rating", "total_sessions", "total_students", "verification_status"])
    chart = {"data": {"labels": [d.tutor_name for d in data], "datasets": [{"values": [d.average_rating or 0 for d in data]}]}, "type": "bar"}
    return columns, data, None, chart
