"""Populate the database with a few sample complaints for demo purposes.

Run once after the database exists:
    python seed_data.py
"""
from app import app, db, Complaint

SAMPLES = [
    dict(student_name="Ananya Rao", roll_number="21CS045", hostel_block="Block B",
         room_number="212", category="Internet & WiFi",
         description="No WiFi signal in the room since yesterday evening.",
         priority="Medium"),
    dict(student_name="Karthik Iyer", roll_number="21CS102", hostel_block="Block A",
         room_number="104", category="Plumbing & Water",
         description="Bathroom tap is leaking continuously, water pooling on the floor.",
         priority="High", status="In Progress",
         admin_remarks="Plumber informed, visiting tomorrow morning."),
    dict(student_name="Divya Menon", roll_number="21CS017", hostel_block="Block C",
         room_number="308", category="Electrical",
         description="Ceiling fan makes a loud noise and stops working after a few minutes.",
         priority="Medium", status="Resolved",
         admin_remarks="Fan capacitor replaced. Working fine now."),
    dict(student_name="Rahul Verma", roll_number="21CS063", hostel_block="Block D",
         room_number="415", category="Food & Mess",
         description="Food served at dinner was undercooked twice this week.",
         priority="Low"),
]

with app.app_context():
    db.create_all()
    if Complaint.query.count() == 0:
        for data in SAMPLES:
            db.session.add(Complaint(**data))
        db.session.commit()
        print(f"Added {len(SAMPLES)} sample complaints.")
    else:
        print("Database already has complaints — skipping seed.")
