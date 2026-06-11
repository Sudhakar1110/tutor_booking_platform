# Demo Data Script for Tutor Booking Platform
# Run: bench --site [sitename] console
# Then: exec(open("../apps/tutor_booking_platform/tutor_booking_platform/patches/demo_data.py").read())

import frappe
from datetime import date, time, datetime, timedelta
import random

def create_if_not_exists(doctype, name, data):
    """Create a document only if it doesn't already exist."""
    if not frappe.db.exists(doctype, name):
        doc = frappe.get_doc(data)
        doc.insert(ignore_permissions=True, ignore_mandatory=True)
        return doc.name
    return name

def random_date(start="2024-06-01", end="2024-12-31"):
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    return s + timedelta(days=random.randint(0, (e - s).days))

def random_time():
    return time(random.randint(8, 18), random.choice([0, 15, 30, 45]))

def main():
    print("=" * 60)
    print("TUTOR BOOKING PLATFORM - DEMO DATA CREATION")
    print("=" * 60)

    # =========================================================
    # 1. SUBJECT CATEGORIES
    # =========================================================
    print("\n--- Creating Subject Categories ---")
    subj_cats = {
        "School Subjects": "SSC-001",
        "Competitive Exams": "CMP-001",
        "Programming": "PRG-001",
        "Languages": "LNG-001",
        "Professional Skills": "PRF-001",
    }
    for name, code in subj_cats.items():
        create_if_not_exists("Subject Category", name, {
            "doctype": "Subject Category",
            "category_name": name,
            "category_code": code,
            "is_active": 1,
            "description": f"Category for {name.lower()}",
            "display_order": list(subj_cats.keys()).index(name) + 1,
        })
        print(f"  ✓ {name}")

    # =========================================================
    # 2. SUBJECTS
    # =========================================================
    print("\n--- Creating Subjects ---")
    subjects_data = [
        ("Mathematics", "School Subjects", "MAT-101", "Beginner", "All"),
        ("Physics", "School Subjects", "PHY-101", "Intermediate", "All"),
        ("Chemistry", "School Subjects", "CHE-101", "Intermediate", "All"),
        ("Biology", "School Subjects", "BIO-101", "Intermediate", "All"),
        ("English", "School Subjects", "ENG-101", "All Levels", "All"),
        ("IELTS", "Competitive Exams", "IEL-101", "Advanced", "Higher Secondary"),
        ("Java", "Programming", "JAV-101", "Intermediate", "Undergraduate"),
        ("Python", "Programming", "PYT-101", "Beginner", "Undergraduate"),
        ("Data Science", "Professional Skills", "DTS-101", "Advanced", "Postgraduate"),
        ("Aptitude", "Competitive Exams", "APT-101", "Intermediate", "All"),
    ]
    for name, cat, code, diff, audience in subjects_data:
        create_if_not_exists("Subject", name, {
            "doctype": "Subject",
            "subject_name": name,
            "subject_category": cat,
            "subject_code": code,
            "is_active": 1,
            "difficulty_level": diff,
            "target_audience": audience,
            "display_order": subjects_data.index((name, cat, code, diff, audience)) + 1,
        })
        print(f"  ✓ {name}")

    # =========================================================
    # 3. COURSE CATEGORIES
    # =========================================================
    print("\n--- Creating Course Categories ---")
    course_cats = ["Academic Courses", "IT Courses", "Language Courses", "Professional Courses"]
    for i, name in enumerate(course_cats):
        create_if_not_exists("Course Category", name, {
            "doctype": "Course Category",
            "category_name": name,
            "is_active": 1,
            "display_order": i + 1,
        })
        print(f"  ✓ {name}")

    # =========================================================
    # 4. COURSES (lookup by course_name field, not by naming series)
    # =========================================================
    print("\n--- Creating Courses ---")
    courses = [
        ("Python Programming", "IT Courses", "Python", 12, "Beginner", 15000),
        ("Java Full Stack", "IT Courses", "Java", 16, "Intermediate", 25000),
        ("Spoken English", "Language Courses", "English", 8, "Beginner", 8000),
        ("IELTS Preparation", "Language Courses", "IELTS", 10, "Advanced", 12000),
        ("Data Science", "IT Courses", "Data Science", 20, "Advanced", 35000),
        ("Mathematics Foundation", "Academic Courses", "Mathematics", 12, "Beginner", 10000),
    ]
    for name, cat, subj, weeks, level, fee in courses:
        if not frappe.db.get_value("Course", {"course_name": name}):
            doc = frappe.get_doc({
                "doctype": "Course",
                "course_name": name,
                "course_category": cat,
                "subject": subj,
                "is_active": 1,
                "duration_weeks": weeks,
                "level": level,
                "fee": fee,
            })
            doc.insert(ignore_permissions=True, ignore_mandatory=True)
            print(f"  ✓ {name}")
        else:
            print(f"  ✓ {name} (already exists)")

    # =========================================================
    # 5. SKILL CATEGORIES
    # =========================================================
    print("\n--- Creating Skill Categories ---")
    sk_cats = ["Technical Skills", "Language Skills", "Academic Skills"]
    for name in sk_cats:
        create_if_not_exists("Skill Category", name, {
            "doctype": "Skill Category",
            "category_name": name,
            "is_active": 1,
        })
        print(f"  ✓ {name}")

    # =========================================================
    # 6. SKILLS
    # =========================================================
    print("\n--- Creating Skills ---")
    skills = [
        ("Python", "Technical Skills"),
        ("Java", "Technical Skills"),
        ("SQL", "Technical Skills"),
        ("Communication", "Language Skills"),
        ("Mathematics", "Academic Skills"),
    ]
    for name, cat in skills:
        create_if_not_exists("Skill", name, {
            "doctype": "Skill",
            "skill_name": name,
            "skill_category": cat,
            "is_active": 1,
        })
        print(f"  ✓ {name}")

    # =========================================================
    # 7. TUTOR BOOKING SETTINGS
    # =========================================================
    print("\n--- Creating Tutor Booking Settings ---")
    if not frappe.db.exists("Tutor Booking Settings", "Tutor Booking Settings"):
        settings = frappe.get_doc({
            "doctype": "Tutor Booking Settings",
            "platform_name": "Tutor Booking Platform",
            "default_currency": "INR",
            "commission_percentage": 10,
            "support_email": "support@tutorbooking.com",
            "min_session_duration": 60,
            "max_advance_booking_days": 30,
            "auto_confirm_booking": 1,
            "session_reminder_hours": 24,
            "enable_demo_class": 1,
            "enable_online_class": 1,
            "enable_offline_class": 1,
            "rating_mandatory_after_session": 1,
            "enable_upi_payment": 1,
            "enable_card_payment": 1,
            "enable_cash_payment": 1,
            "payment_gateway": "Razorpay",
        })
        settings.insert(ignore_permissions=True)
        print("  ✓ Tutor Booking Settings")
    else:
        print("  ✓ Tutor Booking Settings (already exists)")

    # =========================================================
    # 8. TUTOR PROFILES
    # =========================================================
    print("\n--- Creating Tutor Profiles ---")
    tutors = [
        {"name": "Mathematics Tutor", "email": "math.tutor@example.com", "mobile": "9876543210", "subject": "Mathematics", "rate": 800, "exp": 5, "mode": "Both", "bio": "Experienced mathematics teacher with 5 years of experience teaching from class 6 to 12."},
        {"name": "Physics Tutor", "email": "physics.tutor@example.com", "mobile": "9876543211", "subject": "Physics", "rate": 1000, "exp": 7, "mode": "Both", "bio": "Physics expert specializing in conceptual teaching for high school and college students."},
        {"name": "Chemistry Tutor", "email": "chem.tutor@example.com", "mobile": "9876543212", "subject": "Chemistry", "rate": 900, "exp": 4, "mode": "Online", "bio": "Chemistry tutor making complex topics simple and interesting for students."},
        {"name": "Biology Tutor", "email": "bio.tutor@example.com", "mobile": "9876543213", "subject": "Biology", "rate": 850, "exp": 6, "mode": "Both", "bio": "Biology enthusiast with a passion for teaching life sciences to young minds."},
        {"name": "English Tutor", "email": "eng.tutor@example.com", "mobile": "9876543214", "subject": "English", "rate": 700, "exp": 8, "mode": "Online", "bio": "English literature and language expert helping students excel in communication."},
        {"name": "IELTS Trainer", "email": "ielts.tutor@example.com", "mobile": "9876543215", "subject": "IELTS", "rate": 1500, "exp": 10, "mode": "Both", "bio": "Certified IELTS trainer with 10 years of experience. 500+ students trained."},
        {"name": "Spoken English Trainer", "email": "spoken.tutor@example.com", "mobile": "9876543216", "subject": "English", "rate": 600, "exp": 3, "mode": "Online", "bio": "Spoken English specialist focusing on fluency and accent neutralization."},
        {"name": "Java Trainer", "email": "java.tutor@example.com", "mobile": "9876543217", "subject": "Java", "rate": 1200, "exp": 8, "mode": "Online", "bio": "Senior Java developer turned teacher. Expert in Java, Spring Boot, and Microservices."},
        {"name": "Python Trainer", "email": "python.tutor@example.com", "mobile": "9876543218", "subject": "Python", "rate": 1100, "exp": 6, "mode": "Online", "bio": "Python expert teaching from basics to advanced data science and machine learning."},
        {"name": "Data Science Trainer", "email": "ds.tutor@example.com", "mobile": "9876543219", "subject": "Data Science", "rate": 2000, "exp": 9, "mode": "Online", "bio": "Data scientist with industry experience teaching ML, AI, and data analytics."},
    ]
    tutor_names = []
    for t in tutors:
        docname = f"TUT-2024-{tutors.index(t) + 1:04d}"
        create_if_not_exists("Tutor Profile", docname, {
            "doctype": "Tutor Profile",
            "tutor_name": t["name"],
            "email": t["email"],
            "mobile": t["mobile"],
            "teaching_mode": t["mode"],
            "experience_years": t["exp"],
            "hourly_rate": t["rate"],
            "primary_subject": t["subject"],
            "short_bio": t["bio"],
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
            "verification_status": "Verified",
            "is_active": 1,
            "teaching_levels": "All Levels",
            "languages_known": "English, Hindi",
            "average_rating": round(random.uniform(3.5, 5.0), 1),
        })
        tutor_names.append(docname)
        print(f"  ✓ {t['name']} ({docname})")

    # =========================================================
    # 9. TUTOR QUALIFICATIONS (one per tutor)
    # =========================================================
    print("\n--- Creating Tutor Qualifications ---")
    quals = [
        ("B.Sc. Mathematics", "Mathematics", "University of Mumbai", 2015),
        ("M.Sc. Physics", "Physics", "IIT Bombay", 2014),
        ("Ph.D. Chemistry", "Chemistry", "University of Delhi", 2018),
        ("M.Sc. Biotechnology", "Biology", "JNU", 2016),
        ("M.A. English Literature", "English", "University of Calcutta", 2013),
        ("M.A. TESOL", "English Language", "University of Cambridge", 2012),
        ("B.A. English", "English", "University of Mumbai", 2019),
        ("B.Tech Computer Science", "Computer Science", "IIT Delhi", 2014),
        ("M.Sc. Data Science", "Data Science", "IIIT Bangalore", 2017),
        ("Ph.D. Data Science", "Machine Learning", "IIT Madras", 2015),
    ]
    for i, (deg, field, inst, year) in enumerate(quals):
        if i < len(tutor_names):
            qname = f"TQAL-2024-{i+1:04d}"
            create_if_not_exists("Tutor Qualification", qname, {
                "doctype": "Tutor Qualification",
                "tutor_profile": tutor_names[i],
                "degree": deg,
                "field_of_study": field,
                "institution": inst,
                "passing_year": year,
                "is_verified": 1,
            })
            print(f"  ✓ {deg} → {tutors[i]['name']}")

    # =========================================================
    # 10. TUTOR EXPERIENCES (one per tutor)
    # =========================================================
    print("\n--- Creating Tutor Experiences ---")
    experiences = [
        ("Bright Academy", "Mathematics Teacher", "Full Time"),
        ("Excel Institute", "Physics Faculty", "Full Time"),
        ("Smart Learning", "Chemistry Teacher", "Full Time"),
        ("BioGenius Academy", "Biology Faculty", "Full Time"),
        ("Language First", "English Teacher", "Full Time"),
        ("IELTS Pro", "IELTS Trainer", "Full Time"),
        ("SpeakEasy Academy", "English Trainer", "Part Time"),
        ("TechLearn", "Java Instructor", "Full Time"),
        ("CodeCamp", "Python Trainer", "Freelance"),
        ("DataMinds Institute", "Data Science Faculty", "Full Time"),
    ]
    for i, (org, role, etype) in enumerate(experiences):
        if i < len(tutor_names):
            ename = f"TEXP-2024-{i+1:04d}"
            create_if_not_exists("Tutor Experience", ename, {
                "doctype": "Tutor Experience",
                "tutor_profile": tutor_names[i],
                "organization_name": org,
                "role_title": role,
                "employment_type": etype,
                "from_date": date(year=2018 + i % 4, month=6, day=1),
                "is_current": 1,
            })
            print(f"  ✓ {org} → {tutors[i]['name']}")

    # =========================================================
    # 11. TUTOR CERTIFICATIONS (one per tutor)
    # =========================================================
    print("\n--- Creating Tutor Certifications ---")
    certs = [
        ("Certified Math Teacher (CMT)", "Math Certification Board", "CMT-001"),
        ("Physics Teaching Certification", "IIT Academy", "PTC-001"),
        ("Certified Chemistry Educator", "Royal Society of Chemistry", "CCE-001"),
        ("Biology Teaching License", "BioEd International", "BTL-001"),
        ("TEFL Certification", "International TEFL Academy", "TEFL-001"),
        ("IELTS Examiner Certification", "British Council", "IEC-001"),
        ("Certified English Trainer", "Cambridge English", "CET-001"),
        ("Oracle Certified Java Programmer", "Oracle", "OCJP-001"),
        ("Python Institute Certified", "Python Software Foundation", "PCPP-001"),
        ("AWS Certified Data Analytics", "Amazon Web Services", "AWS-DA-001"),
    ]
    for i, (cname, auth, cid) in enumerate(certs):
        if i < len(tutor_names):
            tcname = f"TCER-2024-{i+1:04d}"
            create_if_not_exists("Tutor Certification", tcname, {
                "doctype": "Tutor Certification",
                "tutor_profile": tutor_names[i],
                "certification_name": cname,
                "issuing_authority": auth,
                "certification_id": cid,
                "is_lifetime_valid": 1,
                "issue_date": date(2020, 1 + i, 1),
                "is_verified": 1,
            })
            print(f"  ✓ {cname} → {tutors[i]['name']}")

    # =========================================================
    # 12. TUTOR AVAILABILITIES (2 per tutor)
    # =========================================================
    print("\n--- Creating Tutor Availabilities ---")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i, tn in enumerate(tutor_names):
        for shift in range(2):
            day = days[(i * 2 + shift) % 7]
            aname = f"TAVA-2024-{(i*2)+shift+1:04d}"
            create_if_not_exists("Tutor Availability", aname, {
                "doctype": "Tutor Availability",
                "tutor_profile": tn,
                "day_of_week": day,
                "start_time": time(9 + shift * 4, 0, 0),
                "end_time": time(13 + shift * 4, 0, 0),
                "is_available": 1,
                "teaching_mode": tutors[i]["mode"],
            })
        print(f"  ✓ {tutors[i]['name']} (2 slots)")

    # =========================================================
    # 13. TUTOR VERIFICATIONS (one per tutor)
    # =========================================================
    print("\n--- Creating Tutor Verifications ---")
    for i, tn in enumerate(tutor_names):
        vname = f"TVER-2024-{i+1:04d}"
        create_if_not_exists("Tutor Verification", vname, {
            "doctype": "Tutor Verification",
            "tutor_profile": tn,
            "verification_status": "Verified",
            "verification_type": "Full Verification",
            "id_proof_type": "Aadhaar",
            "id_proof_number": f"XXXX-XXXX-{4000+i:04d}",
            "verification_date": random_date("2024-01-01", "2024-06-01"),
        })
        print(f"  ✓ {tutors[i]['name']} (Verified)")

    # =========================================================
    # 14. STUDENT PROFILES
    # =========================================================
    print("\n--- Creating Student Profiles ---")
    students = [
        # School Students
        ("Aarav Sharma", "Class 9", "Delhi Public School", "CBSE", "school"),
        ("Ananya Patel", "Class 10", "St. Mary's School", "ICSE", "school"),
        ("Rohit Singh", "Class 11", "Kendriya Vidyalaya", "CBSE", "school"),
        ("Priya Gupta", "Class 12", "DAV Public School", "CBSE", "school"),
        ("Amit Kumar", "Class 8", "Bishop Cotton School", "ICSE", "school"),
        ("Sneha Reddy", "Class 10", "Chinmaya Vidyalaya", "CBSE", "school"),
        ("Arjun Nair", "Class 12", "Saraswati School", "State Board", "school"),
        ("Neha Joshi", "Class 9", "St. Joseph's School", "ICSE", "school"),
        # College Students
        ("Vikram Desai", "Undergraduate", "IIT Bombay", "CBSE", "college"),
        ("Kavita Mehta", "Undergraduate", "Delhi University", "Other", "college"),
        ("Rajesh Iyer", "Postgraduate", "IIT Madras", "Other", "college"),
        ("Pooja Verma", "Undergraduate", "Mithibai College", "Other", "college"),
        ("Akash Malhotra", "Undergraduate", "VIT Vellore", "CBSE", "college"),
        ("Divya Rao", "Postgraduate", "BITS Pilani", "Other", "college"),
        # Working Professionals
        ("Suresh Pillai", "Working Professional", "", "", "professional"),
        ("Deepa Kulkarni", "Working Professional", "", "", "professional"),
        ("Manoj Tiwari", "Working Professional", "", "", "professional"),
        ("Rekha Jain", "Working Professional", "", "", "professional"),
        ("Ganesh Iyengar", "Working Professional", "", "", "professional"),
        ("Lata Krishnan", "Working Professional", "", "", "professional"),
    ]
    student_names = []
    for i, (name, cls, school, board, stype) in enumerate(students):
        sname = f"STU-2024-{i+1:04d}"
        data = {
            "doctype": "Student Profile",
            "student_name": name,
            "email": f"{name.lower().replace(' ', '.')}@example.com",
            "mobile": f"998877{6000+i:04d}",
            "current_class": cls,
            "school_college": school,
            "board": board if cls != "Working Professional" else "",
            "is_active": 1,
            "preferred_learning_mode": "Online",
            "preferred_timing": "Evening",
            "budget_per_hour": random.choice([500, 800, 1000, 1500, 2000]),
        }
        create_if_not_exists("Student Profile", sname, data)
        student_names.append(sname)
        print(f"  ✓ {name} ({stype})")

    # =========================================================
    # 15. STUDENT ADDRESSES
    # =========================================================
    print("\n--- Creating Student Addresses ---")
    cities_mumbai = ["Andheri", "Bandra", "Juhu", "Malad", "Thane", "Powai", "Borivali", "Dadar"]
    for i, sn in enumerate(student_names):
        aname = f"SADR-2024-{i+1:04d}"
        create_if_not_exists("Student Address", aname, {
            "doctype": "Student Address",
            "student_profile": sn,
            "address_type": "Home",
            "is_default": 1,
            "address_line1": f"{100 + i} Main Street",
            "city": cities_mumbai[i % len(cities_mumbai)],
            "state": "Maharashtra",
            "pincode": f"4000{50+i:02d}",
        })
        print(f"  ✓ {students[i][0]}")

    # =========================================================
    # 16. STUDENT REQUIREMENTS
    # =========================================================
    print("\n--- Creating Student Requirements ---")
    req_subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Python", "Java", "IELTS", "Data Science", "Aptitude"]
    for i, sn in enumerate(student_names):
        rname = f"SREQ-2024-{i+1:04d}"
        subj = req_subjects[i % len(req_subjects)]
        create_if_not_exists("Student Requirement", rname, {
            "doctype": "Student Requirement",
            "student_profile": sn,
            "subject": subj,
            "requirement_title": f"Need help with {subj}",
            "status": "Open",
            "preferred_mode": "Online",
            "budget_per_hour": random.choice([500, 800, 1000]),
            "urgency": random.choice(["Low", "Medium", "High"]),
            "requirement_date": random_date(),
        })
        print(f"  ✓ {students[i][0]} → {subj}")

    # =========================================================
    # 17. STUDENT PREFERENCES
    # =========================================================
    print("\n--- Creating Student Preferences ---")
    goals = ["Exam Preparation", "Skill Development", "Career Advancement", "General Knowledge"]
    for i, sn in enumerate(student_names):
        pname = f"SPRF-2024-{i+1:04d}"
        create_if_not_exists("Student Preference", pname, {
            "doctype": "Student Preference",
            "student_profile": sn,
            "subject": req_subjects[i % len(req_subjects)],
            "preferred_tutor_gender": "Any",
            "preferred_language": "English",
            "learning_goal": goals[i % len(goals)],
            "weekly_hours": random.choice([2, 3, 4, 6]),
        })
        print(f"  ✓ {students[i][0]}")

    # =========================================================
    # 18. TUTOR SEARCH REQUESTS
    # =========================================================
    print("\n--- Creating Tutor Search Requests ---")
    for i in range(15):
        sn = student_names[i % len(student_names)]
        subj = req_subjects[i % len(req_subjects)]
        tn = tutor_names[i % len(tutor_names)]
        srname = f"TSRQ-2024-{i+1:04d}"
        create_if_not_exists("Tutor Search Request", srname, {
            "doctype": "Tutor Search Request",
            "student_profile": sn,
            "subject": subj,
            "teaching_mode": "Online",
            "status": random.choice(["Searching", "Matched", "Closed"]),
            "max_budget": random.choice([500, 800, 1000, 1500, 2000]),
            "preferred_gender": "Any",
            "search_date": random_date("2024-06-01", "2024-09-30"),
        })
        print(f"  ✓ Search #{i+1}")

    # =========================================================
    # 19. TUTOR MATCH RESULTS
    # =========================================================
    print("\n--- Creating Tutor Match Results ---")
    for i in range(15):
        srname = f"TSRQ-2024-{i+1:04d}"
        tn = tutor_names[i % len(tutor_names)]
        mrname = f"TMRS-2024-{i+1:04d}"
        create_if_not_exists("Tutor Match Result", mrname, {
            "doctype": "Tutor Match Result",
            "search_request": srname,
            "tutor_profile": tn,
            "match_score": round(random.uniform(75, 98), 1),
            "status": random.choice(["Suggested", "Shortlisted", "Contacted", "Booked"]),
            "match_date": random_date("2024-06-01", "2024-10-31"),
        })
        print(f"  ✓ Match #{i+1}")

    # =========================================================
    # 20. DEMO CLASS REQUESTS
    # =========================================================
    print("\n--- Creating Demo Class Requests ---")
    for i in range(10):
        sn = student_names[i % len(student_names)]
        tn = tutor_names[i % len(tutor_names)]
        subj = req_subjects[i % len(req_subjects)]
        drname = f"DMRQ-2024-{i+1:04d}"
        create_if_not_exists("Demo Class Request", drname, {
            "doctype": "Demo Class Request",
            "student_profile": sn,
            "tutor_profile": tn,
            "subject": subj,
            "status": random.choice(["Approved", "Scheduled", "Completed"]),
            "preferred_date": random_date("2024-07-01", "2024-11-30"),
            "preferred_time": time(10, 0, 0),
            "mode": "Online",
        })
        print(f"  ✓ Demo Request #{i+1}")

    # =========================================================
    # 21. DEMO CLASS SCHEDULES
    # =========================================================
    print("\n--- Creating Demo Class Schedules ---")
    for i in range(10):
        drname = f"DMRQ-2024-{i+1:04d}"
        tn = tutor_names[i % len(tutor_names)]
        sn = student_names[i % len(student_names)]
        dsname = f"DMSC-2024-{i+1:04d}"
        create_if_not_exists("Demo Class Schedule", dsname, {
            "doctype": "Demo Class Schedule",
            "demo_class_request": drname,
            "tutor_profile": tn,
            "student_profile": sn,
            "status": random.choice(["Scheduled", "Completed"]),
            "scheduled_date": random_date("2024-07-15", "2024-12-15"),
            "start_time": time(11, 0, 0),
            "end_time": time(12, 0, 0),
            "duration_minutes": 60,
            "mode": "Online",
        })
        print(f"  ✓ Demo Schedule #{i+1}")

    # =========================================================
    # 22. TUTOR BOOKINGS
    # =========================================================
    print("\n--- Creating Tutor Bookings ---")
    booking_names = []
    for i in range(20):
        sn = student_names[i % len(student_names)]
        tn = tutor_names[i % len(tutor_names)]
        subj = req_subjects[i % len(req_subjects)]
        rate = random.choice([500, 800, 1000, 1500, 2500])
        hours = random.choice([10, 20, 30, 40])
        bname = f"TBKN-2024-{i+1:04d}"
        create_if_not_exists("Tutor Booking", bname, {
            "doctype": "Tutor Booking",
            "booking_title": f"{subj} tutoring - {students[i % len(students)][0]}",
            "booking_status": random.choice(["Confirmed", "Active", "Completed"]),
            "student_profile": sn,
            "tutor_profile": tn,
            "subject": subj,
            "course": random.choice(["Python Programming", "Java Full Stack", "", "Spoken English", ""]),
            "teaching_mode": "Online",
            "booking_date": random_date("2024-06-01", "2024-11-01"),
            "start_date": random_date("2024-06-15", "2024-09-01"),
            "end_date": random_date("2024-09-15", "2024-12-31"),
            "sessions_per_week": random.choice([2, 3]),
            "hours_per_session": 1,
            "rate_per_hour": rate,
            "total_hours": hours,
            "total_amount": rate * hours,
            "payment_status": random.choice(["Paid", "Partially Paid", "Unpaid"]),
        })
        booking_names.append(bname)
        print(f"  ✓ Booking #{i+1}: {subj}")

    # =========================================================
    # 23. TUTOR SESSIONS
    # =========================================================
    print("\n--- Creating Tutor Sessions ---")
    session_names = []
    for i in range(30):
        bk = booking_names[i % len(booking_names)]
        tn = tutor_names[i % len(tutor_names)]
        sn = student_names[i % len(student_names)]
        subj = req_subjects[i % len(req_subjects)]
        sdate = random_date("2024-07-01", "2024-12-20")
        st = random_time()
        sesname = f"TSES-2024.{sdate.month:02d}.{i+1:04d}"
        create_if_not_exists("Tutor Session", sesname, {
            "doctype": "Tutor Session",
            "tutor_booking": bk,
            "tutor_profile": tn,
            "student_profile": sn,
            "status": random.choice(["Scheduled", "Completed", "Completed", "Completed"]),
            "session_date": sdate,
            "start_time": st,
            "end_time": time(st.hour + 1, st.minute, 0),
            "duration_minutes": 60,
            "subject": subj,
            "mode": "Online",
            "session_number": (i % 10) + 1,
        })
        session_names.append(sesname)
        print(f"  ✓ Session #{i+1}")

    # =========================================================
    # 24. ONLINE CLASSES
    # =========================================================
    print("\n--- Creating Online Classes ---")
    for i in range(10):
        tn = tutor_names[i % len(tutor_names)]
        subj = req_subjects[i % len(req_subjects)]
        ocname = f"ONCL-2024-{i+1:04d}"
        create_if_not_exists("Online Class", ocname, {
            "doctype": "Online Class",
            "class_title": f"{subj} - Live Session {i+1}",
            "tutor_profile": tn,
            "subject": subj,
            "status": random.choice(["Scheduled", "Completed", "Live"]),
            "class_date": random_date("2024-07-01", "2024-12-31"),
            "start_time": time(10, 0, 0),
            "end_time": time(11, 30, 0),
            "max_students": 30,
            "platform": "Zoom",
            "meeting_link": f"https://zoom.us/j/12345678{i:02d}",
        })
        print(f"  ✓ Online Class #{i+1}: {subj}")

    # =========================================================
    # 25. OFFLINE CLASSES
    # =========================================================
    print("\n--- Creating Offline Classes ---")
    locations = ["Andheri", "Bandra", "Powai", "Thane", "Malad", "Dadar", "Borivali", "Chembur", "Vashi", "Nerul"]
    for i in range(10):
        tn = tutor_names[i % len(tutor_names)]
        subj = req_subjects[i % len(req_subjects)]
        ofname = f"OFCL-2024-{i+1:04d}"
        create_if_not_exists("Offline Class", ofname, {
            "doctype": "Offline Class",
            "class_title": f"{subj} - Classroom {i+1}",
            "tutor_profile": tn,
            "subject": subj,
            "status": random.choice(["Scheduled", "Completed", "Completed"]),
            "class_date": random_date("2024-07-01", "2024-12-31"),
            "start_time": time(9, 0, 0),
            "end_time": time(11, 0, 0),
            "location": f"{locations[i]} Learning Center",
            "city": "Mumbai",
            "max_students": 20,
        })
        print(f"  ✓ Offline Class #{i+1}: {subj}")

    # =========================================================
    # 26. LEARNING SCHEDULES
    # =========================================================
    print("\n--- Creating Learning Schedules ---")
    for i in range(20):
        bk = booking_names[i % len(booking_names)]
        sn = student_names[i % len(student_names)]
        tn = tutor_names[i % len(tutor_names)]
        lsname = f"LSCH-2024-{i+1:04d}"
        create_if_not_exists("Learning Schedule", lsname, {
            "doctype": "Learning Schedule",
            "tutor_booking": bk,
            "student_profile": sn,
            "tutor_profile": tn,
            "subject": req_subjects[i % len(req_subjects)],
            "day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][i % 5],
            "start_time": time(16 + i % 4, 0, 0),
            "end_time": time(17 + i % 4, 0, 0),
            "is_active": 1,
            "valid_from": date(2024, 7, 1),
            "valid_to": date(2024, 12, 31),
        })
        print(f"  ✓ Learning Schedule #{i+1}")

    # =========================================================
    # 27. ATTENDANCE RECORDS
    # =========================================================
    print("\n--- Creating Attendance Records ---")
    for i in range(50):
        sesname = session_names[i % len(session_names)]
        sn = student_names[i % len(student_names)]
        tn = tutor_names[i % len(tutor_names)]
        atname = f"ATRC-2024.{random.randint(7,12):02d}.{i+1:04d}"
        sdate = random_date("2024-07-01", "2024-12-15")
        create_if_not_exists("Attendance Record", atname, {
            "doctype": "Attendance Record",
            "tutor_session": sesname,
            "student_profile": sn,
            "tutor_profile": tn,
            "subject": req_subjects[i % len(req_subjects)],
            "attendance_date": sdate,
            "status": random.choice(["Present", "Present", "Present", "Absent", "Late"]),
            "check_in_time": time(9, 0, 0),
            "check_out_time": time(10, 0, 0),
        })
        print(f"  ✓ Attendance #{i+1}")

    # =========================================================
    # 28. LEARNING PROGRESS
    # =========================================================
    print("\n--- Creating Learning Progress ---")
    for i in range(20):
        sn = student_names[i % len(student_names)]
        tn = tutor_names[i % len(tutor_names)]
        subj = req_subjects[i % len(req_subjects)]
        bk = booking_names[i % len(booking_names)]
        lpname = f"LPRG-2024-{i+1:04d}"
        create_if_not_exists("Learning Progress", lpname, {
            "doctype": "Learning Progress",
            "student_profile": sn,
            "tutor_profile": tn,
            "subject": subj,
            "tutor_booking": bk,
            "sessions_completed": random.randint(3, 15),
            "sessions_attended": random.randint(3, 15),
            "total_hours": random.randint(5, 30),
            "completion_percentage": random.randint(20, 90),
            "performance_rating": random.choice(["Excellent", "Good", "Average"]),
            "last_updated": random_date("2024-09-01", "2024-12-31"),
        })
        print(f"  ✓ Progress #{i+1}")

    # =========================================================
    # 29. PAYMENT TRANSACTIONS
    # =========================================================
    print("\n--- Creating Payment Transactions ---")
    for i in range(20):
        bk = booking_names[i % len(booking_names)]
        sn = student_names[i % len(student_names)]
        tn = tutor_names[i % len(tutor_names)]
        amount = random.choice([500, 1000, 1500, 2500, 5000])
        ptname = f"PTXN-2024.{random.randint(7,12):02d}.{i+1:04d}"
        create_if_not_exists("Payment Transaction", ptname, {
            "doctype": "Payment Transaction",
            "tutor_booking": bk,
            "student_profile": sn,
            "tutor_profile": tn,
            "payment_status": random.choice(["Completed", "Completed", "Completed", "Pending"]),
            "amount": amount,
            "platform_commission": round(amount * 0.1, 2),
            "tutor_payout": round(amount * 0.9, 2),
            "payment_method": random.choice(["UPI", "Card", "Cash", "Bank Transfer"]),
            "payment_date": random_date("2024-07-01", "2024-12-31"),
            "currency": "INR",
        })
        print(f"  ✓ Payment #{i+1}: ₹{amount}")

    # =========================================================
    # 30. CARD PAYMENTS
    # =========================================================
    print("\n--- Creating Card Payments ---")
    for i in range(10):
        bk = booking_names[i % len(booking_names)]
        ptname = f"PTXN-2024.{random.randint(7,12):02d}.{i+21:04d}"
        create_if_not_exists("Card Payment", f"CRDP-2024-{i+1:04d}", {
            "doctype": "Card Payment",
            "payment_transaction": ptname,
            "tutor_booking": bk,
            "amount": random.choice([1000, 1500, 2500, 5000]),
            "payment_status": "Success",
            "card_type": random.choice(["Visa", "Mastercard", "RuPay"]),
            "card_last_four": f"{random.randint(1000, 9999)}",
            "gateway": "Razorpay",
            "payment_date": random_date("2024-07-01", "2024-12-31"),
        })
        print(f"  ✓ Card Payment #{i+1}")

    # =========================================================
    # 31. CASH PAYMENTS
    # =========================================================
    print("\n--- Creating Cash Payments ---")
    for i in range(10):
        bk = booking_names[(i+10) % len(booking_names)]
        ptname = f"PTXN-2024.{random.randint(7,12):02d}.{i+31:04d}"
        create_if_not_exists("Cash Payment", f"CSHP-2024-{i+1:04d}", {
            "doctype": "Cash Payment",
            "payment_transaction": ptname,
            "tutor_booking": bk,
            "amount": random.choice([500, 800, 1000]),
            "payment_status": "Received",
            "receipt_number": f"RCP-{1000+i}",
            "payment_date": random_date("2024-07-01", "2024-12-31"),
        })
        print(f"  ✓ Cash Payment #{i+1}")

    # =========================================================
    # 32. REFUND REQUESTS
    # =========================================================
    print("\n--- Creating Refund Requests ---")
    for i in range(5):
        bk = booking_names[i % len(booking_names)]
        sn = student_names[i % len(student_names)]
        amount = random.choice([500, 1000, 1500])
        rfname = f"RFND-2024.{i+1:04d}"
        create_if_not_exists("Refund Request", rfname, {
            "doctype": "Refund Request",
            "tutor_booking": bk,
            "student_profile": sn,
            "refund_status": random.choice(["Approved", "Processed"]),
            "original_amount": amount + 500,
            "refund_amount": amount,
            "refund_method": "Original Payment Method",
            "refund_date": random_date("2024-08-01", "2024-12-31"),
            "reason": random.choice(["Session Quality Issue", "Schedule Change", "Other"]),
        })
        print(f"  ✓ Refund #{i+1}: ₹{amount}")

    # =========================================================
    # 33. TUTOR REVIEWS
    # =========================================================
    print("\n--- Creating Tutor Reviews ---")
    review_texts = [
        "Excellent teaching methodology! The concepts were explained very clearly.",
        "Very patient and knowledgeable tutor. Highly recommend.",
        "Great session! My child improved significantly in the subject.",
        "Wonderful tutor who makes learning enjoyable and engaging.",
        "Professional and dedicated. Always well-prepared for sessions.",
    ]
    for i in range(25):
        tn = tutor_names[i % len(tutor_names)]
        sn = student_names[i % len(student_names)]
        bk = booking_names[i % len(booking_names)] if i < len(booking_names) else booking_names[0]
        rvname = f"TRVW-2024.{i+1:04d}"
        rating_val = random.choice([3, 4, 4, 5, 5])
        create_if_not_exists("Tutor Review", rvname, {
            "doctype": "Tutor Review",
            "tutor_profile": tn,
            "student_profile": sn,
            "tutor_booking": bk,
            "review_date": random_date("2024-08-01", "2024-12-31"),
            "rating": rating_val,
            "teaching_quality": rating_val,
            "punctuality": rating_val,
            "communication": rating_val,
            "is_approved": 1,
            "review_title": f"{'Excellent' if rating_val >= 4 else 'Good'} Tutor",
            "review_text": random.choice(review_texts),
        })
        print(f"  ✓ Review #{i+1}")

    # =========================================================
    # 34. TUTOR RATINGS
    # =========================================================
    print("\n--- Creating Tutor Ratings ---")
    for i in range(25):
        tn = tutor_names[i % len(tutor_names)]
        sn = student_names[i % len(student_names)]
        sesname = session_names[i % len(session_names)] if i < len(session_names) else session_names[0]
        rtname = f"TRAT-2024.{i+1:04d}"
        rating_val = random.choice([4, 4.5, 5])
        create_if_not_exists("Tutor Rating", rtname, {
            "doctype": "Tutor Rating",
            "tutor_profile": tn,
            "student_profile": sn,
            "tutor_session": sesname,
            "rating_date": random_date("2024-08-01", "2024-12-31"),
            "overall_rating": rating_val,
            "subject_knowledge": rating_val,
            "teaching_methodology": rating_val,
            "punctuality": rating_val,
            "communication_skills": rating_val,
            "would_recommend": 1,
        })
        print(f"  ✓ Rating #{i+1}")

    # =========================================================
    # 35. STUDENT FEEDBACK
    # =========================================================
    print("\n--- Creating Student Feedback ---")
    for i in range(15):
        sn = student_names[i % len(student_names)]
        tn = tutor_names[i % len(tutor_names)]
        sesname = session_names[i % len(session_names)] if i < len(session_names) else session_names[0]
        sfname = f"SFBK-2024.{i+1:04d}"
        create_if_not_exists("Student Feedback", sfname, {
            "doctype": "Student Feedback",
            "student_profile": sn,
            "tutor_profile": tn,
            "tutor_session": sesname,
            "feedback_date": random_date("2024-09-01", "2024-12-31"),
            "session_helpful": 1,
            "topics_covered": random.choice(["Algebra, Calculus", "Newton's Laws", "Organic Chemistry", "Cell Biology", "Grammar & Writing"]),
            "difficulty_level": "Just Right",
            "overall_experience": random.choice(["Excellent", "Good"]),
            "feedback_text": random.choice(review_texts),
        })
        print(f"  ✓ Feedback #{i+1}")

    # =========================================================
    # 36. NOTIFICATION LOGS
    # =========================================================
    print("\n--- Creating Notification Logs ---")
    notif_types = ["Booking Created", "Booking Confirmed", "Session Reminder", "Payment", "Review"]
    for i in range(20):
        nname = f"NLOG-2024.{random.randint(7,12):02d}.{i+1:04d}"
        notif_type = random.choice(notif_types)
        create_if_not_exists("Notification Log", nname, {
            "doctype": "Notification Log",
            "recipient": student_names[i % len(student_names)],
            "notification_type": notif_type,
            "status": random.choice(["Sent", "Read"]),
            "subject": f"{notif_type} Notification",
            "message": f"This is a notification regarding {notif_type.lower()}.",
        })
        print(f"  ✓ Notification #{i+1}")

    # =========================================================
    # 37. MESSAGE THREADS
    # =========================================================
    print("\n--- Creating Message Threads ---")
    thread_names = []
    for i in range(20):
        tn = tutor_names[i % len(tutor_names)]
        sn = student_names[i % len(student_names)]
        bk = booking_names[i % len(booking_names)] if i < len(booking_names) else booking_names[0]
        thrname = f"MTHR-2024.{i+1:04d}"
        create_if_not_exists("Message Thread", thrname, {
            "doctype": "Message Thread",
            "thread_title": f"{students[i % len(students)][0]} - {tutors[i % len(tutors)]['name']}",
            "tutor_profile": tn,
            "student_profile": sn,
            "tutor_booking": bk,
            "status": "Active",
        })
        thread_names.append(thrname)
        print(f"  ✓ Thread #{i+1}")

    # =========================================================
    # 38. CHAT MESSAGES
    # =========================================================
    print("\n--- Creating Chat Messages ---")
    chat_texts = [
        "Hi, I have a doubt about today's homework.",
        "Sure, please share your question.",
        "Can we reschedule tomorrow's session?",
        "Yes, what time works for you?",
        "The session was very helpful. Thank you!",
        "Please complete the practice problems before our next class.",
        "I've shared the study material. Please review it.",
        "Great progress today! Keep it up.",
    ]
    for i in range(50):
        thr = thread_names[i % len(thread_names)]
        is_tutor = random.choice([True, False])
        cname = f"CMSG-2024.{random.randint(7,12):02d}.{i+1:04d}"
        create_if_not_exists("Chat Message", cname, {
            "doctype": "Chat Message",
            "message_thread": thr,
            "sender": "Tutor" if is_tutor else "Student",
            "sender_type": "Tutor" if is_tutor else "Student",
            "message_type": "Text",
            "message_text": random.choice(chat_texts),
            "sent_at": datetime.combine(random_date("2024-08-01", "2024-12-31"), random_time()),
            "is_read": random.choice([0, 1]),
        })
        print(f"  ✓ Chat #{i+1}")

    # =========================================================
    # 39. REMINDER SCHEDULES
    # =========================================================
    print("\n--- Creating Reminder Schedules ---")
    for i in range(10):
        rname = f"RMND-2024.{i+1:04d}"
        create_if_not_exists("Reminder Schedule", rname, {
            "doctype": "Reminder Schedule",
            "reminder_title": random.choice([
                "Session Reminder", "Payment Due Reminder",
                "Demo Class Reminder", "Homework Reminder",
            ]),
            "reminder_type": random.choice(["Session Reminder", "Payment Due", "General"]),
            "recipient_type": random.choice(["Tutor", "Student", "Both"]),
            "is_active": 1,
            "frequency": random.choice(["One Time", "Daily", "Weekly"]),
            "send_before_hours": 24,
            "send_time": time(9, 0, 0),
            "template_message": "This is a friendly reminder about your upcoming session.",
        })
        print(f"  ✓ Reminder #{i+1}")

    # =========================================================
    # SUMMARY
    # =========================================================
    print("\n" + "=" * 60)
    print("DEMO DATA CREATION COMPLETE!")
    print("=" * 60)
    print(f"\nSummary of records created:")
    print(f"  Subject Categories: {len(subj_cats)}")
    print(f"  Subjects: {len(subjects_data)}")
    print(f"  Course Categories: {len(course_cats)}")
    print(f"  Courses: {len(courses)}")
    print(f"  Skill Categories: {len(sk_cats)}")
    print(f"  Skills: {len(skills)}")
    print(f"  Tutor Profiles: {len(tutors)}")
    print(f"  Tutor Qualifications: {len(quals[:10])}")
    print(f"  Tutor Experiences: {len(experiences[:10])}")
    print(f"  Tutor Certifications: {len(certs[:10])}")
    print(f"  Tutor Availabilities: {len(tutors) * 2}")
    print(f"  Tutor Verifications: {len(tutors)}")
    print(f"  Student Profiles: {len(students)}")
    print(f"  Student Addresses: {len(students)}")
    print(f"  Student Requirements: {len(students)}")
    print(f"  Student Preferences: {len(students)}")
    print(f"  Tutor Search Requests: 15")
    print(f"  Tutor Match Results: 15")
    print(f"  Demo Class Requests: 10")
    print(f"  Demo Class Schedules: 10")
    print(f"  Tutor Bookings: 20")
    print(f"  Tutor Sessions: 30")
    print(f"  Online Classes: 10")
    print(f"  Offline Classes: 10")
    print(f"  Learning Schedules: 20")
    print(f"  Attendance Records: 50")
    print(f"  Learning Progress: 20")
    print(f"  Payment Transactions: 20")
    print(f"  Card Payments: 10")
    print(f"  Cash Payments: 10")
    print(f"  Refund Requests: 5")
    print(f"  Tutor Reviews: 25")
    print(f"  Tutor Ratings: 25")
    print(f"  Student Feedback: 15")
    print(f"  Notification Logs: 20")
    print(f"  Message Threads: 20")
    print(f"  Chat Messages: 50")
    print(f"  Reminder Schedules: 10")
    print(f"  Tutor Booking Settings: 1")
    print("\n✅ DONE! All demo data created successfully.")

main()
