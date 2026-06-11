// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subject', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Category: ${frm.doc.subject_category} | Audience: ${frm.doc.target_audience || 'All'}`);
        }
    }
});
