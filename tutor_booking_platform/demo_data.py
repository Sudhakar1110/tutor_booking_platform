# -*- coding: utf-8 -*-
"""
Tutor Booking Platform — Demo Data Generator
Run this script to populate realistic demo data for all 40+ DocTypes.

Usage On Server:
    bench --site testing.site1.local console
    >>> exec(open("../apps/tutor_booking_platform/tutor_booking_platform/demo_data.py").read())
    >>> generate_demo_data()
"""

import frappe
from datetime import datetime, date, timedelta
import random

# ─── Helpers ──────────────────────────────────────────────────────────────────

def create_doc(doctype, data):
    """Create a document safely, return its name or None on failure."""
    try:
        doc = frappe.get_doc({"doctype": doctype, **data})
        doc.insert(ignore_permissions=True)
        return doc.name
    except frappe.DuplicateEntryError as e:
        # Try to find by name or a unique field
        name_val = data.get("subject_name") or data.get("course_name") or data.get("skill_name") or \
                   data.get("category_name") or data.get("settings_name") or data.get("tutor_name") or \
                   data.get("student_name") or data.get("booking_title") or data.get("class_title") or \
                   data.get("certification_name") or data.get("degree") or data.get("organization_name") or \
                   data.get("thread_title")
        if name_val:
            existing = frappe.db.get_value(doctype, {"name": name_val}) or \
                       frappe.db.get_value(doctype, {"subject_name": name_val}) or \
                       frappe.db.get_value(doctype, {"course_name": name_val}) or \
                       frappe.db.get_value(doctype, {"skill_name": name_val}) or \
                       frappe.db.get_value(doctype, {"category_name": name_val})
            if existing:
                return existing
        print(f"  ⚠️ Duplicate skipped: {doctype}: {str(e)[:80]}")
        return None
    except Exception as e:
        print(f"  ❌ Error creating {doctype}: {str(e)[:120]}")
        frappe.log_error(f"DemoData: {doctype}: {str(e)}", "Demo Data Generator")
        return None

def random_phone():
    return f"+91{random.choice([9,8,7,6])}{random.randint(100000000, 999999999)}"

def random_date(start_year=2024, end_year=2026):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def random_time(start_hour=7, end_hour=21):
    h = random.randint(start_hour, end_hour - 1)
    m = random.choice(["00", "15", "30", "45"])
    return f"{h:02d}:{m}:00"

def choice(lst):
    return random.choice(lst)

# ─── Static Data ──────────────────────────────────────────────────────────────

CITIES = [
    ("Mumbai", "Maharashtra"), ("Delhi", "Delhi"), ("Bangalore", "Karnataka"),
    ("Hyderabad", "Telangana"), ("Chennai", "Tamil Nadu"), ("Kolkata", "West Bengal"),
    ("Pune", "Maharashtra"), ("Ahmedabad", "Gujarat"), ("Jaipur", "Rajasthan"),
    ("Lucknow", "Uttar Pradesh"),
]

STUDENT_DATA = [
    ("Aarav", "Sharma", "Class 10"), ("Vivaan", "Verma", "Class 9"),
    ("Aditya", "Patel", "Class 12"), ("Vihaan", "Singh", "Class 11"),
    ("Arjun", "Kumar", "Undergraduate"), ("Sai", "Reddy", "Undergraduate"),
    ("Dhruv", "Joshi", "Class 10"), ("Reyansh", "Gupta", "Class 12"),
    ("Ayaan", "Desai", "Postgraduate"), ("Ishaan", "Nair", "Undergraduate"),
    ("Ananya", "Kapoor", "Class 9"), ("Diya", "Malhotra", "Class 11"),
    ("Isha", "Chopra", "Class 10"), ("Myra", "Agarwal", "Class 8"),
    ("Aanya", "Saxena", "Undergraduate"), ("Sara", "Bhatt", "Postgraduate"),
    ("Siya", "Trivedi", "Class 12"), ("Riya", "Mishra", "Working Professional"),
    ("Neha", "Rao", "Working Professional"), ("Priya", "Choudhury", "Undergraduate"),
    ("Sneha", "Banerjee", "Class 10"), ("Pooja", "Das", "Class 9"),
    ("Kavya", "Pillai", "Class 11"), ("Shruti", "Thakur", "Postgraduate"),
    ("Tanvi", "Seth", "Working Professional"), ("Nandini", "Ghosh", "Undergraduate"),
    ("Divya", "Kulkarni", "Class 12"), ("Meera", "Dutta", "Class 11"),
    ("Rohan", "Iyer", "Undergraduate"), ("Krishna", "Menon", "Postgraduate"),
]

