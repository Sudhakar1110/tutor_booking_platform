# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class DemoClassRequest(Document):
    def validate(self):
        if not self.subject:
            frappe.throw(_("Subject is mandatory."))
    def on_submit(self):
        self.status = "Approved"
        frappe.db.set_value("Demo Class Request", self.name, "status", "Approved")