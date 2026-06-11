// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Session', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Status: <strong>${frm.doc.status}</strong>`,
                frm.doc.status === 'Completed' ? 'green' : 
                frm.doc.status === 'Cancelled' ? 'red' : 'blue'
            );
            
            frm.add_custom_button(__('Attendance'), function() {
                frappe.set_route('List', 'Attendance Record', {tutor_session: frm.doc.name});
            }, __('View'));
        }
    },
    
    start_time: function(frm) {
        frm.trigger('validate_times');
    },
    
    end_time: function(frm) {
        frm.trigger('validate_times');
    },
    
    validate_times: function(frm) {
        if (frm.doc.start_time && frm.doc.end_time) {
            if (frm.doc.start_time >= frm.doc.end_time) {
                frappe.msgprint(__('Start Time must be before End Time'));
            }
        }
    }
});
