# -*- coding: utf-8 -*-
import frappe
from frappe.model.document import Document
from frappe import _
import re

class StudentProfile(Document):
    def validate(self):
        self._validate_email()
        self._validate_mobile()

    def before_save(self):
        if not self.user and self.email:
            user = frappe.db.get_value("User", {"email": self.email}, "name")
            if user:
                self.user = user

    def _validate_email(self):
        if self.email and not re.match(r'^[\\w.+-]+@[\\w-]+\\.[\\w.]+$', self.email):
            frappe.throw(_("Invalid email address: {0}").format(self.email))

    def _validate_mobile(self):
        if self.mobile:
            mobile = self.mobile.strip().replace(" ", "")
            if not mobile.replace("+", "").replace("-", "").isdigit():
                frappe.throw(_("Invalid mobile number: {0}").format(self.mobile))