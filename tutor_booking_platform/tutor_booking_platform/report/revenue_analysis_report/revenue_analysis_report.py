import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "month", "label": _("Month"), "fieldtype": "Data", "width": 120},
        {"fieldname": "total_revenue", "label": _("Revenue"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "commission", "label": _("Commission"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "payout", "label": _("Payout"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "transactions", "label": _("Transactions"), "fieldtype": "Int", "width": 100},
    ]
    data = frappe.db.sql("""
        SELECT DATE_FORMAT(creation, '%Y-%m') as month,
               SUM(amount) as total_revenue,
               SUM(platform_commission) as commission,
               SUM(tutor_payout) as payout,
               COUNT(*) as transactions
        FROM `tabPayment Transaction`
        WHERE docstatus = 1
        GROUP BY month
        ORDER BY month DESC
    """, as_dict=True)
    return columns, data
