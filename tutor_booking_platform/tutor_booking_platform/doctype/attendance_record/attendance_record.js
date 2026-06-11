// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Record', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`Session: ${frm.doc.tutor_session}`);
        }
    }
});
