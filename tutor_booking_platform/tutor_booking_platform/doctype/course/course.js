// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Category: ${frm.doc.course_category} | Level: ${frm.doc.level || 'All'}`);
        }
    }
});
