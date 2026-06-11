// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Verification', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.verification_status === 'Verified') {
            frm.set_intro(__('✅ Tutor has been verified successfully'), 'green');
        } else if (frm.doc.docstatus === 1 && frm.doc.verification_status === 'Rejected') {
            frm.set_intro(__('❌ Tutor verification has been rejected'), 'red');
        }
    },
    
    verification_status: function(frm) {
        if (frm.doc.verification_status === 'Verified') {
            frm.set_value('verification_date', frappe.datetime.nowdate());
        }
    }
});
