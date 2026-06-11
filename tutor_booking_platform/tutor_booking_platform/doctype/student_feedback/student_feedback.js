// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Feedback', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Overall: ${frm.doc.overall_experience}`,
                frm.doc.overall_experience === 'Excellent' ? 'green' : 
                frm.doc.overall_experience === 'Good' ? 'blue' : 'orange'
            );
        }
    }
});
