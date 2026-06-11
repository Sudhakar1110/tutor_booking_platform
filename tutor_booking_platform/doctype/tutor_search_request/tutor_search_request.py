# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class TutorSearchRequest(Document):
    def validate(self):
        if self.max_budget and self.max_budget < 0:
            frappe.throw(_("Budget cannot be negative."))

    def on_submit(self):
        self.status = "Searching"
        frappe.db.set_value("Tutor Search Request", self.name, "status", "Searching")
        self._auto_match_tutors()

    def _auto_match_tutors(self):
        """Auto-match tutors based on criteria."""
        filters = {"verification_status": "Verified", "is_active": 1}
        if self.subject:
            filters["primary_subject"] = self.subject
        if self.teaching_mode and self.teaching_mode != "Both":
            filters["teaching_mode"] = ["in", [self.teaching_mode, "Both"]]
        tutors = frappe.get_all("Tutor Profile", filters=filters,
                                fields=["name", "tutor_name", "hourly_rate", "average_rating"],
                                order_by="average_rating desc", limit=10)
        for t in tutors:
            try:
                frappe.get_doc({
                    "doctype": "Tutor Match Result",
                    "search_request": self.name,
                    "tutor_profile": t.name,
                    "match_score": t.average_rating * 20,
                    "status": "Suggested",
                }).insert(ignore_permissions=True)
            except Exception:
                pass