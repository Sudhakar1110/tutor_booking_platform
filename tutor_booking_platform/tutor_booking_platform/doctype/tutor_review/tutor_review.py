# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import today

class TutorReview(Document):
    def validate(self):
        if self.rating and (self.rating < 1 or self.rating > 5):
            frappe.throw(_("Rating must be between 1 and 5."))
        if not self.review_date:
            self.review_date = today()
    def after_insert(self):
        self._update_tutor_avg()
    def _update_tutor_avg(self):
        try:
            result = frappe.db.sql("""
                SELECT AVG(rating) as avg FROM `tabTutor Review`
                WHERE tutor_profile = %s
            """, self.tutor_profile, as_dict=True)
            avg = round(result[0].avg or 0, 2) if result else 0
            frappe.db.set_value("Tutor Profile", self.tutor_profile, "average_rating", avg,
                                update_modified=False)
        except Exception as e:
            frappe.log_error(str(e), "Update Tutor Rating Error")
