// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Notification Log', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Status: <strong>${frm.doc.status}</strong>`,
                frm.doc.status === 'Sent' ? 'green' : 
                frm.doc.status === 'Failed' ? 'red' : 'orange'
            );
        }
    }
});
