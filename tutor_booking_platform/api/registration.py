# -*- coding: utf-8 -*-
"""Registration API endpoints for Tutor Booking Platform website."""
import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def register_student():
    """Register a new student."""
    try:
        data = frappe.local.form_dict
        
        # Validate required fields
        required = ['student_name', 'email', 'mobile', 'password']
        for field in required:
            if not data.get(field):
                frappe.throw(_(f"{field.replace('_', ' ').title()} is required"))
        
        # Create User
        user = frappe.get_doc({
            'doctype': 'User',
            'email': data.get('email'),
            'first_name': data.get('student_name'),
            'mobile_no': data.get('mobile'),
            'send_welcome_email': 0,
            'roles': [{'role': 'Student'}],
            'new_password': data.get('password')
        })
        user.insert(ignore_permissions=True)
        
        # Create Student Profile
        student = frappe.get_doc({
            'doctype': 'Student Profile',
            'student_name': data.get('student_name'),
            'email': data.get('email'),
            'mobile': data.get('mobile'),
            'user': user.name,
            'current_class': data.get('current_class'),
            'school_college': data.get('school_college'),
            'preferred_learning_mode': data.get('preferred_learning_mode'),
            'preferred_timing': data.get('preferred_timing'),
            'budget_per_hour': data.get('budget_per_hour'),
            'parent_name': data.get('parent_name'),
            'is_active': 1
        })
        student.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            'message': _('Registration successful! Please login.'),
            'redirect_url': '/login',
            'status': 'success'
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.throw(_(str(e)))

@frappe.whitelist(allow_guest=True)
def register_tutor():
    """Register a new tutor."""
    try:
        data = frappe.local.form_dict
        
        # Validate required fields
        required = ['tutor_name', 'email', 'mobile', 'password', 'primary_subject', 
                    'experience_years', 'hourly_rate', 'teaching_mode', 'short_bio']
        for field in required:
            if not data.get(field):
                frappe.throw(_(f"{field.replace('_', ' ').title()} is required"))
        
        # Create User
        user = frappe.get_doc({
            'doctype': 'User',
            'email': data.get('email'),
            'first_name': data.get('tutor_name'),
            'mobile_no': data.get('mobile'),
            'send_welcome_email': 0,
            'roles': [{'role': 'Tutor'}],
            'new_password': data.get('password')
        })
        user.insert(ignore_permissions=True)
        
        # Create Tutor Profile
        tutor = frappe.get_doc({
            'doctype': 'Tutor Profile',
            'tutor_name': data.get('tutor_name'),
            'email': data.get('email'),
            'mobile': data.get('mobile'),
            'user': user.name,
            'primary_subject': data.get('primary_subject'),
            'experience_years': data.get('experience_years'),
            'hourly_rate': data.get('hourly_rate'),
            'teaching_mode': data.get('teaching_mode'),
            'city': data.get('city'),
            'short_bio': data.get('short_bio'),
            'teaching_levels': data.get('teaching_levels'),
            'languages_known': data.get('languages_known'),
            'verification_status': 'Pending',
            'is_active': 1
        })
        tutor.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            'message': _('Registration successful! Your profile will be verified shortly.'),
            'redirect_url': '/login',
            'status': 'success'
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.throw(_(str(e)))
