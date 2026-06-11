// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Experience', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Organization: ${frm.doc.organization_name} | Role: ${frm.doc.role_title}`);
        }
    },
    
    is_current: function(frm) {
        if (frm.doc.is_current) {
            frm.set_value('to_date', null);
        }
    }
});
