"""
Hostel Management System (HMS)
Simple, practical, and professional hostel portal.
Two user roles: Warden and Student.
Single hostel block, 3 room types, no bed allocation, no mess.
"""
import os
import re
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "hostel-mgmt-portal-key-2026")

# ---------------------------------------------------------------------------
# Predefined Room Types (Exactly 3)
# ---------------------------------------------------------------------------
ROOM_TYPES = [
    "AC — Three Sharing",
    "Non-AC — Three Sharing",
    "Non-AC — Four Sharing",
]

# ---------------------------------------------------------------------------
# In-Memory Realistic Data Store
# ---------------------------------------------------------------------------
STUDENTS_DATA = [
    {
        "id": 1,
        "name": "Aarav Sharma",
        "student_id": "2024CS101",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43210",
        "room_number": "201",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 96.0,
    },
    {
        "id": 2,
        "name": "Kunal Verma",
        "student_id": "2024ME102",
        "dept": "Mechanical Engineering",
        "year": 3,
        "phone": "98765 43211",
        "room_number": "201",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 92.0,
    },
    {
        "id": 3,
        "name": "Devansh Joshi",
        "student_id": "2024CS103",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43212",
        "room_number": "201",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 94.0,
    },
    {
        "id": 4,
        "name": "Rohan Deshmukh",
        "student_id": "2023CS104",
        "dept": "Computer Science & Engineering",
        "year": 4,
        "phone": "98765 43213",
        "room_number": "202",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 95.0,
    },
    {
        "id": 5,
        "name": "Aditya Nair",
        "student_id": "2025EE105",
        "dept": "Electrical Engineering",
        "year": 2,
        "phone": "98765 43214",
        "room_number": "202",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 89.0,
    },
    {
        "id": 6,
        "name": "Mohd. Farhan",
        "student_id": "2025EE106",
        "dept": "Electrical Engineering",
        "year": 2,
        "phone": "98765 43215",
        "room_number": "202",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 91.0,
    },
    {
        "id": 7,
        "name": "Tanmay Joshi",
        "student_id": "2025ME107",
        "dept": "Mechanical Engineering",
        "year": 2,
        "phone": "98765 43216",
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "attendance_pct": 93.0,
    },
    {
        "id": 8,
        "name": "Ritik Saxena",
        "student_id": "2024CS108",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43217",
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "attendance_pct": 88.0,
    },
    {
        "id": 9,
        "name": "Siddharth Roy",
        "student_id": "2025CV109",
        "dept": "Civil Engineering",
        "year": 2,
        "phone": "98765 43218",
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "attendance_pct": 90.0,
    },
    {
        "id": 10,
        "name": "Vikram Sen",
        "student_id": "2026EC110",
        "dept": "Electronics & Communication",
        "year": 1,
        "phone": "98765 43219",
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "attendance_pct": 97.0,
    },
    {
        "id": 11,
        "name": "Kavya Menon",
        "student_id": "2024CS111",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43220",
        "room_number": "301",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 98.0,
    },
    {
        "id": 12,
        "name": "Pooja",
        "student_id": "2024EC112",
        "dept": "Electronics & Communication",
        "year": 4,
        "phone": "98765 43221",
        "room_number": "301",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 92.0,
    },
    {
        "id": 13,
        "name": "Sneha Rao",
        "student_id": "2024CS113",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43222",
        "room_number": "301",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 94.0,
    },
    {
        "id": 14,
        "name": "Ananya Iyer",
        "student_id": "2026IT114",
        "dept": "Information Technology",
        "year": 1,
        "phone": "98765 43223",
        "room_number": "203",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 96.0,
    },
    {
        "id": 15,
        "name": "Karthik Subramanian",
        "student_id": "2023ME115",
        "dept": "Mechanical Engineering",
        "year": 4,
        "phone": "98765 43224",
        "room_number": "203",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 93.0,
    },
]

