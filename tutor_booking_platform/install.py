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
    frappe.clear_cache()
    create_roles()
    create_default_settings()
    create_module_def()
    clean_workspace()
    fix_doctype_modules()
    frappe.db.commit()
    frappe.clear_cache()
    print("✅ Tutor Booking Platform installed successfully.")


def after_migrate():
    """Run after bench migrate."""
    # Clear cache FIRST so get_meta() sees freshly-synced DocTypes
    frappe.clear_cache()
    create_default_settings()
    clean_workspace()
    fix_doctype_modules()
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
    """Remove any cross-app doctypes from Tutor Booking Platform workspace.
    Also removes links to doctypes that don't exist in the database.
    """
    try:
        workspace_name = "Tutor Booking Platform"
        if not frappe.db.exists("Workspace", workspace_name):
            return

        workspace = frappe.get_doc("Workspace", workspace_name)
        allowed_modules = ["Tutor Booking Platform"]
        changed = False

        # Clean shortcuts (shortcuts use 'type', not 'link_type')
        for s in list(workspace.shortcuts):
            link_to = s.link_to
            if not link_to:
                continue
            try:
                meta = frappe.get_meta(link_to)
                if hasattr(meta, 'module') and meta.module not in allowed_modules:
                    workspace.shortcuts.remove(s)
                    changed = True
                    print(f"  Removed shortcut: {s.label} (module: {meta.module})")
            except frappe.DoesNotExistError:
                # Doctype not in DB - remove it from workspace
                workspace.shortcuts.remove(s)
                changed = True
                print(f"  Removed shortcut (not in DB): {s.label} -> {link_to}")
            except Exception:
                pass

        # Clean links (links have 'link_type')
        for l in list(workspace.links):
            link_to = l.link_to
            if not link_to:
                continue
            # Skip non-DocType links (reports, card breaks, etc.)
            if not hasattr(l, 'link_type') or l.link_type != "DocType":
                continue
            try:
                meta = frappe.get_meta(link_to)
                if hasattr(meta, 'module') and meta.module not in allowed_modules:
                    workspace.links.remove(l)
                    changed = True
                    print(f"  Removed link: {l.label} (module: {meta.module})")
            except frappe.DoesNotExistError:
                # Doctype not in DB - remove it from workspace
                workspace.links.remove(l)
                changed = True
                print(f"  Removed link (not in DB): {l.label} -> {link_to}")
            except Exception:
                pass

        if changed:
            try:
                workspace.save(ignore_permissions=True)
                frappe.db.commit()
                print("✅ Workspace cleaned - cross-app doctypes removed")
            except frappe.LinkValidationError:
                # If still failing, force clear all links and reset from JSON
                print("  Link validation failed. Resetting workspace from JSON...")
                workspace.links = []
                workspace.shortcuts = []
                workspace.save(ignore_permissions=True)
                frappe.db.commit()
                print("✅ Workspace cleared. Will reload from JSON on next visit.")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "clean_workspace Error")


def fix_doctype_modules():
    """Ensure all Tutor Booking Platform doctypes have correct module assignment."""
    try:
        # Fix TBP doctypes that may have wrong module (e.g., from other app fixtures)
        tbp_app_doctypes = [
            "Attendance Record", "Card Payment", "Cash Payment", "Chat Message",
            "Course", "Course Category", "Demo Class Request", "Demo Class Schedule",
            "Learning Progress", "Learning Schedule", "Message Thread",
            "Notification Log", "Offline Class", "Online Class", "Payment Transaction",
            "Refund Request", "Reminder Schedule", "Skill", "Skill Category",
            "Student Address", "Student Feedback", "Student Preference",
            "Student Profile", "Student Requirement", "Subject", "Subject Category",
            "Tutor Availability", "Tutor Booking", "Tutor Booking Settings",
            "Tutor Certification", "Tutor Experience", "Tutor Match Result",
            "Tutor Profile", "Tutor Qualification", "Tutor Rating", "Tutor Review",
            "Tutor Search Request", "Tutor Session", "Tutor Verification", "UPI Payment",
        ]
        for dt in tbp_app_doctypes:
            if frappe.db.exists("DocType", dt):
                current_module = frappe.db.get_value("DocType", dt, "module")
                if current_module != "Tutor Booking Platform":
                    frappe.db.set_value("DocType", dt, "module", "Tutor Booking Platform")
                    print(f"  Fixed module for {dt}: '{current_module}' → 'Tutor Booking Platform'")
    except Exception as e:
        frappe.log_error(str(e), "fix_doctype_modules Error")
    print("✅ Fixed module for Tutor Booking Platform doctypes")