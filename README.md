# Tutor Booking Platform

[![Frappe](https://img.shields.io/badge/Frappe-v15-blue)](https://frappe.io)
[![ERPNext](https://img.shields.io/badge/ERPNext-v15-green)](https://erpnext.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A production-ready **Tutor Booking Platform** (similar to UrbanPro) built as a custom Frappe app on ERPNext v15+.

## Modules

| Module | DocTypes |
|--------|----------|
| Tutor Management | Tutor Profile, Tutor Qualification, Tutor Experience, Tutor Certification, Tutor Availability, Tutor Verification |
| Student Management | Student Profile, Student Requirement, Student Address, Student Preference |
| Subject & Course Management | Subject Category, Subject, Course Category, Course, Skill Category, Skill |
| Discovery & Booking | Tutor Search Request, Tutor Match Result, Demo Class Request, Demo Class Schedule, Tutor Booking, Tutor Session |
| Learning Management | Online Class, Offline Class, Learning Schedule, Attendance Record, Learning Progress |
| Payment Management | Payment Transaction, UPI Payment, Card Payment, Cash Payment, Refund Request |
| Reviews & Ratings | Tutor Review, Tutor Rating, Student Feedback |
| Communication | Notification Log, Message Thread, Chat Message, Reminder Schedule |
| Reports & Analytics | 6 Script Reports |
| Configuration | Tutor Booking Settings |

## Installation

\`\`\`bash
# Get the app
bench get-app tutor_booking_platform https://github.com/your-org/tutor_booking_platform.git

# Install on your ERPNext site
bench --site your-site.local install-app tutor_booking_platform

# Run migrations
bench --site your-site.local migrate

# Restart and clear cache
bench restart
bench --site your-site.local clear-cache
\`\`\`

## License

MIT License — Copyright © 2025 Antigravity