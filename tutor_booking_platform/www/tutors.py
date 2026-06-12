# -*- coding: utf-8 -*-
"""Context provider for Tutors listing page."""
import frappe


def get_context(context):
    """Provide tutor listing data to the template."""
    filters = {'is_active': 1}
    
    # Apply filters from query params
    subject = frappe.form_dict.get('subject')
    city = frappe.form_dict.get('city')
    mode = frappe.form_dict.get('mode')
    sort = frappe.form_dict.get('sort', 'rating')
    
    if subject:
        filters['primary_subject'] = subject
    if city:
        filters['city'] = city
    if mode:
        filters['teaching_mode'] = ['in', [mode, 'Both']]
    
    # Get tutors
    tutors = frappe.get_all(
        'Tutor Profile',
        filters=filters,
        fields=['name', 'tutor_name', 'primary_subject', 'city', 'experience_years',
                'hourly_rate', 'average_rating', 'teaching_mode', 'profile_image', 'short_bio']
    )
    
    # Sort
    if sort == 'rate_low':
        tutors.sort(key=lambda t: t.hourly_rate or 0)
    elif sort == 'rate_high':
        tutors.sort(key=lambda t: t.hourly_rate or 0, reverse=True)
    elif sort == 'experience':
        tutors.sort(key=lambda t: t.experience_years or 0, reverse=True)
    else:
        tutors.sort(key=lambda t: t.average_rating or 0, reverse=True)
    
    context.tutors = tutors
