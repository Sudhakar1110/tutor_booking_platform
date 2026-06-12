# -*- coding: utf-8 -*-
"""Demo Class API endpoints for Tutor Booking Platform website."""
import frappe
from frappe import _

@frappe.whitelist()
def request_demo():
    """Request a demo class."""
    try:
        data = frappe.local.form_dict
        
        # Validate required fields
        required = ['student_profile', 'tutor_profile', 'subject', 'preferred_date', 'preferred_time']
        for field in required:
            if not data.get(field):
                frappe.throw(_(f"{field.replace('_', ' ').title()} is required"))
        
        demo = frappe.get_doc({
            'doctype': 'Demo Class Request',
            'student_profile': data.get('student_profile'),
            'tutor_profile': data.get('tutor_profile'),
            'subject': data.get('subject'),
            'preferred_date': data.get('preferred_date'),
            'preferred_time': data.get('preferred_time'),
            'alternate_date': data.get('alternate_date'),
            'alternate_time': data.get('alternate_time'),
            'mode': data.get('mode', 'Online'),
            'message': data.get('message'),
            'status': 'Pending'
        })
        demo.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            'message': _('Demo class request submitted successfully!'),
            'redirect_url': '/dashboard',
            'status': 'success'
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.throw(_(str(e)))