TUTOR_SPECS = [
    ("Dr. Rajesh Kumar", "Mathematics", "IIT Bombay, B.Tech + M.Tech", 12, 800),
    ("Prof. Sunil Verma", "Physics", "IIT Delhi, B.Tech + PhD Physics", 10, 900),
    ("Dr. Anita Deshmukh", "Chemistry", "BHU, MSc Chemistry + B.Ed", 8, 700),
    ("Dr. Arvind Singh", "Biology", "AIIMS, MBBS", 6, 1000),
    ("Ms. Pooja Sharma", "English", "Delhi University, MA English", 15, 600),
    ("Mr. Amit Patel", "IELTS", "British Council Certified IELTS Trainer", 9, 1200),
    ("Prof. Deepa Nair", "Spoken English", "Cambridge CELTA Certified", 11, 750),
    ("Mr. Manoj Reddy", "Java", "NIIT Certified Java Programmer", 8, 850),
    ("Dr. Vikram Joshi", "Python", "IIT Madras, B.Tech CS", 7, 900),
    ("Ms. Shweta Menon", "Data Science", "IIM Bangalore, Data Science Program", 5, 1500),
    ("Prof. Ravi Gupta", "Artificial Intelligence", "Stanford Online, AI Certificate", 6, 1800),
    ("Mr. Harsh Mehta", "Full Stack", "UpGrad, Full Stack Development", 8, 1100),
    ("Dr. Kavita Rao", "Aptitude", "IMS, CAT Topper 99.9%ile", 14, 500),
    ("Ms. Lata Krishnan", "Reasoning", "LSAT India, Top 1% scorer", 10, 550),
    ("Dr. Suresh Iyer", "Communication", "XLRI, HRM + Soft Skills", 13, 700),
]

SUBJECT_NAMES = [
    "Mathematics", "Physics", "Chemistry", "Biology", "English",
    "IELTS", "Spoken English", "Aptitude", "Reasoning",
    "Java", "Python", "SQL", "Data Science", "Artificial Intelligence", "Machine Learning"
]

COURSE_DEFS = [
    ("Python Programming", "Programming Courses", "Python", 8, 12000, "Beginner"),
    ("Java Full Stack", "Programming Courses", "Java", 16, 25000, "Intermediate"),
    ("Data Science", "Professional Courses", "Data Science", 12, 35000, "Intermediate"),
    ("AI & ML", "Professional Courses", "Artificial Intelligence", 16, 45000, "Advanced"),
    ("Spoken English", "Language Courses", "Spoken English", 8, 8000, "Beginner"),
    ("IELTS Preparation", "Language Courses", "IELTS", 6, 12000, "Intermediate"),
    ("Mathematics Foundation", "Academic Courses", "Mathematics", 12, 10000, "Beginner"),
    ("Competitive Exam Training", "Academic Courses", "Aptitude", 16, 15000, "Advanced"),
]

