// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tutor Profile', {
    refresh: function(frm) {
        // Set dashboard data
        if (!frm.is_new()) {
            frm.dashboard.set_headline_alert(
                `<span>Status: <strong>${frm.doc.verification_status}</strong> | 
                 Rating: <strong>${frm.doc.average_rating || 0}/5</strong> | 
                 Sessions: <strong>${frm.doc.total_sessions || 0}</strong></span>`
            );
            
            // Add custom buttons
            frm.add_custom_button(__('Tutor Bookings'), function() {
                frappe.set_route('List', 'Tutor Booking', {tutor_profile: frm.doc.name});
            }, __('View'));
            
            frm.add_custom_button(__('Tutor Sessions'), function() {
                frappe.set_route('List', 'Tutor Session', {tutor_profile: frm.doc.name});
            }, __('View'));
            
            frm.add_custom_button(__('Tutor Reviews'), function() {
                frappe.set_route('List', 'Tutor Review', {tutor_profile: frm.doc.name});
            }, __('View'));
        }
    },
    
    tutor_name: function(frm) {
        // Auto-set naming series if empty
        if (!frm.doc.naming_series) {
            frm.set_value('naming_series', 'TUT-.YYYY.-.####');
        }
    }
});
