// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Qualification', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Degree: ${frm.doc.degree} | Institution: ${frm.doc.institution}`);
        }
    },
    
    passing_year: function(frm) {
        if (frm.doc.passing_year && frm.doc.passing_year > new Date().getFullYear()) {
            frappe.msgprint(__('Passing year cannot be in the future'));
        }
    }
});
