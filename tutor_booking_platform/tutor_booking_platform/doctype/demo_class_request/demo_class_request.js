// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Demo Class Request', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Demo Class Schedule'), function() {
                frappe.set_route('List', 'Demo Class Schedule', {demo_class_request: frm.doc.name});
            }, __('View'));
        }
    }
});
