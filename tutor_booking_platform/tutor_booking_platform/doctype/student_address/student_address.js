// Copyright (c) 2025, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Address', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.set_intro(`${frm.doc.address_type}: ${frm.doc.city}, ${frm.doc.state || ''}`);
        }
    },
    
    is_default: function(frm) {
        if (frm.doc.is_default) {
            frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: "Student Address",
                    name: frm.doc.name,
                    fieldname: "is_default",
                    value: 1
                }
            });
        }
    }
});
