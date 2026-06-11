// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Message Thread', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View Messages'), function() {
                frappe.set_route('List', 'Chat Message', {message_thread: frm.doc.name});
            }, __('View'));
        }
    }
});
