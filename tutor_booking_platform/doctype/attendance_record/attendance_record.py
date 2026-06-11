# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _

class AttendanceRecord(Document):
    def validate(self):
        if not self.tutor_session:
            frappe.throw(_("Tutor Session reference is mandatory."))
    def on_submit(self):
        self._update_progress()
    def _update_progress(self):
        try:
            existing = frappe.db.get_value("Learning Progress", {
                "student_profile": self.student_profile,
                "subject": self.subject,
            }, "name")
            if existing:
                pdoc = frappe.get_doc("Learning Progress", existing)
                if self.status == "Present":
                    pdoc.sessions_attended = (pdoc.sessions_attended or 0) + 1
                pdoc.sessions_completed = (pdoc.sessions_completed or 0) + 1
                pdoc.save(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(str(e), "Update Learning Progress Error")