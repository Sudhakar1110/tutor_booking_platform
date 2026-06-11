# -*- coding: utf-8 -*-
from frappe.model.document import Document
from frappe.utils import today
class StudentFeedback(Document):
    def validate(self):
        if not self.feedback_date:
            self.feedback_date = today()
