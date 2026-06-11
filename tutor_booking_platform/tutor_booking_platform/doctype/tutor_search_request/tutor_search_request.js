// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Search Request', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('View Matches'), function() {
                frappe.set_route('List', 'Tutor Match Result', {search_request: frm.doc.name});
            }, __('View'));
        }
    }
});
