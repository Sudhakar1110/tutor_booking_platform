# -*- coding: utf-8 -*-
import frappe


def get_tutor_rating(tutor_profile):
    """Return average rating for a tutor."""
    result = frappe.db.sql("""
        SELECT AVG(overall_rating) as avg_rating, COUNT(name) as total_reviews
        FROM \`tabTutor Rating\`
        WHERE tutor_profile = %s AND docstatus = 1
    """, tutor_profile, as_dict=True)
    if result:
        return {
            "avg_rating": round(result[0].avg_rating or 0, 2),
            "total_reviews": result[0].total_reviews or 0,
        }
    return {"avg_rating": 0, "total_reviews": 0}


def get_session_count(tutor_profile):
    """Return total completed sessions for a tutor."""
    return frappe.db.count("Tutor Session", {
        "tutor_profile": tutor_profile,
        "status": "Completed",
        "docstatus": 1,
    })