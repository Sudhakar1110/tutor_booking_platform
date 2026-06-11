// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Requirement', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Search Tutors'), function() {
                frappe.set_route('List', 'Tutor Search Request', {student_profile: frm.doc.student_profile});
            }, __('View'));
        }
    }
});
