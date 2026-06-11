// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Booking Settings', {
    refresh: function(frm) {
        frm.set_intro(__('Configure platform-wide settings for the Tutor Booking Platform'));
    },
    
    commission_percentage: function(frm) {
        if (frm.doc.commission_percentage > 100) {
            frappe.msgprint(__('Commission percentage cannot exceed 100%'));
            frm.set_value('commission_percentage', 100);
        }
    }
});
