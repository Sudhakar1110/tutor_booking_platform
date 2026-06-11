# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
class NotificationLog(Document):
    def before_save(self):
        if self.status == "Sent" and not self.sent_at:
            self.sent_at = now_datetime()