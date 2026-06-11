// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Demo Class Schedule', {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.meeting_link) {
            frm.add_web_link(frm.doc.meeting_link, __('Join Meeting'));
        }
    }
});
