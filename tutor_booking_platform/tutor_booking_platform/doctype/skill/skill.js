// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Skill', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Category: ${frm.doc.skill_category}`);
        }
    }
});
