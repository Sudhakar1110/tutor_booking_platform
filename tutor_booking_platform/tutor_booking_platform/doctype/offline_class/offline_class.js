// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Offline Class', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Location: ${frm.doc.location || 'Not specified'}`);
        }
    }
});