SKILL_DEFS = [
    ("Python", "Technical Skills"), ("Java", "Technical Skills"), ("SQL", "Technical Skills"),
    ("Communication", "Professional Skills"), ("Mathematics", "Academic Skills"),
    ("Teaching", "Professional Skills"), ("Problem Solving", "Academic Skills"),
    ("Data Analysis", "Technical Skills"),
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ─── Main Generator ───────────────────────────────────────────────────────────

def generate_demo_data():
    print("=" * 60)
    print("  TUTOR BOOKING PLATFORM — DEMO DATA GENERATOR")
    print("=" * 60)

    stats = {}
    subject_map = {}    # subject_name → document name
    course_map = {}     # course_name → document name
    skill_map = {}      # skill_name → document name

    # ------------------------------------------------------------------
    # 1. CATEGORIES
    # ------------------------------------------------------------------
    print("\n─── Creating Subject Categories ───")
    cat_map = {}
    for i, name in enumerate(["School Subjects", "College Subjects", "Competitive Exams",
                               "Programming", "Languages", "Professional Skills"]):
        n = create_doc("Subject Category", {
            "category_name": name, "is_active": 1,
            "description": f"Category for {name.lower()}",
            "display_order": i + 1
        })
        if n: cat_map[name] = n
    stats["Subject Category"] = len(cat_map)

    print("\n─── Creating Course Categories ───")
    course_cat_map = {}
    for name in ["Academic Courses", "Programming Courses", "Language Courses", "Professional Courses"]:
        n = create_doc("Course Category", {
            "category_name": name, "is_active": 1,
            "description": f"Category for {name.lower()}"
        })
        if n: course_cat_map[name] = n
    stats["Course Category"] = len(course_cat_map)

    print("\n─── Creating Skill Categories ───")
    skill_cat_map = {}
    for name in ["Technical Skills", "Academic Skills", "Language Skills", "Professional Skills"]:
        n = create_doc("Skill Category", {
            "category_name": name, "is_active": 1,
            "description": f"Category for {name.lower()}"
        })
        if n: skill_cat_map[name] = n
    stats["Skill Category"] = len(skill_cat_map)
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 2. SUBJECTS (capture document names)
    # ------------------------------------------------------------------
    print("\n─── Creating Subjects ───")
    for sname in SUBJECT_NAMES:
        n = create_doc("Subject", {
            "subject_name": sname,
            "subject_category": choice(list(cat_map.values())),
            "subject_code": f"SUB-{random.randint(100, 999)}",
            "is_active": 1,
            "description": f"Comprehensive {sname.lower()} tutoring for all levels.",
            "target_audience": "All",
            "difficulty_level": "All Levels",
        })
        if n:
            subject_map[sname] = n
    stats["Subject"] = len(subject_map)

    # 3. COURSES (capture document names)
    print("\n─── Creating Courses ───")
    for cname, ccat, subj, dur, fee, lvl in COURSE_DEFS:
        subj_name = next((s for s in SUBJECT_NAMES if s.lower() == subj.lower()), None)
        n = create_doc("Course", {
            "course_name": cname,
            "course_category": course_cat_map.get(ccat),
            "subject": subject_map.get(subj_name),
            "is_active": 1,
            "duration_weeks": dur,
            "level": lvl,
            "fee": fee,
            "mode": choice(["Online", "Offline", "Hybrid"]),
            "description": f"Complete {cname.lower()} course. Duration: {dur} weeks. Fee: ₹{fee:,}.",
        })
        if n:
            course_map[cname] = n
    stats["Course"] = len(course_map)

    # 4. SKILLS (capture document names)
    print("\n─── Creating Skills ───")
    for sk_name, sk_cat_name in SKILL_DEFS:
        n = create_doc("Skill", {
            "skill_name": sk_name,
            "skill_category": skill_cat_map.get(sk_cat_name),
            "is_active": 1,
            "description": f"Skill in {sk_name.lower()}",
        })
        if n:
            skill_map[sk_name] = n
    stats["Skill"] = len(skill_map)
    frappe.db.commit()
    print("  ✅ Base data committed")

    # ------------------------------------------------------------------
    # 5. TUTOR PROFILES + child records
    # ------------------------------------------------------------------
    print("\n─── Creating Tutor Profiles (15) ───")
    tutor_names = []
    for i, (tname, primary_subj, edu, exp_yrs, rate) in enumerate(TUTOR_SPECS):
        first_name = tname.split()[1] if len(tname.split()) > 1 else tname.split()[0]
        last_name = tname.split()[-1]
        city, state = choice(CITIES)
        levels = choice(["High School, Undergraduate", "All Levels", "Undergraduate, Postgraduate", "High School, Undergraduate, Postgraduate"])
        tp = create_doc("Tutor Profile", {
            "tutor_name": tname,
            "gender": choice(["Male", "Female"]),
            "date_of_birth": date(random.randint(1975, 1995), random.randint(1, 12), random.randint(1, 28)),
            "email": f"{first_name.lower()}.{last_name.lower()}@tutorexample.com",
            "mobile": random_phone(),
            "city": city,
            "state": state,
            "country": "India",
            "teaching_mode": choice(["Online", "Offline", "Both"]),
            "experience_years": exp_yrs,
            "hourly_rate": rate,
            "minimum_hours": choice([1, 1.5, 2]),
            "primary_subject": subject_map.get(primary_subj),
            "subjects_taught": f"<p>{primary_subj} and related subjects.</p>",
            "teaching_levels": levels,
            "languages_known": choice(["English, Hindi", "English, Hindi, Marathi", "English, Hindi, Tamil"]),
            "verification_status": "Verified",
            "average_rating": round(random.uniform(4.0, 5.0), 2),
            "total_sessions": random.randint(50, 500),
            "total_students": random.randint(20, 200),
            "short_bio": f"Experienced {primary_subj.lower()} tutor with {exp_yrs} years. {edu}.",
            "detailed_bio": f"<p>Passionate {primary_subj.lower()} educator with {exp_yrs}+ years of teaching. {edu}.</p>",
        })
        if tp:
            tutor_names.append(tp)
    stats["Tutor Profile"] = len(tutor_names)
    frappe.db.commit()

    # Tutor child records
    print("\n─── Tutor Qualifications, Experience, Certifications ───")
    qual_n, exp_n, cert_n, avail_n, verif_n = 0, 0, 0, 0, 0
    for tp_name in tutor_names:
        primary_subj = frappe.db.get_value("Tutor Profile", tp_name, "primary_subject")
        # 1 Qualification
        if create_doc("Tutor Qualification", {
            "tutor_profile": tp_name, "degree": "Master's Degree",
            "field_of_study": primary_subj or "Education",
            "institution": choice(["IIT Bombay", "IIT Delhi", "Delhi University", "BHU"]),
            "passing_year": random.randint(1995, 2015),
            "grade_percentage": random.randint(70, 95),
            "is_verified": 1,
        }): qual_n += 1
        # 1-2 Experience
        for _ in range(random.randint(1, 2)):
            org = choice(["Kota Coaching", "Delhi Public School", "FIITJEE", "Self Employed"])
            fy = date(2005 + random.randint(0, 10), 1, 1)
            ty = date(fy.year + random.randint(2, 5), 1, 1)
            if ty > date(2026, 1, 1): ty = date(2025, 12, 31)
            if create_doc("Tutor Experience", {
                "tutor_profile": tp_name, "organization_name": org,
                "role_title": choice(["Senior Tutor", "Faculty", "Subject Expert"]),
                "employment_type": choice(["Full Time", "Part Time"]),
                "from_date": fy, "to_date": ty,
                "is_current": 0,
                "description": f"Taught {primary_subj or 'subjects'} to students.",
            }): exp_n += 1
        # 1 Certification
        if create_doc("Tutor Certification", {
            "tutor_profile": tp_name,
            "certification_name": choice(["B.Ed", "NTA NET", "GATE", "Certified Educator"]),
            "issuing_authority": choice(["UGC", "NTA", "Cambridge", "Microsoft"]),
            "issue_date": date(random.randint(2015, 2024), random.randint(1, 12), random.randint(1, 28)),
            "is_lifetime_valid": 1,
            "is_verified": 1,
        }): cert_n += 1
        # Availability (3-5 days)
        for day in random.sample(DAYS, random.randint(3, 5)):
            sh = random.randint(8, 14)
            if create_doc("Tutor Availability", {
                "tutor_profile": tp_name, "day_of_week": day,
                "start_time": f"{sh:02d}:00:00", "end_time": f"{sh + 3:02d}:00:00",
                "is_available": 1, "teaching_mode": choice(["Online", "Both"]),
                "max_students_per_slot": random.randint(1, 5),
            }): avail_n += 1
        # Verification
        if create_doc("Tutor Verification", {
            "tutor_profile": tp_name, "verification_status": "Verified",
            "verification_type": "Full Verification", "verified_by": "Administrator",
            "id_proof_type": choice(["Aadhaar", "PAN Card", "Passport"]),
            "id_proof_number": f"{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
            "verification_date": date(2025, random.randint(1, 12), random.randint(1, 28)),
            "remarks": "All documents verified.",
        }): verif_n += 1
    stats["Tutor Qualification"] = qual_n
    stats["Tutor Experience"] = exp_n
    stats["Tutor Certification"] = cert_n
    stats["Tutor Availability"] = avail_n
    stats["Tutor Verification"] = verif_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 6. STUDENT PROFILES + child records
    # ------------------------------------------------------------------
    print("\n─── Creating Student Profiles (30) ───")
    student_names = []
    for first, last, cls in STUDENT_DATA:
        city, state = choice(CITIES)
        is_working = cls == "Working Professional"
        sp = create_doc("Student Profile", {
            "student_name": f"{first} {last}",
            "gender": choice(["Male", "Female"]),
            "date_of_birth": date(random.randint(2000, 2015), random.randint(1, 12), random.randint(1, 28)),
            "email": f"{first.lower()}.{last.lower()}@studentmail.com",
            "mobile": random_phone(),
            "parent_name": f"{choice(['Mr.', 'Mrs.'])} {last}" if not is_working else "",
            "parent_mobile": random_phone() if not is_working else "",
            "current_class": cls,
            "school_college": choice(["DPS", "St. Mary's", "Mumbai University", "VIT"]) if not is_working else "",
            "board": choice(["CBSE", "ICSE"]) if not is_working else "",
            "preferred_learning_mode": choice(["Online", "Offline", "Both"]),
            "preferred_timing": choice(["Morning", "Evening", "Flexible"]),
            "budget_per_hour": choice([300, 500, 700, 1000]),
        })
        if sp: student_names.append(sp)
    stats["Student Profile"] = len(student_names)
    frappe.db.commit()

    print("\n─── Student Addresses, Requirements, Preferences ───")
    addr_n, req_n, pref_n = 0, 0, 0
    for sp_name in student_names:
        city = frappe.db.get_value("Student Profile", sp_name, "city") or "Mumbai"
        # Address
        if create_doc("Student Address", {
            "student_profile": sp_name, "address_type": "Home", "is_default": 1,
            "address_line1": f"{random.randint(1,999)}, {choice(['MG Road', 'Park St', 'Lake View'])}",
            "city": city, "state": "Maharashtra", "pincode": f"{random.randint(100000,999999)}",
        }): addr_n += 1
        # 1 Requirement
        subj = choice(list(subject_map.values())) if subject_map else None
        if create_doc("Student Requirement", {
            "student_profile": sp_name, "subject": subj,
            "requirement_title": f"Need help with tutoring",
            "status": choice(["Open", "Matched"]),
            "preferred_mode": choice(["Online", "Offline", "Both"]),
            "preferred_gender": "Any",
            "budget_per_hour": choice([300, 500, 800]),
            "urgency": choice(["Medium", "High"]),
            "requirement_date": random_date(2025, 2026),
        }): req_n += 1
        # Preference
        if create_doc("Student Preference", {
            "student_profile": sp_name, "subject": subj,
            "preferred_tutor_gender": "Any",
            "preferred_language": "English, Hindi",
            "learning_goal": choice(["Exam Preparation", "Skill Development", "Career Advancement"]),
            "weekly_hours": choice([2, 3, 4, 6]),
        }): pref_n += 1
    stats["Student Address"] = addr_n
    stats["Student Requirement"] = req_n
    stats["Student Preference"] = pref_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 7. SEARCH REQUESTS & MATCH RESULTS
    # ------------------------------------------------------------------
    print("\n─── Search Requests & Match Results ───")
    sr_n, mr_n = 0, 0
    for _ in range(20):
        sp = choice(student_names) if student_names else None
        subj = choice(list(subject_map.values())) if subject_map else None
        sr = create_doc("Tutor Search Request", {
            "student_profile": sp, "subject": subj,
            "teaching_mode": choice(["Online", "Both"]),
            "status": choice(["Matched", "Closed"]),
            "max_budget": choice([500, 800, 1000, 1500]),
            "search_date": random_date(2025, 2026),
        })
        if sr:
            sr_n += 1
            for tp in random.sample(tutor_names, min(random.randint(1, 3), len(tutor_names))):
                if create_doc("Tutor Match Result", {
                    "search_request": sr, "tutor_profile": tp,
                    "match_score": round(random.uniform(75, 99), 2),
                    "status": choice(["Suggested", "Shortlisted", "Booked"]),
                    "match_date": random_date(2025, 2026),
                }): mr_n += 1
    stats["Tutor Search Request"] = sr_n
    stats["Tutor Match Result"] = mr_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 8. DEMO CLASS REQUESTS & SCHEDULES
    # ------------------------------------------------------------------
    print("\n─── Demo Class Requests & Schedules ───")
    dr_n, ds_n = 0, 0
    for _ in range(15):
        sp = choice(student_names) if student_names else None
        tp = choice(tutor_names) if tutor_names else None
        subj = frappe.db.get_value("Tutor Profile", tp, "primary_subject") if tp else None
        dr = create_doc("Demo Class Request", {
            "student_profile": sp, "tutor_profile": tp, "subject": subj,
            "status": "Approved", "preferred_date": random_date(2025, 2026),
            "preferred_time": random_time(9, 18), "mode": choice(["Online", "Offline"]),
            "message": "I'd like a demo session. Please let me know available timings.",
        })
        if dr:
            dr_n += 1
            if random.random() > 0.3:
                if create_doc("Demo Class Schedule", {
                    "demo_class_request": dr, "tutor_profile": tp,
                    "student_profile": sp, "status": "Scheduled",
                    "scheduled_date": random_date(2025, 2026),
                    "start_time": random_time(9, 18), "end_time": random_time(10, 19),
                    "duration_minutes": 60, "mode": choice(["Online", "Offline"]),
                }): ds_n += 1
    stats["Demo Class Request"] = dr_n
    stats["Demo Class Schedule"] = ds_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 9. TUTOR BOOKINGS
    # ------------------------------------------------------------------
    print("\n─── Tutor Bookings (30) ───")
    booking_names = []
    for _ in range(30):
        sp = choice(student_names) if student_names else None
        tp = choice(tutor_names) if tutor_names else None
        subj = frappe.db.get_value("Tutor Profile", tp, "primary_subject") if tp else None
        rate = frappe.db.get_value("Tutor Profile", tp, "hourly_rate") or 500
        sw = random.randint(1, 3)
        hp = choice([1, 1.5, 2])
        total_h = sw * hp * random.randint(4, 12)
        total = int(rate * total_h)
        start = random_date(2025, 2026)
        end = start + timedelta(days=random.randint(30, 120))
        bk = create_doc("Tutor Booking", {
            "booking_title": f"Regular {subj or 'tutoring'} Sessions",
            "booking_status": choice(["Confirmed", "Active", "Completed"]),
            "student_profile": sp, "tutor_profile": tp, "subject": subj,
            "teaching_mode": choice(["Online", "Offline"]),
            "booking_date": random_date(2025, 2026),
            "start_date": start, "end_date": end,
            "sessions_per_week": sw, "hours_per_session": hp,
            "rate_per_hour": rate, "total_hours": total_h, "total_amount": total,
            "payment_status": choice(["Unpaid", "Partially Paid", "Paid"]),
        })
        if bk: booking_names.append(bk)
    stats["Tutor Booking"] = len(booking_names)
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 10. TUTOR SESSIONS
    # ------------------------------------------------------------------
    print("\n─── Tutor Sessions (50) ───")
    session_names = []
    for _ in range(50):
        bk = choice(booking_names) if booking_names else None
        if not bk: continue
        bk_doc = frappe.get_doc("Tutor Booking", bk)
        sd = random_date(2025, 2026)
        sh = random.randint(9, 17)
        sess = create_doc("Tutor Session", {
            "tutor_booking": bk, "tutor_profile": bk_doc.tutor_profile,
            "student_profile": bk_doc.student_profile,
            "status": choice(["Completed", "Completed", "Scheduled"]),
            "session_date": sd,
            "start_time": f"{sh:02d}:00:00", "end_time": f"{sh + 1:02d}:00:00",
            "duration_minutes": 60, "subject": bk_doc.subject,
            "mode": bk_doc.teaching_mode, "session_number": random.randint(1, 15),
            "homework_assigned": 1 if random.random() > 0.5 else 0,
            "notes": "Session went well.", "tutor_remarks": "Good progress.",
        })
        if sess: session_names.append(sess)
    stats["Tutor Session"] = len(session_names)
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 11. ONLINE / OFFLINE CLASSES
    # ------------------------------------------------------------------
    print("\n─── Online & Offline Classes ───")
    on_n, off_n = 0, 0
    for _ in range(20):
        tp = choice(tutor_names) if tutor_names else None
        subj = frappe.db.get_value("Tutor Profile", tp, "primary_subject") if tp else None
        if create_doc("Online Class", {
            "class_title": f"{subj or 'General'} Online Session",
            "tutor_profile": tp, "subject": subj,
            "status": choice(["Scheduled", "Completed"]),
            "class_date": random_date(2025, 2026),
            "start_time": random_time(9, 17), "end_time": random_time(10, 18),
            "max_students": random.randint(10, 40),
            "platform": choice(["Zoom", "Google Meet", "Microsoft Teams"]),
            "meeting_link": f"https://zoom.us/j/{random.randint(100000000,999999999)}",
        }): on_n += 1
    for _ in range(10):
        tp = choice(tutor_names) if tutor_names else None
        subj = frappe.db.get_value("Tutor Profile", tp, "primary_subject") if tp else None
        if create_doc("Offline Class", {
            "class_title": f"{subj or 'General'} Offline Session",
            "tutor_profile": tp, "subject": subj,
            "status": choice(["Scheduled", "Completed"]),
            "class_date": random_date(2025, 2026),
            "start_time": random_time(9, 17), "end_time": random_time(10, 18),
            "location": choice(["Classroom A", "Lab 1", "Conference Room"]),
            "city": choice(CITIES)[0], "max_students": random.randint(20, 50),
        }): off_n += 1
    stats["Online Class"] = on_n
    stats["Offline Class"] = off_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 12. LEARNING SCHEDULES
    # ------------------------------------------------------------------
    print("\n─── Learning Schedules (30) ───")
    ls_n = 0
    for _ in range(30):
        bk = choice(booking_names) if booking_names else None
        if not bk: continue
        bk_doc = frappe.get_doc("Tutor Booking", bk)
        if create_doc("Learning Schedule", {
            "tutor_booking": bk, "student_profile": bk_doc.student_profile,
            "tutor_profile": bk_doc.tutor_profile, "subject": bk_doc.subject,
            "day_of_week": choice(DAYS),
            "start_time": random_time(9, 17), "end_time": random_time(10, 18),
            "is_active": 1, "valid_from": random_date(2025, 2026),
            "valid_to": random_date(2026, 2026),
        }): ls_n += 1
    stats["Learning Schedule"] = ls_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 13. ATTENDANCE RECORDS
    # ------------------------------------------------------------------
    print("\n─── Attendance Records (up to 100) ───")
    att_n = 0
    for sess in session_names:
        sd = frappe.get_doc("Tutor Session", sess)
        if sd.status == "Completed":
            if create_doc("Attendance Record", {
                "tutor_session": sess, "student_profile": sd.student_profile,
                "tutor_profile": sd.tutor_profile, "subject": sd.subject,
                "attendance_date": sd.session_date,
                "status": choice(["Present", "Present", "Late"]),
                "check_in_time": sd.start_time, "check_out_time": sd.end_time,
            }): att_n += 1
    stats["Attendance Record"] = att_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 14. LEARNING PROGRESS
    # ------------------------------------------------------------------
    print("\n─── Learning Progress (30) ───")
    lp_n = 0
    for _ in range(30):
        bk = choice(booking_names) if booking_names else None
        if not bk: continue
        bk_doc = frappe.get_doc("Tutor Booking", bk)
        total = random.randint(10, 30)
        attended = random.randint(total - 5, total)
        if create_doc("Learning Progress", {
            "student_profile": bk_doc.student_profile,
            "tutor_profile": bk_doc.tutor_profile,
            "subject": bk_doc.subject, "tutor_booking": bk,
            "sessions_completed": total, "sessions_attended": attended,
            "total_hours": float(total * 1.0),
            "completion_percentage": random.randint(30, 100),
            "performance_rating": choice(["Excellent", "Good", "Good", "Average"]),
            "notes": "Making steady progress.", "last_updated": date.today(),
        }): lp_n += 1
    stats["Learning Progress"] = lp_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 15. PAYMENT TRANSACTIONS
    # ------------------------------------------------------------------
    print("\n─── Payment Transactions (30) ───")
    payment_names = []
    for bk in booking_names[:30]:
        bk_doc = frappe.get_doc("Tutor Booking", bk)
        amt = bk_doc.total_amount or choice([500, 1000, 2500, 5000])
        pmt = create_doc("Payment Transaction", {
            "tutor_booking": bk, "student_profile": bk_doc.student_profile,
            "tutor_profile": bk_doc.tutor_profile,
            "payment_status": choice(["Completed", "Completed", "Pending"]),
            "amount": amt, "platform_commission": int(amt * 0.1),
            "tutor_payout": int(amt * 0.9), "currency": "INR",
            "payment_method": choice(["UPI", "Card", "Cash"]),
            "payment_date": random_date(2025, 2026),
            "transaction_id": f"TXN{random.randint(10000000, 99999999)}",
        })
        if pmt: payment_names.append(pmt)
    stats["Payment Transaction"] = len(payment_names)
    frappe.db.commit()

    # Card Payments
    print("\n─── Card & Cash Payments ───")
    card_n, cash_n = 0, 0
    for pmt in payment_names[:15]:
        pmt_doc = frappe.get_doc("Payment Transaction", pmt)
        if create_doc("Card Payment", {
            "payment_transaction": pmt, "tutor_booking": pmt_doc.tutor_booking,
            "amount": pmt_doc.amount, "payment_status": "Success",
            "card_type": choice(["Visa", "Mastercard", "RuPay"]),
            "card_last_four": str(random.randint(1000, 9999)),
            "gateway": choice(["Razorpay", "PayU"]),
            "gateway_transaction_id": f"GT{random.randint(100000,999999)}",
            "payment_date": pmt_doc.payment_date,
        }): card_n += 1
    for pmt in payment_names[15:30]:
        pmt_doc = frappe.get_doc("Payment Transaction", pmt)
        if create_doc("Cash Payment", {
            "payment_transaction": pmt, "tutor_booking": pmt_doc.tutor_booking,
            "amount": pmt_doc.amount,
            "payment_status": choice(["Received", "Verified"]),
            "received_by": "Administrator",
            "receipt_number": f"RCPT-{random.randint(1000,9999)}",
            "payment_date": pmt_doc.payment_date,
        }): cash_n += 1
    stats["Card Payment"] = card_n
    stats["Cash Payment"] = cash_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 16. REFUND REQUESTS
    # ------------------------------------------------------------------
    print("\n─── Refund Requests (10) ───")
    ref_n = 0
    for _ in range(10):
        bk = choice(booking_names) if booking_names else None
        if not bk: continue
        bk_doc = frappe.get_doc("Tutor Booking", bk)
        if create_doc("Refund Request", {
            "tutor_booking": bk, "student_profile": bk_doc.student_profile,
            "refund_status": choice(["Pending", "Approved"]),
            "original_amount": bk_doc.total_amount or 1000,
            "refund_amount": int((bk_doc.total_amount or 1000) * 0.8),
            "refund_method": choice(["Original Payment Method", "Bank Transfer"]),
            "reason": choice(["Tutor No Show", "Schedule Change", "Other"]),
            "description": "Student requested refund.",
        }): ref_n += 1
    stats["Refund Request"] = ref_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 17. REVIEWS & RATINGS
    # ------------------------------------------------------------------
    print("\n─── Reviews, Ratings & Feedback ───")
    rev_n, rat_n, fb_n = 0, 0, 0
    for _ in range(50):
        tp = choice(tutor_names) if tutor_names else None
        sp = choice(student_names) if student_names else None
        rated = choice([4.0, 4.5, 5.0])
        # Review
        if create_doc("Tutor Review", {
            "tutor_profile": tp, "student_profile": sp,
            "review_date": random_date(2025, 2026), "rating": rated,
            "teaching_quality": rated, "punctuality": choice([4.0, 4.5, 5.0]),
            "communication": choice([4.0, 4.5, 5.0]), "is_approved": 1,
            "review_title": choice(["Excellent!", "Very Good", "Highly Recommended", "Great Tutor"]),
            "review_text": "<p>Great tutor! Very knowledgeable and patient. Highly recommended.</p>",
        }): rev_n += 1
        # Rating
        if create_doc("Tutor Rating", {
            "tutor_profile": tp, "student_profile": sp,
            "rating_date": random_date(2025, 2026), "overall_rating": rated,
            "subject_knowledge": rated, "teaching_methodology": choice([4.0, 4.5, 5.0]),
            "punctuality": choice([4.0, 4.5, 5.0]), "communication_skills": choice([4.0, 4.5, 5.0]),
            "would_recommend": 1,
        }): rat_n += 1
        # Feedback (25 only)
        if _ < 25 and create_doc("Student Feedback", {
            "student_profile": sp, "tutor_profile": tp,
            "feedback_date": random_date(2025, 2026), "session_helpful": 1,
            "topics_covered": "Course material", "difficulty_level": "Just Right",
            "overall_experience": choice(["Excellent", "Good", "Good"]),
            "feedback_text": "<p>Great session. Very helpful.</p>",
        }): fb_n += 1
    stats["Tutor Review"] = rev_n
    stats["Tutor Rating"] = rat_n
    stats["Student Feedback"] = fb_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 18. COMMUNICATION
    # ------------------------------------------------------------------
    print("\n─── Notifications, Messages, Reminders ───")
    notif_n = 0
    for _ in range(50):
        if create_doc("Notification Log", {
            "recipient": f"student{random.randint(1,30)}@email.com",
            "notification_type": choice(["Booking Confirmed", "Session Reminder", "Payment", "General"]),
            "status": choice(["Sent", "Read"]),
            "subject": choice(["Booking confirmed!", "Reminder: Session tomorrow", "Payment received"]),
            "message": "<p>Notification message.</p>",
        }): notif_n += 1
    stats["Notification Log"] = notif_n

    thread_n, chat_n = 0, 0
    for _ in range(25):
        tp = choice(tutor_names) if tutor_names else None
        sp = choice(student_names) if student_names else None
        thread = create_doc("Message Thread", {
            "thread_title": f"Chat - {random.randint(100,999)}",
            "tutor_profile": tp, "student_profile": sp, "status": choice(["Active", "Closed"]),
        })
        if thread:
            thread_n += 1
            for _ in range(random.randint(3, 5)):
                if create_doc("Chat Message", {
                    "message_thread": thread,
                    "sender": choice(["Student", "Tutor"]),
                    "sender_type": choice(["Student", "Tutor"]),
                    "sent_at": f"{random_date(2025,2026)} {random_time(8,20)}",
                    "is_read": 1, "message_type": "Text",
                    "message_text": choice([
                        "Hi, can we schedule a class?", "Sure, what time works?",
                        "Monday at 5 PM works.", "Perfect, see you then!",
                        "Thanks for the session!", "I have a question about homework.",
                    ]),
                }): chat_n += 1
    stats["Message Thread"] = thread_n
    stats["Chat Message"] = chat_n

    remind_n = 0
    for _ in range(20):
        if create_doc("Reminder Schedule", {
            "reminder_title": choice(["Session Reminder", "Payment Alert", "Profile Reminder"]),
            "reminder_type": choice(["Session Reminder", "Payment Due", "General"]),
            "recipient_type": choice(["Tutor", "Student", "Both"]),
            "is_active": 1, "frequency": choice(["One Time", "Daily", "Weekly"]),
            "send_before_hours": choice([1, 6, 12, 24]),
            "send_time": random_time(8, 12),
            "template_message": "<p>Dear {{recipient}}, this is a reminder.</p>",
        }): remind_n += 1
    stats["Reminder Schedule"] = remind_n
    frappe.db.commit()

    # ------------------------------------------------------------------
    # 19. SETTINGS
    # ------------------------------------------------------------------
    if not frappe.db.exists("Tutor Booking Settings", "Tutor Booking Settings"):
        create_doc("Tutor Booking Settings", {
            "settings_name": "Tutor Booking Settings",
            "default_currency": "INR",
            "enable_online_booking": 1,
            "enable_demo_classes": 1,
        })

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  DEMO DATA GENERATION COMPLETE")
    print("=" * 60)
    print("\n  Records Created Per DocType:")
    print("-" * 45)
    total = 0
    for doctype, count in sorted(stats.items()):
        print(f"  {doctype:30s}: {count:4d}")
        total += count
    print("-" * 45)
    print(f"  {'TOTAL':30s}: {total:4d}")
    print("=" * 60)
    return stats


# ─── CLI entry point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    generate_demo_data()
