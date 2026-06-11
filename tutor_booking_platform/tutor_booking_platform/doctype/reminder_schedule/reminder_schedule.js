// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reminder Schedule', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Type: ${frm.doc.reminder_type} | Frequency: ${frm.doc.frequency}`,
                frm.doc.is_active ? 'green' : 'gray'
            );
        }
    }
});
