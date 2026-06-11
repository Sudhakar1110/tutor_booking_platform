// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Rating', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Rating: ${frm.doc.overall_rating}/5`);
        }
    },
    
    overall_rating: function(frm) {
        if (frm.doc.overall_rating) {
            frappe.model.set_value(frm.doctype, frm.docname, 'subject_knowledge', frm.doc.overall_rating);
            frappe.model.set_value(frm.doctype, frm.docname, 'teaching_methodology', frm.doc.overall_rating);
            frappe.model.set_value(frm.doctype, frm.docname, 'punctuality', frm.doc.overall_rating);
            frappe.model.set_value(frm.doctype, frm.docname, 'communication_skills', frm.doc.overall_rating);
        }
    }
});
