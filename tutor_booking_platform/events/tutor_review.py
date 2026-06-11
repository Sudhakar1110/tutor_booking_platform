# -*- coding: utf-8 -*-
"""Document events for Tutor Review DocType."""
import frappe
from frappe import _


def validate(doc, method=None):
    if doc.rating and (doc.rating < 1 or doc.rating > 5):
        frappe.throw(_("Rating must be between 1 and 5."))


def after_insert(doc, method=None):
    _update_tutor_rating(doc.tutor_profile)


def _update_tutor_rating(tutor_profile):
    try:
        result = frappe.db.sql("""
            SELECT AVG(rating) as avg_rating
            FROM \`tabTutor Review\`
            WHERE tutor_profile = %s
        """, tutor_profile, as_dict=True)
        avg = round(result[0].avg_rating or 0, 2) if result else 0
        frappe.db.set_value("Tutor Profile", tutor_profile, "average_rating", avg,
                            update_modified=False)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(str(e), "Update Tutor Rating Error")