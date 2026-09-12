# University Hostel Management System (HMS)

A modern, responsive, university-grade Hostel & Residential Life Management System built for **Rajalakshmi Institute of Technology**. Designed with authentic collegiate styling, accessible typography, high data density, full Dark Mode support, and dedicated **Warden** and **Student** portals.

---

## 🏛️ System Features & User Roles

The system is strictly divided into two distinct roles:

### 1. 🛡️ Warden Role (Administrative Command)
- **Executive Command Center:** Real-time occupancy KPIs (342/380 beds &bull; 90%), pending maintenance triage, today's roll call summary, live in-campus visitor count, and overdue dues tracker.
- **Student Management:** Resident directory with search, block/status filters, enrollment modal, and full student dossier.
- **Room & Bed Matrix:** Interactive wing and floor explorer (Block A–D, Floors 1–4) with visual bed slot statuses (`Allotted`, `Vacant`, `Under Maintenance`).
- **Allocations & Transfers:** Bed allocation wizard preventing duplicate assignments, room vacancy synchronization, vacate/clearance desk, and transfer request decision queue.
- **Fees, Invoices & Receipts:** Approved semester rate cards, invoice generator, payment recording modal, late fee application, and print-ready official fee receipts with digital verification stamp.
- **Night Attendance & Outpasses:** Daily night roll call register with 1-click "Mark All Present" action, and outpass application clearance desk (weekend home, medical, night out) with parent verification check.
- **Visitor Gate Desk:** Live in-campus visitors register, 1-click checkout with stay duration tracking, and government ID verification.
- **Maintenance & Complaints:** Ticket triage board, priority flags, technician assignment (electrician, plumber, carpenter), and resolution notes.
- **Notices & Mess Menu:** Official circular publisher with priority tags, and 7-day central dining mess schedule.
- **Reports & Analytics:** Semester fee realization bar chart, maintenance expenditure distribution, and wing-wise attendance audit.
- **Hostel System Settings:** Curfew hours (10:00 PM), grace periods, late fine rates (₹100/day), and emergency contacts.

---

### 2. 🎓 Student Role (Resident Personal Portal)
- **Personal Dashboard:** Allocated room and bed slot (Room B-302, Bed 1), roommate info (Kunal Verma), fee status cleared banner, 96.4% attendance ring, today's mess menu, active repair tickets, and quick action shortcuts.
- **Personal Dossier & Profile:** View/edit personal phone, emergency contacts, local guardian details, blood group, and room allotment history.
- **Maintenance & Repairs:** Submit new issue with category, priority, and photo upload; live 4-stage repair progress timeline.
- **Outpasses & Gate Pass:** Apply for weekend home/night out outpass with parent verification; active approved gate pass with printable QR security pass.
- **Fees & Receipts:** Invoices list, payment history, and instant view/print official university clearance receipt.
- **Attendance & Visitors:** 30-day night roll call log, attendance compliance percentage, and guest gate entry history.
- **Mess Menu & Rules:** Full 7-day dining schedule (breakfast, lunch, tea, dinner) with today highlighted, and hostel code of conduct.
- **Room Transfer Request:** Submit transfer application to preferred block/room type with justification and real-time status tracker.

---

## 🎨 UI & Design Highlights

- **Authentic Collegiate Theme:** Deep navy (`#0f2942`), academic blue (`#1e3a8a`, `#2563eb`), slate steel borders (`#e2e8f0`), and crisp card surfaces. Avoids generic AI gradient blobs in favor of high readability and institutional precision.
- **Theme Engine (Light & Dark Mode):** Instant toggle with `localStorage` memory and smooth CSS transitions.
- **Role Switcher for Evaluation:** Seamless 1-click switcher pill in the top navigation bar to jump between Warden and Student views instantly.
- **Interactive Prototyping:** Connected workflows for allocating beds, recording payments, checking out visitors, approving outpasses, and submitting tickets with animated toast notifications and modals.
- **Printable Receipts & Gate Passes:** Clean CSS print stylesheets for official fee receipts and gate permits.
- **Fully Responsive:** Adapts seamlessly across mobile (collapsible drawer), tablet, and desktop viewports.

---

## 🚀 Running the Application

### 1. Prerequisites
- Python 3.10+ (tested with Python 3.13)
- Virtual environment with Flask, Flask-SQLAlchemy, and Werkzeug

### 2. Launching Locally
```bash
cd hostel_complaint_system
.\.venv\Scripts\python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Demo Credentials
The login screen includes **1-Click Demo Buttons** for both roles, or you can log in manually:

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Warden** | `warden` | `admin123` | Full Administrative Command |
| **Student** | `student` | `student123` | Resident Student Personal Portal |

You can also switch roles at any point from the top header using the **"Switch to Student"** or **"Switch to Warden"** button.