ROOMS_DATA = [
    {
        "room_number": "201",
        "room_type": "AC — Three Sharing",
        "capacity": 3,
        "students": [
            {"name": "Aarav Sharma", "student_id": "2024CS101", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43210"},
            {"name": "Kunal Verma", "student_id": "2024ME102", "dept": "Mechanical Engineering", "year": 3, "phone": "98765 43211"},
            {"name": "Devansh Joshi", "student_id": "2024CS103", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43212"},
        ]
    },
    {
        "room_number": "301",
        "room_type": "AC — Three Sharing",
        "capacity": 3,
        "students": [
            {"name": "Kavya Menon", "student_id": "2024CS111", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43220"},
            {"name": "Pooja", "student_id": "2024EC112", "dept": "Electronics & Communication", "year": 4, "phone": "98765 43221"},
            {"name": "Sneha Rao", "student_id": "2024CS113", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43222"},
        ]
    },
    {
        "room_number": "202",
        "room_type": "Non-AC — Three Sharing",
        "capacity": 3,
        "students": [
            {"name": "Rohan Deshmukh", "student_id": "2023CS104", "dept": "Computer Science & Engineering", "year": 4, "phone": "98765 43213"},
            {"name": "Aditya Nair", "student_id": "2025EE105", "dept": "Electrical Engineering", "year": 2, "phone": "98765 43214"},
            {"name": "Mohd. Farhan", "student_id": "2025EE106", "dept": "Electrical Engineering", "year": 2, "phone": "98765 43215"},
        ]
    },
    {
        "room_number": "203",
        "room_type": "Non-AC — Three Sharing",
        "capacity": 3,
        "students": [
            {"name": "Ananya Iyer", "student_id": "2026IT114", "dept": "Information Technology", "year": 1, "phone": "98765 43223"},
            {"name": "Karthik Subramanian", "student_id": "2023ME115", "dept": "Mechanical Engineering", "year": 4, "phone": "98765 43224"},
        ]
    },
    {
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "capacity": 4,
        "students": [
            {"name": "Tanmay Joshi", "student_id": "2025ME107", "dept": "Mechanical Engineering", "year": 2, "phone": "98765 43216"},
            {"name": "Ritik Saxena", "student_id": "2024CS108", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43217"},
            {"name": "Siddharth Roy", "student_id": "2025CV109", "dept": "Civil Engineering", "year": 2, "phone": "98765 43218"},
            {"name": "Vikram Sen", "student_id": "2026EC110", "dept": "Electronics & Communication", "year": 1, "phone": "98765 43219"},
        ]
    },
    {
        "room_number": "102",
        "room_type": "Non-AC — Four Sharing",
        "capacity": 4,
        "students": []
    },
]

LEAVE_REQUESTS_DATA = [
    {
        "id": 1,
        "student_id": "2024CS101",
        "student_name": "Aarav Sharma",
        "room_number": "201",
        "leave_type": "Home Visit",
        "start_date": "14-Sep-2026",
        "end_date": "17-Sep-2026",
        "reason": "Family function at hometown.",
        "status": "Pending",
        "applied_on": "11-Sep-2026",
    },
    {
        "id": 2,
        "student_id": "2024EC112",
        "student_name": "Pooja",
        "room_number": "301",
        "leave_type": "Medical Leave",
        "start_date": "12-Sep-2026",
        "end_date": "15-Sep-2026",
        "reason": "Doctor appointment and dental procedure.",
        "status": "Pending",
        "applied_on": "10-Sep-2026",
    },
    {
        "id": 3,
        "student_id": "2025ME107",
        "student_name": "Tanmay Joshi",
        "room_number": "101",
        "leave_type": "Academic",
        "start_date": "05-Sep-2026",
        "end_date": "07-Sep-2026",
        "reason": "Attending inter-college technical symposium.",
        "status": "Approved",
        "applied_on": "01-Sep-2026",
    },
    {
        "id": 4,
        "student_id": "2024CS101",
        "student_name": "Aarav Sharma",
        "room_number": "201",
        "leave_type": "Home Visit",
        "start_date": "20-Aug-2026",
        "end_date": "22-Aug-2026",
        "reason": "Sibling engagement ceremony.",
        "status": "Approved",
        "applied_on": "16-Aug-2026",
    },
    {
        "id": 5,
        "student_id": "2025EE106",
        "student_name": "Mohd. Farhan",
        "room_number": "202",
        "leave_type": "Personal",
        "start_date": "15-Aug-2026",
        "end_date": "16-Aug-2026",
        "reason": "Visiting local guardian.",
        "status": "Rejected",
        "applied_on": "14-Aug-2026",
    },
]

COMPLAINTS_DATA = [
    {
        "id": 1,
        "student_id": "2024CS101",
        "student_name": "Aarav Sharma",
        "room_number": "201",
        "category": "Electrical",
        "description": "Ceiling fan regulator sparking and not working at speeds 3 and 4.",
        "status": "In Progress",
        "created_on": "10-Sep-2026",
    },
    {
        "id": 2,
        "student_id": "2024CS111",
        "student_name": "Kavya Menon",
        "room_number": "301",
        "category": "Plumbing",
        "description": "Bathroom tap valve loose and leaking continuously.",
        "status": "Submitted",
        "created_on": "11-Sep-2026",
    },
    {
        "id": 3,
        "student_id": "2025ME107",
        "student_name": "Tanmay Joshi",
        "room_number": "101",
        "category": "Cleaning",
        "description": "Room corridor trash bin overflowing.",
        "status": "Submitted",
        "created_on": "11-Sep-2026",
    },
    {
        "id": 4,
        "student_id": "2024CS101",
        "student_name": "Aarav Sharma",
        "room_number": "201",
        "category": "Furniture",
        "description": "Study chair right armrest screw loose.",
        "status": "Resolved",
        "created_on": "28-Aug-2026",
    },
    {
        "id": 5,
        "student_id": "2023CS104",
        "student_name": "Rohan Deshmukh",
        "room_number": "202",
        "category": "Room",
        "description": "Window latch not locking properly on windy nights.",
        "status": "Resolved",
        "created_on": "25-Aug-2026",
    },
]

ANNOUNCEMENTS_DATA = [
    {
        "id": 1,
        "title": "Water Tank Cleaning Tomorrow Morning",
        "description": "Routine overhead water tank cleaning will be conducted tomorrow between 10:00 AM and 1:00 PM. Please store adequate water beforehand.",
        "date": "11-Sep-2026",
        "is_important": True,
    },
    {
        "id": 2,
        "title": "Curfew and Night Roll Call Reminder",
        "description": "Hostel main gates close at 10:00 PM on weekdays. Students returning after 10:00 PM must carry an approved outpass or sign the late entry register.",
        "date": "08-Sep-2026",
        "is_important": True,
    },
    {
        "id": 3,
        "title": "Wi-Fi Access Point Upgrade Notice",
        "description": "Network access points on the 2nd floor will be rebooted on Saturday evening for firmware updates. Minor connectivity interruptions may occur.",
        "date": "04-Sep-2026",
        "is_important": False,
    },
]

# Daily Attendance Data by Date
ATTENDANCE_DB = {
    "2026-09-11": {
        "2024CS101": "Present",
        "2024ME102": "Present",
        "2024CS103": "Present",
        "2023CS104": "Present",
        "2025EE105": "Present",
        "2025EE106": "Absent",
        "2025ME107": "Present",
        "2024CS108": "Present",
        "2025CV109": "Present",
        "2026EC110": "Present",
        "2024CS111": "Present",
        "2024EC112": "Absent",
        "2024CS113": "Present",
    },
    "2026-09-10": {
        "2024CS101": "Present",
        "2024ME102": "Present",
        "2024CS103": "Present",
        "2023CS104": "Present",
        "2025EE105": "Present",
        "2025EE106": "Present",
        "2025ME107": "Present",
        "2024CS108": "Absent",
        "2025CV109": "Present",
        "2026EC110": "Present",
        "2024CS111": "Present",
        "2024EC112": "Present",
        "2024CS113": "Present",
    }
}

# ---------------------------------------------------------------------------
# Role Credentials & Access Configuration
# ---------------------------------------------------------------------------
WARDEN_CREDENTIALS = {
    "warden": "admin123",
    "admin": "admin123",
    "warden@rit.edu": "admin123",
}

STUDENT_DEFAULT_PASSWORD = "student123"

def get_current_student():
    """Retrieve currently authenticated student or default to Aarav Sharma."""
    student_id = session.get("student_id", "2024CS101")
    return next((s for s in STUDENTS_DATA if s["student_id"].upper() == student_id.upper()), STUDENTS_DATA[0])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_role" not in session:
            flash("Please sign in to access the hostel portal.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def warden_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_role" not in session:
            flash("Please sign in to access the Warden portal.", "warning")
            return redirect(url_for("login"))
        if session.get("user_role") != "warden":
            flash("Access restricted. Warden credentials required.", "warning")
            return redirect(url_for("student_dashboard"))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_role" not in session:
            flash("Please sign in to access the Student portal.", "warning")
            return redirect(url_for("login"))
        if session.get("user_role") != "student":
            session["user_role"] = "student"
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------------------------------------------------------
# Role-Specific Chatbot Knowledge Bases
# ---------------------------------------------------------------------------
STUDENT_CHATBOT_FAQS = [
    {
        "keywords": ["my room", "room number", "where do i stay", "who is my roommate", "roommate", "room allocation", "bed"],
        "answer": "You are currently allocated to Room 201 (AC — Three Sharing) on Floor 2. Your registered roommates are Kunal Verma (Mechanical) and Devansh Joshi (Computer Science). For room change requests, contact the Warden's office during counseling hours."
    },
    {
        "keywords": ["room type", "room types", "sharing", "ac", "non ac", "capacity", "rooms"],
        "answer": "The hostel has exactly 3 room types: (1) AC — Three Sharing, (2) Non-AC — Three Sharing, and (3) Non-AC — Four Sharing. All rooms come with study desks, personal wardrobes, ceiling fans, and high-speed Wi-Fi."
    },
    {
        "keywords": ["leave", "apply for leave", "gate pass", "outstation", "home visit", "permission", "vacation", "pass", "outpass"],
        "answer": "To apply for leave or an outstation gate pass: Navigate to the 'Leave' tab in the left menu, click 'Apply for Leave', select your category (Home Visit, Medical, Academic, or Personal), select start & end dates, and state your reason. Your request will be submitted for Warden review. You can track approval status in real-time."
    },
    {
        "keywords": ["complaint", "repair", "electrical", "plumbing", "issue", "broken", "fan", "tap", "light", "cleaning", "maintenance", "furniture"],
        "answer": "To report a maintenance issue: Go to the 'Complaints' tab and click 'New Complaint'. Select the issue category (Electrical, Plumbing, Room, Cleaning, Furniture, or Other), describe the problem clearly, and submit. Campus technicians attend to tickets daily between 9:00 AM and 5:00 PM."
    },
    {
        "keywords": ["attendance", "roll call", "mark attendance", "daily attendance", "night roll call", "present", "absent"],
        "answer": "Hostel roll call is conducted daily in your room at 5:30 PM by the hostel warden and caretaker. Please ensure you are inside your room during verification. You can review your personal attendance logs under the 'Attendance' tab."
    },
    {
        "keywords": ["curfew", "timing", "gate close", "time", "late entry", "night rule", "gate timings", "in time"],
        "answer": "Hostel gates close strictly at 10:00 PM on weekdays and 10:30 PM on weekends. Returning after curfew without an approved Warden leave pass requires signing the security late register and triggers a notification to your local guardian."
    },
    {
        "keywords": ["contact", "warden number", "help", "phone", "emergency", "ambulance", "security", "doctor", "helpline"],
        "answer": "Resident emergency helplines:\n• Chief Warden: +91 98450 11223 (Ext. 4041)\n• Hostel Caretaker Desk: Ext. 4042\n• Campus Health Center & Ambulance: Ext. 108\n• Main Gate Security Control: Ext. 101."
    },
    {
        "keywords": ["announcement", "notices", "circular", "notice board", "news", "updates"],
        "answer": "Official college and hostel circulars are published under the 'Announcements' tab. Critical updates such as water tank cleaning, power maintenance, or holiday schedules are highlighted with an 'Important' badge."
    },
    {
        "keywords": ["wifi", "wi-fi", "internet", "network", "router"],
        "answer": "Hostel Wi-Fi is available 24/7. Connect to 'RIT-Hostel-WiFi' using your student roll number and campus network credentials. For connectivity issues, file an IT ticket under Complaints."
    },
    {
        "keywords": ["mess", "food", "dining", "canteen", "lunch", "dinner", "breakfast"],
        "answer": "Dining facilities are managed centrally at the college food court. Breakfast: 7:30 - 9:00 AM | Lunch: 12:30 - 2:00 PM | Dinner: 7:30 - 9:15 PM."
    }
]

WARDEN_CHATBOT_FAQS = [
    {
        "keywords": ["leave", "leave request", "approve", "reject", "pending leaves", "gate pass", "permission", "review leave", "outpass"],
        "answer": "As Warden, you can manage resident leave applications from the 'Leave Requests' section. You can filter by Pending, Approved, or Rejected status, verify student department and parental consent, and click 'Approve' or 'Reject' with administrative remarks."
    },
    {
        "keywords": ["room", "rooms", "capacity", "vacancy", "vacancies", "occupancy", "room type", "sharing", "allotment", "allocation"],
        "answer": "The hostel block comprises 54 total rooms with an overall capacity of 180 students across 3 room types: (1) AC — Three Sharing (18 rooms), (2) Non-AC — Three Sharing (18 rooms), and (3) Non-AC — Four Sharing (18 rooms). Overall occupancy is 96.6% (174 residents, 6 vacancies). Check the 'Rooms' tab to view floor-wise occupancy bars and assign incoming students."
    },
    {
        "keywords": ["attendance", "roll call", "mark attendance", "absent", "present", "daily attendance", "evening roll call", "absentees"],
        "answer": "Evening roll call is scheduled daily at 5:30 PM. In the 'Attendance' section, select today's date to mark individual students as Present or Absent room-by-room, or use the 'Mark All Present' tool for bulk recording. Unaccounted absentees should be flagged for immediate guardian contact."
    },
    {
        "keywords": ["complaint", "complaints", "maintenance", "repair", "electrical", "plumbing", "contractor", "technician", "ticket"],
        "answer": "You have oversight of all hostel maintenance tickets in the 'Complaints' dashboard. Requests are categorized by Electrical, Plumbing, Cleaning, and Furniture. You can update statuses to 'In Progress' or 'Resolved' and coordinate with campus facility contractors."
    },
    {
        "keywords": ["announcement", "announcements", "notice", "publish", "broadcast", "circular", "post"],
        "answer": "To broadcast notices to all residents: Go to 'Announcements' and click 'New Announcement'. Enter the circular title, message details, and toggle 'Mark as Important' if it requires immediate attention. Published announcements instantly appear on all student dashboards."
    },
    {
        "keywords": ["curfew", "timing", "gate close", "late entry", "security", "main gate", "rule", "gate timings"],
        "answer": "Hostel curfew is enforced at 10:00 PM (Weekdays) and 10:30 PM (Weekends). Main Gate Security maintains the physical late-entry log. In the morning, you can cross-reference late entries with approved leave passes and issue disciplinary warnings for unauthorized delays."
    },
    {
        "keywords": ["contact", "emergency", "security", "police", "hospital", "management", "estate", "director", "helpline"],
        "answer": "Administrative & Emergency Directory:\n• Campus Security Control Room: Ext. 101 (Mobile: +91 94440 98765)\n• Estate & Maintenance Supervisor: Ext. 205\n• Campus Health Center: Ext. 108\n• Director / Principal's Office: Ext. 5001\n• Local Police Station: 100 / 044-26810200."
    },
    {
        "keywords": ["student", "students", "resident", "directory", "year", "department", "search", "registry"],
        "answer": "The 'Students' registry lists all 174 residents. You can search by student name or roll number, and filter by study year (1st, 2nd, 3rd, or 4th Year) or department to view allocated room numbers and guardian contact info."
    },
    {
        "keywords": ["discipline", "fine", "ragging", "prohibited", "alcohol", "smoking", "violation", "penalty"],
        "answer": "The institution enforces a strict zero-tolerance anti-ragging and substance-free code of conduct. Log disciplinary incidents in the student record and escalate to the Hostel Disciplinary Board."
    }
]

# Backward compatibility alias
CHATBOT_FAQS = STUDENT_CHATBOT_FAQS

def get_chatbot_reply(user_query, role="student"):
    query_lower = user_query.lower()
    faqs = WARDEN_CHATBOT_FAQS if role == "warden" else STUDENT_CHATBOT_FAQS

    # Check multi-word phrase matches first (e.g. "my room", "room type", "gate pass")
    for item in faqs:
        for kw in item["keywords"]:
            if " " in kw and kw in query_lower:
                return item["answer"]

    # Check whole-word boundary matches for single words (e.g. "leave", "contact", "rooms", "curfew")
    for item in faqs:
        for kw in item["keywords"]:
            if " " not in kw and re.search(r'\b' + re.escape(kw) + r'\b', query_lower):
                return item["answer"]

    if role == "warden":
        return (
            "As Hostel Warden, I can assist you with managing student leave approvals, room capacity & vacancies, "
            "roll call attendance monitoring, maintenance complaints, resident registry, and publishing announcements. "
            "Try asking: 'What is the room vacancy status?' or 'How do I review pending leave requests?'"
        )
    else:
        return (
            "As a resident student, I can assist you with your room details, hostel room types, applying for leave passes, "
            "submitting maintenance complaints, roll call timing, and campus emergency contacts. "
            "Try asking: 'How do I apply for leave?' or 'Where do I stay and what is my room number?'"
        )

# ---------------------------------------------------------------------------
# Role & Context Middleware
# ---------------------------------------------------------------------------
@app.context_processor
def inject_globals():
    role = session.get("user_role", "warden")
    if role == "warden":
        user_name = "Dr. K. S. Venkatesh (Warden)"
    else:
        student = get_current_student()
        user_name = student["name"]
    pending_leaves_count = sum(1 for l in LEAVE_REQUESTS_DATA if l["status"] == "Pending")
    pending_complaints_count = sum(1 for c in COMPLAINTS_DATA if c["status"] in ["Submitted", "In Progress"])
    return {
        "current_role": role,
        "current_user_name": user_name,
        "pending_leaves_count": pending_leaves_count,
        "pending_complaints_count": pending_complaints_count,
        "today_str": datetime.now().strftime("%d-%b-%Y"),
    }

# ---------------------------------------------------------------------------
# General Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    if "user_role" not in session:
        return redirect(url_for("login"))
    if session["user_role"] == "warden":
        return redirect(url_for("warden_dashboard"))
    return redirect(url_for("student_dashboard"))

@app.route("/switch-role/<role>")
def switch_role(role):
    if role in ["warden", "student"]:
        session["user_role"] = role
        if role == "warden":
            session["user_name"] = "Dr. K. S. Venkatesh (Warden)"
            session["user_id"] = "warden"
            flash("Switched view to Warden portal.", "info")
            return redirect(url_for("warden_dashboard"))
        else:
            student = get_current_student()
            session["user_name"] = student["name"]
            session["user_id"] = student["student_id"]
            session["student_id"] = student["student_id"]
            flash(f"Switched view to Student portal ({student['name']}).", "info")
            return redirect(url_for("student_dashboard"))
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if role == "warden":
            u_low = username.lower()
            if (u_low in WARDEN_CREDENTIALS and WARDEN_CREDENTIALS[u_low] == password) or (u_low in ["warden", "admin"] and password in ["admin123", "warden123"]):
                session["user_role"] = "warden"
                session["user_id"] = "warden"
                session["user_name"] = "Dr. K. S. Venkatesh (Warden)"
                flash("Signed in successfully as Warden.", "success")
                return redirect(url_for("warden_dashboard"))
            else:
                flash("Invalid Warden credentials. Username or password incorrect.", "danger")
                return render_template("auth/login.html", selected_role="warden", username=username)

        elif role == "student":
            u_low = username.lower()
            matched_student = None
            if u_low in ["student", "aarav"]:
                matched_student = STUDENTS_DATA[0]
            else:
                matched_student = next((s for s in STUDENTS_DATA if s["student_id"].lower() == u_low), None)

            if matched_student and (password in [STUDENT_DEFAULT_PASSWORD, matched_student["student_id"], "student"]):
                session["user_role"] = "student"
                session["student_id"] = matched_student["student_id"]
                session["user_name"] = matched_student["name"]
                session["user_id"] = matched_student["student_id"]
                flash(f"Signed in successfully as {matched_student['name']} ({matched_student['student_id']}).", "success")
                return redirect(url_for("student_dashboard"))
            else:
                flash("Invalid Student credentials. Roll Number or password incorrect.", "danger")
                return render_template("auth/login.html", selected_role="student", username=username)

        else:
            flash("Please select a valid portal role (Warden or Student).", "danger")
            return render_template("auth/login.html")

    selected_role = request.args.get("role", "student")
    return render_template("auth/login.html", selected_role=selected_role)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("login"))

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        flash("Password reset instructions sent to your registered email address.", "info")
        return redirect(url_for("login"))
    return render_template("auth/forgot_password.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True, silent=True) or {}
    message = data.get("message", "").strip()
    role = data.get("role") or session.get("user_role", "student")
    if not message:
        return jsonify({"reply": "Please enter a question to get assistance."})
    reply = get_chatbot_reply(message, role=role)
    return jsonify({"reply": reply, "role": role})

# ---------------------------------------------------------------------------
# Student Portal Routes
# ---------------------------------------------------------------------------
@app.route("/student/dashboard")
@student_required
def student_dashboard():
    student = get_current_student()
    my_leaves = [l for l in LEAVE_REQUESTS_DATA if l["student_id"] == student["student_id"]]
    my_complaints = [c for c in COMPLAINTS_DATA if c["student_id"] == student["student_id"]]
    latest_leave = my_leaves[0] if my_leaves else None
    latest_complaint = my_complaints[0] if my_complaints else None
    latest_announcements = ANNOUNCEMENTS_DATA[:2]

    return render_template(
        "student/dashboard.html",
        student=student,
        latest_leave=latest_leave,
        latest_complaint=latest_complaint,
        announcements=latest_announcements,
        active_page="student_dashboard"
    )

@app.route("/student/my-room")
@student_required
def student_my_room():
    student = get_current_student()
    room = next((r for r in ROOMS_DATA if r["room_number"] == student["room_number"]), None)
    roommates = room["students"] if room else []

    return render_template(
        "student/my_room.html",
        student=student,
        room=room,
        roommates=roommates,
        active_page="student_my_room"
    )

@app.route("/student/attendance")
@student_required
def student_attendance():
    student = get_current_student()
    history = []
    for d, recs in ATTENDANCE_DB.items():
        status = recs.get(student["student_id"], "Present")
        history.append({"date": d, "status": status})
    
    history.append({"date": "2026-09-09", "status": "Present"})
    history.append({"date": "2026-09-08", "status": "Present"})
    history.append({"date": "2026-09-07", "status": "Present"})
    history.append({"date": "2026-09-06", "status": "Present"})
    history.append({"date": "2026-09-05", "status": "Present"})

    return render_template(
        "student/attendance.html",
        student=student,
        history=history,
        active_page="student_attendance"
    )

@app.route("/student/leave", methods=["GET", "POST"])
@student_required
def student_leave():
    student = get_current_student()
    if request.method == "POST":
        leave_type = request.form.get("leave_type", "Home Visit")
        start_date = request.form.get("start_date", "")
        end_date = request.form.get("end_date", "")
        reason = request.form.get("reason", "").strip()

        new_leave = {
            "id": len(LEAVE_REQUESTS_DATA) + 1,
            "student_id": student["student_id"],
            "student_name": student["name"],
            "room_number": student["room_number"],
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "reason": reason,
            "status": "Pending",
            "applied_on": datetime.now().strftime("%d-%b-%Y"),
        }
        LEAVE_REQUESTS_DATA.insert(0, new_leave)
        flash("Leave request submitted successfully. Warden will review it.", "success")
        return redirect(url_for("student_leave"))

    my_leaves = [l for l in LEAVE_REQUESTS_DATA if l["student_id"] == student["student_id"]]
    return render_template(
        "student/leave.html",
        student=student,
        leaves=my_leaves,
        active_page="student_leave"
    )

@app.route("/student/complaints", methods=["GET", "POST"])
@student_required
def student_complaints():
    student = get_current_student()
    if request.method == "POST":
        category = request.form.get("category", "Other")
        description = request.form.get("description", "").strip()

        new_complaint = {
            "id": len(COMPLAINTS_DATA) + 1,
            "student_id": student["student_id"],
            "student_name": student["name"],
            "room_number": student["room_number"],
            "category": category,
            "description": description,
            "status": "Submitted",
            "created_on": datetime.now().strftime("%d-%b-%Y"),
        }
        COMPLAINTS_DATA.insert(0, new_complaint)
        flash("Complaint submitted. Maintenance staff will look into it.", "success")
        return redirect(url_for("student_complaints"))

    my_complaints = [c for c in COMPLAINTS_DATA if c["student_id"] == student["student_id"]]
    return render_template(
        "student/complaints.html",
        student=student,
        complaints=my_complaints,
        active_page="student_complaints"
    )

@app.route("/student/announcements")
@student_required
def student_announcements():
    return render_template(
        "student/announcements.html",
        announcements=ANNOUNCEMENTS_DATA,
        active_page="student_announcements"
    )

@app.route("/student/chatbot")
@student_required
def student_chatbot():
    student = get_current_student()
    return render_template(
        "student/chatbot.html",
        student=student,
        faqs=STUDENT_CHATBOT_FAQS,
        active_page="student_chatbot"
    )

@app.route("/student/profile")
@student_required
def student_profile():
    student = get_current_student()
    return render_template(
        "student/profile.html",
        student=student,
        active_page="student_profile"
    )

# ---------------------------------------------------------------------------
# Warden Portal Routes
# ---------------------------------------------------------------------------
@app.route("/warden/dashboard")
@warden_required
def warden_dashboard():
    total_students = 174
    total_rooms = 54
    
    # Dashboard attendance summary
    present_today = 170
    absent_today = 4

    pending_leaves = [l for l in LEAVE_REQUESTS_DATA if l["status"] == "Pending"]
    pending_complaints = [c for c in COMPLAINTS_DATA if c["status"] in ["Submitted", "In Progress"]]

    return render_template(
        "warden/dashboard.html",
        total_students=total_students,
        total_rooms=total_rooms,
        present_today=present_today,
        absent_today=absent_today,
        pending_leaves=pending_leaves,
        pending_complaints=pending_complaints,
        announcements=ANNOUNCEMENTS_DATA[:2],
        active_page="warden_dashboard"
    )

@app.route("/warden/students")
@warden_required
def warden_students():
    search_q = request.args.get("q", "").strip().lower()
    room_filter = request.args.get("room_type", "all")
    year_filter = request.args.get("year", "all")

    filtered = STUDENTS_DATA
    if search_q:
        filtered = [
            s for s in filtered
            if search_q in s["name"].lower() or search_q in s["student_id"].lower() or search_q in s["room_number"].lower()
        ]
    if room_filter != "all":
        filtered = [s for s in filtered if s["room_type"] == room_filter]
    if year_filter != "all":
        try:
            y = int(year_filter)
            filtered = [s for s in filtered if s.get("year") == y]
        except ValueError:
            pass

    return render_template(
        "warden/students.html",
        students=filtered,
        room_types=ROOM_TYPES,
        search_q=search_q,
        selected_room_type=room_filter,
        selected_year=year_filter,
        active_page="warden_students"
    )

@app.route("/warden/rooms")
@warden_required
def warden_rooms():
    # Group rooms by room type
    grouped = {t: [] for t in ROOM_TYPES}
    for r in ROOMS_DATA:
        if r["room_type"] in grouped:
            grouped[r["room_type"]].append(r)
        else:
            grouped[r["room_type"]] = [r]

    selected_room_no = request.args.get("room", "")
    selected_room = None
    if selected_room_no:
        selected_room = next((r for r in ROOMS_DATA if r["room_number"] == selected_room_no), None)

    return render_template(
        "warden/rooms.html",
        grouped_rooms=grouped,
        all_rooms=ROOMS_DATA,
        selected_room=selected_room,
        active_page="warden_rooms"
    )

@app.route("/warden/attendance", methods=["GET", "POST"])
@warden_required
def warden_attendance():
    selected_date = request.args.get("date", "2026-09-11")

    if request.method == "POST":
        action_date = request.form.get("attendance_date", "2026-09-11")
        if action_date not in ATTENDANCE_DB:
            ATTENDANCE_DB[action_date] = {}

        for s in STUDENTS_DATA:
            status_val = request.form.get(f"status_{s['student_id']}", "Present")
            ATTENDANCE_DB[action_date][s["student_id"]] = status_val

        flash(f"Attendance for {action_date} saved successfully.", "success")
        return redirect(url_for("warden_attendance", date=action_date))

    # Retrieve status for selected date
    day_records = ATTENDANCE_DB.get(selected_date, {})
    students_with_status = []
    for s in STUDENTS_DATA:
        st = day_records.get(s["student_id"], "Present")
        students_with_status.append({**s, "current_status": st})

    return render_template(
        "warden/attendance.html",
        selected_date=selected_date,
        available_dates=list(ATTENDANCE_DB.keys()),
        students=students_with_status,
        active_page="warden_attendance"
    )

@app.route("/warden/leaves")
@warden_required
def warden_leaves():
    filter_status = request.args.get("status", "all")
    if filter_status == "all":
        leaves = LEAVE_REQUESTS_DATA
    else:
        leaves = [l for l in LEAVE_REQUESTS_DATA if l["status"].lower() == filter_status.lower()]

    return render_template(
        "warden/leaves.html",
        leaves=leaves,
        selected_status=filter_status,
        active_page="warden_leaves"
    )

@app.route("/warden/leave/<int:leave_id>/<action>", methods=["POST"])
@warden_required
def warden_action_leave(leave_id, action):
    leave = next((l for l in LEAVE_REQUESTS_DATA if l["id"] == leave_id), None)
    if leave:
        if action == "approve":
            leave["status"] = "Approved"
            flash(f"Leave request #{leave_id} for {leave['student_name']} has been Approved.", "success")
        elif action == "reject":
            leave["status"] = "Rejected"
            flash(f"Leave request #{leave_id} for {leave['student_name']} has been Rejected.", "info")
    return redirect(url_for("warden_leaves"))

@app.route("/warden/complaints")
@warden_required
def warden_complaints():
    filter_status = request.args.get("status", "all")
    if filter_status == "all":
        complaints = COMPLAINTS_DATA
    else:
        complaints = [c for c in COMPLAINTS_DATA if c["status"].lower() == filter_status.lower()]

    return render_template(
        "warden/complaints.html",
        complaints=complaints,
        selected_status=filter_status,
        active_page="warden_complaints"
    )

@app.route("/warden/complaint/<int:complaint_id>/status", methods=["POST"])
@warden_required
def warden_update_complaint(complaint_id):
    new_status = request.form.get("status", "Submitted")
    comp = next((c for c in COMPLAINTS_DATA if c["id"] == complaint_id), None)
    if comp:
        comp["status"] = new_status
        flash(f"Complaint #{complaint_id} status updated to '{new_status}'.", "success")
    return redirect(url_for("warden_complaints"))

@app.route("/warden/announcements", methods=["GET", "POST"])
@warden_required
def warden_announcements():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        is_important = bool(request.form.get("is_important"))

        new_ann = {
            "id": len(ANNOUNCEMENTS_DATA) + 1,
            "title": title,
            "description": description,
            "date": datetime.now().strftime("%d-%b-%Y"),
            "is_important": is_important,
        }
        ANNOUNCEMENTS_DATA.insert(0, new_ann)
        flash("Hostel announcement published.", "success")
        return redirect(url_for("warden_announcements"))

    return render_template(
        "warden/announcements.html",
        announcements=ANNOUNCEMENTS_DATA,
        active_page="warden_announcements"
    )

@app.route("/warden/chatbot")
@warden_required
def warden_chatbot():
    return render_template(
        "warden/chatbot.html",
        faqs=WARDEN_CHATBOT_FAQS,
        active_page="warden_chatbot"
    )

@app.route("/warden/profile")
@warden_required
def warden_profile():
    return render_template(
        "warden/profile.html",
        active_page="warden_profile"
    )

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)

