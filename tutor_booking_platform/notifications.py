# -*- coding: utf-8 -*-
"""
tutor_booking_platform/notifications.py
Notification configuration for Frappe desk notifications.
"""
import frappe


def get_notification_config():
    """Return notification config for desk bell icon counts."""
    return {
        "for_doctype": {
            "Tutor Booking": {
                "status": "Pending"
            },
            "Demo Class Request": {
                "status": "Pending"
            },
            "Refund Request": {
                "status": "Pending"
            },
            "Tutor Verification": {
                "verification_status": "Pending"
            },
            "Tutor Session": {
                "status": "Scheduled"
            },
        },
    }