// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Chat Message', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`From: ${frm.doc.sender} | ${frm.doc.sent_at || ''}`);
        }
    }
});
