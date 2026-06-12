# -*- coding: utf-8 -*-
"""Contact API endpoints for Tutor Booking Platform website."""
import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def submit_contact():
    """Submit a contact form inquiry."""
    try:
        data = frappe.local.form_dict
        
        required = ['full_name', 'email', 'subject', 'message']
        for field in required:
            if not data.get(field):
                frappe.throw(_(f"{field.replace('_', ' ').title()} is required"))
        
        # Create a notification or log
        frappe.get_doc({
            'doctype': 'Notification Log',
            'subject': f"Contact Form: {data.get('subject')}",
            'message': f"From: {data.get('full_name')} ({data.get('email')})\nPhone: {data.get('phone', 'N/A')}\n\n{data.get('message')}",
            'notification_type': 'Alert',
            'status': 'Pending'
        }).insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            'message': _('Thank you! Your message has been received. We will get back to you shortly.'),
            'status': 'success'
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.throw(_(str(e)))
