# -*- coding: utf-8 -*-
"""Context provider for Tutor Detail page."""
import frappe


def get_context(context):
    """Provide tutor details to the template."""
    tutor_name = frappe.form_dict.get('name')
    
    if tutor_name:
        try:
            tutor = frappe.get_doc('Tutor Profile', tutor_name)
            context.tutor = tutor
            
            # Fetch related data
            context.qualifications = frappe.get_all(
                'Tutor Qualification',
                filters={'tutor_profile': tutor_name},
                fields=['degree', 'field_of_study', 'institution', 'passing_year']
            )
            context.experiences = frappe.get_all(
                'Tutor Experience',
                filters={'tutor_profile': tutor_name},
                fields=['role_title', 'organization_name', 'from_date', 'to_date', 'description']
            )
            context.certifications = frappe.get_all(
                'Tutor Certification',
                filters={'tutor_profile': tutor_name},
                fields=['certification_name', 'issuing_authority', 'issue_date']
            )
            context.reviews = frappe.get_all(
                'Tutor Review',
                filters={'tutor_profile': tutor_name, 'is_approved': 1},
                fields=['student_profile', 'review_title', 'review_text', 'rating', 
                        'tutor_response', 'review_date', 'student_name']
            )
            context.availability = frappe.get_all(
                'Tutor Availability',
                filters={'tutor_profile': tutor_name, 'is_available': 1},
                fields=['day_of_week', 'start_time', 'end_time']
            )
        except Exception:
            context.tutor = None
    else:
        context.tutor = None
