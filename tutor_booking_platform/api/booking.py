# -*- coding: utf-8 -*-
"""Booking API endpoints for Tutor Booking Platform website."""
import frappe
from frappe import _

@frappe.whitelist()
def create_booking():
    """Create a new tutor booking."""
    try:
        data = frappe.local.form_dict
        
        # Validate required fields
        required = ['booking_title', 'tutor_profile', 'subject', 'teaching_mode', 'start_date', 'rate_per_hour']
        for field in required:
            if not data.get(field):
                frappe.throw(_(f"{field.replace('_', ' ').title()} is required"))
        
        # Get student profile for current user
        student_name = frappe.db.get_value('Student Profile', {'user': frappe.session.user}, 'name')
        if not student_name:
            frappe.throw(_('Student profile not found. Please register as a student first.'))
        
        booking = frappe.get_doc({
            'doctype': 'Tutor Booking',
            'booking_title': data.get('booking_title'),
            'student_profile': student_name,
            'tutor_profile': data.get('tutor_profile'),
            'subject': data.get('subject'),
            'teaching_mode': data.get('teaching_mode'),
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
            'sessions_per_week': data.get('sessions_per_week'),
            'hours_per_session': data.get('hours_per_session'),
            'rate_per_hour': data.get('rate_per_hour'),
            'total_hours': data.get('total_hours'),
            'special_instructions': data.get('special_instructions'),
            'booking_status': 'Pending'
        })
        booking.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            'message': _(f'Booking {booking.name} created successfully!'),
            'redirect_url': '/dashboard',
            'booking_name': booking.name,
            'status': 'success'
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.throw(_(str(e)))
