# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
class ChatMessage(Document):
    def before_insert(self):
        if not self.sent_at:
            self.sent_at = now_datetime()
    def after_insert(self):
        if self.message_thread:
            frappe.db.set_value("Message Thread", self.message_thread,
                                "last_message_date", self.sent_at, update_modified=False)
