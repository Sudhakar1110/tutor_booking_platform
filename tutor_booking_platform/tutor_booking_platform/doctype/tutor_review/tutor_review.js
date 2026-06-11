// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Review', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Rating: ${frm.doc.overall_rating}/5`,
                frm.doc.overall_rating >= 4 ? 'green' : 
                frm.doc.overall_rating >= 3 ? 'blue' : 'orange'
            );
        }
    },
    
    overall_rating: function(frm) {
        if (frm.doc.overall_rating) {
            // Auto-set sub-ratings
            frappe.model.set_value(frm.doctype, frm.docname, 'teaching_quality', frm.doc.overall_rating);
            frappe.model.set_value(frm.doctype, frm.docname, 'punctuality', frm.doc.overall_rating);
            frappe.model.set_value(frm.doctype, frm.docname, 'communication', frm.doc.overall_rating);
        }
    }
});
