// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Refund Request', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Status: <strong>${frm.doc.refund_status}</strong> | 
                 Amount: <strong>${format_currency(frm.doc.refund_amount, 'INR')}</strong>`,
                frm.doc.refund_status === 'Processed' ? 'green' : 
                frm.doc.refund_status === 'Rejected' ? 'red' : 'orange'
            );
        }
    }
});
