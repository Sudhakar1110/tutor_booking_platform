import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "booking_month", "label": _("Month"), "fieldtype": "Data", "width": 120},
        {"fieldname": "total_bookings", "label": _("Total"), "fieldtype": "Int", "width": 100},
        {"fieldname": "confirmed", "label": _("Confirmed"), "fieldtype": "Int", "width": 100},
        {"fieldname": "completed", "label": _("Completed"), "fieldtype": "Int", "width": 100},
        {"fieldname": "cancelled", "label": _("Cancelled"), "fieldtype": "Int", "width": 100},
    ]
    data = frappe.db.sql("""
        SELECT DATE_FORMAT(creation, '%Y-%m') as booking_month,
               COUNT(*) as total_bookings,
               SUM(CASE WHEN booking_status = 'Confirmed' THEN 1 ELSE 0 END) as confirmed,
               SUM(CASE WHEN booking_status = 'Completed' THEN 1 ELSE 0 END) as completed,
               SUM(CASE WHEN booking_status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled
        FROM `tabTutor Booking`
        GROUP BY booking_month
        ORDER BY booking_month DESC
    """, as_dict=True)
    return columns, data
