# -*- coding: utf-8 -*-
"""Monthly scheduled tasks."""
import frappe
from frappe.utils import today, add_months


def generate_revenue_report():
    """Generate monthly revenue summary."""
    try:
        month_start = add_months(today(), -1)
        result = frappe.db.sql("""
            SELECT SUM(amount) as total, COUNT(name) as count
            FROM `tabPayment Transaction`
            WHERE payment_status = 'Completed'
              AND docstatus = 1
              AND creation >= %s
        """, (month_start,), as_dict=True)
        total = result[0].total or 0 if result else 0
        count = result[0].count or 0 if result else 0
        frappe.log_error(
            f"Monthly Revenue: {total} | Transactions: {count}",
            "Monthly Revenue Report"
        )
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "generate_revenue_report Error")