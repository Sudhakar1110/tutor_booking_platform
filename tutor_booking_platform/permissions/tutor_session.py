# -*- coding: utf-8 -*-
import frappe


def get_permission_query_conditions(user=None):
    if not user:
        user = frappe.session.user
    if "Tutor Booking Manager" in frappe.get_roles(user) or "System Manager" in frappe.get_roles(user):
        return ""
    if "Tutor" in frappe.get_roles(user):
        tutor = frappe.db.get_value("Tutor Profile", {"user": user}, "name")
        if tutor:
            return f"\`tabTutor Session\`.\`tutor_profile\` = '{tutor}'"
    if "Student" in frappe.get_roles(user):
        student = frappe.db.get_value("Student Profile", {"user": user}, "name")
        if student:
            return f"\`tabTutor Session\`.\`student_profile\` = '{student}'"
    return "1=0"