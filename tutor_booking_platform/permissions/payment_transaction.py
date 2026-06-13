# -*- coding: utf-8 -*-
import frappe


def get_permission_query_conditions(user=None):
    """Restrict Payment Transaction visibility by role.

    - Administrators / System Managers: see all
    - Tutor Booking Managers: see all
    - Tutors: see payments for their own bookings
    - Students: see only their own payments
    - Everyone else: see nothing
    """
    if not user:
        user = frappe.session.user

    if user == "Guest":
        return "1=0"

    roles = frappe.get_roles(user)

    if "System Manager" in roles or "Tutor Booking Manager" in roles:
        return ""

    if "Tutor" in roles:
        tutor = frappe.db.get_value("Tutor Profile", {"user": user}, "name")
        if tutor:
            return f"`tabPayment Transaction`.`tutor_profile` = {frappe.db.escape(tutor)}"

    if "Student" in roles:
        student = frappe.db.get_value("Student Profile", {"user": user}, "name")
        if student:
            return f"`tabPayment Transaction`.`student_profile` = {frappe.db.escape(student)}"

    return "1=0"