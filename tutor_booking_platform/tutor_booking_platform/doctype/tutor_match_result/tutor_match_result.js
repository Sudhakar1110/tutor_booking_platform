// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Match Result', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Match Score: ${frm.doc.match_score || 0}% | Status: ${frm.doc.status}`,
                frm.doc.match_score >= 80 ? 'green' : 
                frm.doc.match_score >= 60 ? 'blue' : 'orange'
            );
        }
    }
});
