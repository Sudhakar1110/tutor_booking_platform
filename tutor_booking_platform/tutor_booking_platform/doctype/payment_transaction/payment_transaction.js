// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Transaction', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Status: <strong>${frm.doc.payment_status}</strong> | 
                 Amount: <strong>${format_currency(frm.doc.amount, 'INR')}</strong>`,
                frm.doc.payment_status === 'Completed' ? 'green' : 
                frm.doc.payment_status === 'Failed' ? 'red' : 'blue'
            );
        }
    },
    
    amount: function(frm) {
        if (frm.doc.amount && frm.doc.amount > 0) {
            frm.set_value('platform_commission', frm.doc.amount * (frm.doc.commission_percentage || 10) / 100);
            frm.set_value('tutor_payout', frm.doc.amount - (frm.doc.platform_commission || 0));
        }
    }
});
