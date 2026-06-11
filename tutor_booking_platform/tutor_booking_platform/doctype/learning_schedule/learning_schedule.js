// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Learning Schedule', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`${frm.doc.day_of_week}: ${frm.doc.start_time} - ${frm.doc.end_time}`);
        }
    }
});
