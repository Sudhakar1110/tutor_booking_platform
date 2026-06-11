# -*- coding: utf-8 -*-
"""
tutor_booking_platform/install.py
Installation, migration and uninstall hooks for Tutor Booking Platform
"""
import frappe
from frappe import _


def after_install():
    """Run after app installation."""
    frappe.db.commit()
    create_roles()
    create_default_settings()
    create_module_def()
    frappe.db.commit()
    frappe.clear_cache()
    print("✅ Tutor Booking Platform installed successfully.")


def after_migrate():
    """Run after bench migrate."""
    create_default_settings()
    clean_workspace()
    fix_child_table_modules()
    frappe.db.commit()
    frappe.clear_cache()
    print("✅ Tutor Booking Platform migration completed.")


def before_uninstall():
    """Run before app uninstall — clean up records."""
    try:
        # Remove settings doc if exists
        if frappe.db.exists("Tutor Booking Settings", "Tutor Booking Settings"):
            frappe.delete_doc("Tutor Booking Settings", "Tutor Booking Settings",
                              ignore_permissions=True, force=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(str(e), "Tutor Booking Platform Uninstall Error")
    print("✅ Tutor Booking Platform uninstalled cleanly.")


def create_roles():
    """Create custom roles required by the app."""
    roles = [
        {"role_name": "Tutor Booking Manager", "desk_access": 1},
        {"role_name": "Tutor",                 "desk_access": 1},
        {"role_name": "Student",               "desk_access": 0},
        {"role_name": "Tutor Booking Operator","desk_access": 1},
    ]
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.get_doc({"doctype": "Role", **role_data})
            role.insert(ignore_permissions=True)
    frappe.db.commit()


def create_default_settings():
    """Create default Tutor Booking Settings if not exists."""
    if not frappe.db.exists("Tutor Booking Settings", "Tutor Booking Settings"):
        try:
            doc = frappe.get_doc({
                "doctype": "Tutor Booking Settings",
                "platform_name": "Tutor Booking Platform",
                "default_currency": "INR",
                "commission_percentage": 10.0,
                "min_session_duration": 60,
                "max_advance_booking_days": 30,
                "enable_demo_class": 1,
                "enable_online_class": 1,
                "enable_offline_class": 1,
                "enable_upi_payment": 1,
                "enable_card_payment": 1,
                "enable_cash_payment": 1,
                "auto_confirm_booking": 0,
                "session_reminder_hours": 24,
                "rating_mandatory_after_session": 1,
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(str(e), "Create Default Settings Error")


def create_module_def():
    """Ensure Module Def exists for Tutor Booking Platform."""
    if not frappe.db.exists("Module Def", "Tutor Booking Platform"):
        try:
            module = frappe.get_doc({
                "doctype": "Module Def",
                "module_name": "Tutor Booking Platform",
                "app_name": "tutor_booking_platform",
            })
            module.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(str(e), "Create Module Def Error")


def clean_workspace():
    """Remove any cross-app doctypes from Tutor Booking Platform workspace."""
    try:
        workspace_name = "Tutor Booking Platform"
        if not frappe.db.exists("Workspace", workspace_name):
            return

        workspace = frappe.get_doc("Workspace", workspace_name)
        allowed_modules = ["Tutor Booking Platform"]
        changed = False

        # Clean shortcuts
        for s in list(workspace.shortcuts):
            if s.link_to and s.link_type == "DocType":
                try:
                    meta = frappe.get_meta(s.link_to)
                    if meta.module not in allowed_modules:
                        workspace.shortcuts.remove(s)
                        changed = True
                        print(f"  Removed shortcut: {s.label} (from {meta.module})")
                except Exception:
                    pass

        # Clean links
        for l in list(workspace.links):
            if l.link_to and l.link_type == "DocType":
                try:
                    meta = frappe.get_meta(l.link_to)
                    if meta.module not in allowed_modules:
                        workspace.links.remove(l)
                        changed = True
                        print(f"  Removed link: {l.label} (from {meta.module})")
                except Exception:
                    pass

        if changed:
            workspace.save(ignore_permissions=True)
            frappe.db.commit()
            print("✅ Workspace cleaned - cross-app doctypes removed")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "clean_workspace Error")


def fix_child_table_modules():
    """Fix module assignment for child table doctypes."""
    child_tables = [
        "Student Address",
        "Student Preference",
        "Tutor Qualification",
        "Tutor Experience",
        "Tutor Certification",
        "Tutor Availability",
        "Learning Schedule",
        "Learning Progress",
        "Attendance Record",
        "UPI Payment",
        "Card Payment",
        "Cash Payment",
        "Notification Log",
        "Message Thread",
        "Chat Message",
        "Reminder Schedule",
        "Tutor Rating",
        "Student Feedback",
    ]
    for dt_name in child_tables:
        try:
            if frappe.db.exists("DocType", dt_name):
                frappe.db.set_value("DocType", dt_name, "module", "Tutor Booking Platform")
        except Exception:
            pass
    print("✅ Fixed module for child table doctypes")