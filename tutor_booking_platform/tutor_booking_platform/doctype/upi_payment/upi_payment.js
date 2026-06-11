// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('UPI Payment', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`UPI ID: ${frm.doc.upi_id} | Status: ${frm.doc.status}`);
        }
    }
});
