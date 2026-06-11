# -*- coding: utf-8 -*-
# Tutor Booking Platform — hooks.py
# Frappe v15 + ERPNext v15 Compatible

from . import __version__ as app_version

app_name        = "tutor_booking_platform"
app_title       = "Tutor Booking Platform"
app_publisher   = "Antigravity"
app_description = "A production-ready Tutor Booking Platform similar to UrbanPro, built on Frappe Framework v15 and ERPNext v15"
app_email       = "info@antigravity.dev"
app_license     = "MIT"
app_version     = app_version

# ─── Required Apps ────────────────────────────────────────────────────────────
required_apps = ["erpnext"]

# ─── Fixtures ─────────────────────────────────────────────────────────────────
fixtures = [
    {"dt": "Role", "filters": [["name", "in", [
        "Tutor Booking Manager",
        "Tutor",
        "Student",
        "Tutor Booking Operator",
    ]]]},
    {"dt": "Workflow", "filters": [["name", "in", [
        "Tutor Verification Workflow",
        "Demo Class Approval Workflow",
        "Tutor Booking Approval Workflow",
        "Refund Approval Workflow",
    ]]]},
    {"dt": "Notification", "filters": [["name", "in", [
        "New Student Enquiry",
        "Demo Class Scheduled",
        "Demo Class Completed",
        "Booking Confirmed",
        "Booking Cancelled",
        "Session Reminder",
        "Payment Received",
        "Refund Approved",
        "Tutor Verification Approved",
        "Tutor Verification Rejected",
    ]]]},
    {"dt": "Custom Field"},
    {"dt": "Property Setter"},
]

# ─── Installation / Migration Hooks ───────────────────────────────────────────
after_install  = "tutor_booking_platform.install.after_install"
after_migrate  = "tutor_booking_platform.install.after_migrate"
before_uninstall = "tutor_booking_platform.install.before_uninstall"

# ─── Scheduler Events ─────────────────────────────────────────────────────────
scheduler_events = {
    "daily": [
        "tutor_booking_platform.tasks.daily.send_session_reminders",
        "tutor_booking_platform.tasks.daily.auto_close_expired_bookings",
        "tutor_booking_platform.tasks.daily.send_demo_class_reminders",
        "tutor_booking_platform.tasks.daily.update_tutor_ratings",
    ],
    "hourly": [
        "tutor_booking_platform.tasks.hourly.process_pending_notifications",
        "tutor_booking_platform.tasks.hourly.check_session_status",
    ],
    "weekly": [
        "tutor_booking_platform.tasks.weekly.generate_weekly_report",
        "tutor_booking_platform.tasks.weekly.send_tutor_performance_summary",
    ],
    "monthly": [
        "tutor_booking_platform.tasks.monthly.generate_revenue_report",
    ],
}

# ─── Document Events ──────────────────────────────────────────────────────────
doc_events = {
    "Tutor Booking": {
        "after_insert": "tutor_booking_platform.events.tutor_booking.after_insert",
        "on_submit":    "tutor_booking_platform.events.tutor_booking.on_submit",
        "on_cancel":    "tutor_booking_platform.events.tutor_booking.on_cancel",
        "validate":     "tutor_booking_platform.events.tutor_booking.validate",
    },
    "Tutor Session": {
        "after_insert": "tutor_booking_platform.events.tutor_session.after_insert",
        "on_submit":    "tutor_booking_platform.events.tutor_session.on_submit",
        "validate":     "tutor_booking_platform.events.tutor_session.validate",
    },
    "Payment Transaction": {
        "on_submit":    "tutor_booking_platform.events.payment_transaction.on_submit",
        "on_cancel":    "tutor_booking_platform.events.payment_transaction.on_cancel",
        "validate":     "tutor_booking_platform.events.payment_transaction.validate",
    },
    "Demo Class Request": {
        "after_insert": "tutor_booking_platform.events.demo_class_request.after_insert",
        "on_submit":    "tutor_booking_platform.events.demo_class_request.on_submit",
        "validate":     "tutor_booking_platform.events.demo_class_request.validate",
    },
    "Tutor Review": {
        "after_insert": "tutor_booking_platform.events.tutor_review.after_insert",
        "validate":     "tutor_booking_platform.events.tutor_review.validate",
    },
    "Attendance Record": {
        "on_submit":    "tutor_booking_platform.events.attendance_record.on_submit",
        "validate":     "tutor_booking_platform.events.attendance_record.validate",
    },
    "Refund Request": {
        "on_submit":    "tutor_booking_platform.events.refund_request.on_submit",
        "validate":     "tutor_booking_platform.events.refund_request.validate",
    },
}

# ─── Notification Config ──────────────────────────────────────────────────────
notification_config = "tutor_booking_platform.notifications.get_notification_config"

# ─── Permission Query Conditions ──────────────────────────────────────────────
permission_query_conditions = {
    "Tutor Booking": "tutor_booking_platform.permissions.tutor_booking.get_permission_query_conditions",
    "Tutor Session": "tutor_booking_platform.permissions.tutor_session.get_permission_query_conditions",
    "Payment Transaction": "tutor_booking_platform.permissions.payment_transaction.get_permission_query_conditions",
}

# ─── Assets (Desk-side includes) ─────────────────────────────────────────────
app_include_css = "/assets/tutor_booking_platform/css/tutor_booking_platform.css"

# ─── Jinja Globals ────────────────────────────────────────────────────────────
jinja = {
    "methods": [
        "tutor_booking_platform.utils.jinja_helpers.get_tutor_rating",
        "tutor_booking_platform.utils.jinja_helpers.get_session_count",
    ]
}