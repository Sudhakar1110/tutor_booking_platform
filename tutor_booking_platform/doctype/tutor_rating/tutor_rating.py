# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import today
class TutorRating(Document):
    def validate(self):
        if self.overall_rating and (self.overall_rating < 1 or self.overall_rating > 5):
            frappe.throw(_("Overall rating must be between 1 and 5."))
        if not self.rating_date:
            self.rating_date = today()