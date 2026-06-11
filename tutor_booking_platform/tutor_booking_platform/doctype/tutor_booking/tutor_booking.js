// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Booking', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(
                `Status: <strong>${frm.doc.booking_status}</strong> | 
                 Total: <strong>${format_currency(frm.doc.total_amount, frm.doc.currency || 'INR')}</strong>`,
                frm.doc.booking_status === 'Confirmed' ? 'green' : 
                frm.doc.booking_status === 'Cancelled' ? 'red' : 'blue'
            );
            
            frm.add_custom_button(__('Tutor Sessions'), function() {
                frappe.set_route('List', 'Tutor Session', {tutor_booking: frm.doc.name});
            }, __('View'));
            
            frm.add_custom_button(__('Payments'), function() {
                frappe.set_route('List', 'Payment Transaction', {tutor_booking: frm.doc.name});
            }, __('View'));
        }
    },
    
    total_hours: function(frm) {
        frm.trigger('calculate_total');
    },
    
    rate_per_hour: function(frm) {
        frm.trigger('calculate_total');
    },
    
    calculate_total: function(frm) {
        if (frm.doc.total_hours && frm.doc.rate_per_hour) {
            frm.set_value('total_amount', frm.doc.total_hours * frm.doc.rate_per_hour);
        }
    }
});
