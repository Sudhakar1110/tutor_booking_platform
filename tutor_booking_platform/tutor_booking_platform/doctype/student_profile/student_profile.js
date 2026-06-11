// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Profile', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Student Requirements'), function() {
                frappe.set_route('List', 'Student Requirement', {student_profile: frm.doc.name});
            }, __('View'));
            
            frm.add_custom_button(__('Tutor Bookings'), function() {
                frappe.set_route('List', 'Tutor Booking', {student_profile: frm.doc.name});
            }, __('View'));
            
            frm.add_custom_button(__('Tutor Reviews'), function() {
                frappe.set_route('List', 'Tutor Review', {student_profile: frm.doc.name});
            }, __('View'));
        }
    }
});
