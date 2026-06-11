// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Certification', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Certification: ${frm.doc.certification_name} | Issued by: ${frm.doc.issuing_authority}`);
        }
    }
});
