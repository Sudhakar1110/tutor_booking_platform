import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "month", "label": _("Month"), "fieldtype": "Data", "width": 120},
        {"fieldname": "total_sessions", "label": _("Total"), "fieldtype": "Int", "width": 100},
        {"fieldname": "completed", "label": _("Completed"), "fieldtype": "Int", "width": 100},
        {"fieldname": "scheduled", "label": _("Scheduled"), "fieldtype": "Int", "width": 100},
        {"fieldname": "cancelled", "label": _("Cancelled"), "fieldtype": "Int", "width": 100},
    ]
    data = frappe.db.sql("""
        SELECT DATE_FORMAT(session_date, '%Y-%m') as month,
               COUNT(*) as total_sessions,
               SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
               SUM(CASE WHEN status = 'Scheduled' THEN 1 ELSE 0 END) as scheduled,
               SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled
        FROM `tabTutor Session`
        GROUP BY month
        ORDER BY month DESC
    """, as_dict=True)
    return columns, data
