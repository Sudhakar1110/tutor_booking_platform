// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Card Payment', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Card: ****${frm.doc.card_last_four} | Type: ${frm.doc.card_type}`);
        }
    }
});
