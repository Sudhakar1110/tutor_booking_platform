// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course Category', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View Courses'), function() {
                frappe.set_route('List', 'Course', {course_category: frm.doc.name});
            }, __('View'));
        }
    }
});
