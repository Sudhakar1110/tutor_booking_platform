# -*- coding: utf-8 -*-
"""
Tutor Booking Platform — Payment Transaction Fix Script
Runs diagnostics and fixes common issues causing "Payment Transaction not found"
in the Frappe Desk.

Usage:
    bench --site testing.site1.local console
    >>> exec(open("../apps/tutor_booking_platform/tutor_booking_platform/fix_payment_issue.py").read(), globals())
    >>> fix_payment_issue()
"""

import frappe
import traceback
import sys


def fix_payment_issue():
    print("=" * 60)
    print("  PAYMENT TRANSACTION — DIAGNOSTIC & FIX")
    print("=" * 60)

    issues_found = []
    fixes_applied = []

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Check if Payment Transaction table exists
    # ──────────────────────────────────────────────────────────────────────────
    print("\n📋 Step 1: Checking Payment Transaction table...")
    try:
        count = frappe.db.count("Payment Transaction")
        print(f"  ✅ Payment Transaction table exists. Records: {count}")
        if count > 0:
            samples = frappe.get_all("Payment Transaction", fields=["name", "payment_status", "amount", "payment_method"], limit=3)
            for s in samples:
                print(f"     - {s.name}: {s.payment_status}, ₹{s.amount}, {s.payment_method}")
        else:
            print(f"  ⚠️  No Payment Transaction records found!")
            issues_found.append("No records in Payment Transaction table")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        issues_found.append(f"Table check failed: {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Check import paths
    # ──────────────────────────────────────────────────────────────────────────
    print("\n📋 Step 2: Testing import paths...")
    imports_to_test = [
        "tutor_booking_platform.events.payment_transaction",
        "tutor_booking_platform.permissions.payment_transaction",
        "tutor_booking_platform.api.booking",
        "tutor_booking_platform.install",
    ]
    for imp_path in imports_to_test:
        try:
            __import__(imp_path)
            print(f"  ✅ {imp_path} — OK")
        except Exception as e:
            print(f"  ❌ {imp_path} — FAILED: {e}")
            issues_found.append(f"Import failed: {imp_path}: {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Check Permission Query Conditions
    # ──────────────────────────────────────────────────────────────────────────
    print("\n📋 Step 3: Checking Permission Query Conditions...")
    try:
        user = frappe.session.user
        print(f"  Current user: {user}")
        roles = frappe.get_roles(user)
        print(f"  Roles: {', '.join(roles[:10])}" + (f" + {len(roles)-10} more" if len(roles) > 10 else ""))

        # Test the permission function
        from tutor_booking_platform.permissions.payment_transaction import get_permission_query_conditions
        condition = get_permission_query_conditions(user)
        if condition == "":
            print(f"  ✅ Permission condition: NO FILTER (all records visible)")
        elif condition == "1=0":
            print(f"  ❌ Permission condition: 1=0 (NO RECORDS visible!)")
            print(f"     This means the user doesn't have proper roles assigned!")
            print(f"     Administrator should have 'System Manager' role.")
            if "System Manager" not in roles:
                print(f"     ⚠️  'System Manager' role NOT found in user roles!")
                issues_found.append("System Manager role missing — need to assign it")
            if "Tutor Booking Manager" not in roles:
                print(f"     ⚠️  'Tutor Booking Manager' role NOT found")
        else:
            print(f"  ℹ️  Permission condition: {condition[:80]}...")
    except Exception as e:
        print(f"  ❌ Error checking permissions: {e}")
        traceback.print_exc()
        issues_found.append(f"Permission check failed: {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Check DocType metadata
    # ──────────────────────────────────────────────────────────────────────────
    print("\n📋 Step 4: Checking DocType metadata...")
    try:
        meta = frappe.get_meta("Payment Transaction")
        print(f"  ✅ DocType metadata loaded: {meta.name}")
        # Check if module is correct
        from frappe.model.meta import get_meta
        dt_meta = frappe.get_doc("DocType", "Payment Transaction")
        print(f"  Module: {dt_meta.module}")
        if dt_meta.module != "Tutor Booking Platform":
            print(f"  ⚠️  Module is '{dt_meta.module}' instead of 'Tutor Booking Platform'")
            issues_found.append(f"Wrong module: {dt_meta.module}")
    except Exception as e:
        print(f"  ❌ Error loading DocType metadata: {e}")
        issues_found.append(f"DocType metadata load failed: {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # 5. Check the server script can be instantiated
    # ──────────────────────────────────────────────────────────────────────────
    print("\n📋 Step 5: Checking server script...")
    try:
        # Try creating a dummy document object to test methods
        doc = frappe.new_doc("Payment Transaction")
        print(f"  ✅ Can create new Payment Transaction document")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        issues_found.append(f"Cannot create new doc: {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # 6. Try opening each Payment Transaction
    # ──────────────────────────────────────────────────────────────────────────
    print("\n📋 Step 6: Testing individual Payment Transaction records...")
    try:
        names = frappe.get_all("Payment Transaction", pluck="name")
        if names:
            errors = 0
            for name in names[:5]:  # Test up to 5
                try:
                    doc = frappe.get_doc("Payment Transaction", name)
                    print(f"  ✅ {name} — OK (status={doc.payment_status}, amt=₹{doc.amount})")
                except Exception as e:
                    print(f"  ❌ {name} — FAILED: {e}")
                    errors += 1
            if errors == 0:
                print(f"  ✅ All {min(len(names), 5)} tested Payment Transactions open correctly")
            else:
                issues_found.append(f"{errors} Payment Transactions failed to open")
        else:
            print(f"  ⚠️  No Payment Transactions to test")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # Summary & Fixes
    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    if issues_found:
        print(f"  ❌ ISSUES FOUND ({len(issues_found)}):")
        for i, issue in enumerate(issues_found, 1):
            print(f"     {i}. {issue}")

        print("\n  🔧 RECOMMENDED FIXES:")

        # Fix 1: Clear cache
        print("\n  1. Clear Frappe cache:")
        print("     bench --site testing.site1.local clear-cache")
        print("     bench --site testing.site1.local clear-website-cache")

        # Fix 2: Assign roles if needed
        if any("role" in issue.lower() for issue in issues_found):
            print("\n  2. Assign System Manager role to current user:")
            print("     bench --site testing.site1.local console")
            print("     >>> user = frappe.get_doc('User', frappe.session.user)")
            print("     >>> user.add_roles('System Manager')")
            print("     >>> user.save(ignore_permissions=True)")
            print("     >>> frappe.db.commit()")

        # Fix 3: Re-import hooks
        if any("import" in issue.lower() for issue in issues_found):
            print("\n  3. Rebuild Python modules:")
            print("     bench build")
            print("     bench --site testing.site1.local migrate")

        # Fix 4: Restart
        print("\n  4. Restart the server:")
        print("     bench restart")

    else:
        print("  ✅ NO ISSUES FOUND!")
        print("  Payment Transaction should work correctly in Frappe Desk.")
        print("\n  If still seeing 'not found', try clearing browser cache and hard refresh.")
        print("  Or run: bench clear-cache && bench clear-website-cache && bench restart")

    print("=" * 60)
    return issues_found


if __name__ == "__main__":
    fix_payment_issue()
