// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Payment', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Receipt: ${frm.doc.receipt_number || 'N/A'} | Status: ${frm.doc.status}`);
        }
    }
});
