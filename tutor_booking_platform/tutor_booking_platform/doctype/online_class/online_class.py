# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class OnlineClass(Document):
    def validate(self):
        if not self.meeting_link:
            frappe.throw(_("Meeting Link is mandatory for online classes."))
    def on_submit(self):
        self.status = "Completed"
        frappe.db.set_value("Online Class", self.name, "status", "Completed")
