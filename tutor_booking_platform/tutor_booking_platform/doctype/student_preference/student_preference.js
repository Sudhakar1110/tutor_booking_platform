// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Preference', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Goal: ${frm.doc.learning_goal || 'Not specified'}`);
        }
    }
});
