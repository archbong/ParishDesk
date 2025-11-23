# **ParishKeeper — MVP Documentation**

**ParishKeeper** is a modular, multi-church administration platform designed for the Anglican Diocese of Ogoni and adaptable for any Christian organization.
It helps missionaries, clergy, and church workers manage Sunday teachings, attendance, financial records, events, prayer requests, welfare cases, and more — all in one place.

This MVP version lays the foundation for future diocesan-wide deployment and internship participation.

---

## **📌 Purpose of the Project**

As a missionary/evangelist who is present in the parish mainly on Sundays, this application enables consistent, structured pastoral work throughout the week. It ensures:

* Proper documentation of teachings
* Accurate attendance tracking
* Organized events/programs
* Centralized announcements
* Secure financial record-keeping (tithes, offerings, welfare, building)
* Tracking of church assets
* Managing prayer needs
* Handling welfare support cases
* Engaging members via contacts & messaging
* Supporting interns who contribute to the platform

---

## **📦 MVP Scope**

The MVP focuses on the following modules:

### **1. Core Module**

* Churches (multi-church support)
* User profiles & role management (Admins, Clergy, Treasurer, Volunteer, Intern)
* Authentication (JWT)
* Permissions system

### **2. Teachings**

* Document weekly Sunday messages
* Scripture references
* Attach audio, notes, outlines, and resources

### **3. Attendance**

* Create services/events
* Record attendance (adult, children, visitors)
* Weekly & monthly summaries

### **4. Contacts & Messaging**

* Manage member records
* Import contact lists
* Send messages via email/SMS (future)

### **5. Accounts (Financials)**

* Track tithes, offerings, welfare giving, building fund
* Manage accounts
* Generate simple income reports

### **6. Events & Announcements**

* Church programs & event scheduling
* Publish announcements
* Display upcoming programs

### **7. Prayer Requests**

* Submit requests
* Assign follow-up
* Track answered/ongoing prayers

### **8. Welfare**

* Track individuals needing support
* Log follow-ups and assistance

### **9. Assets**

* Track church properties (land, equipment, instruments, etc.)

### **10. Internships**

* Application intake for contributors
* Assign roles and tasks

---

## **🧱 Architecture Overview**

### **Tech Stack**

* **Backend:** Django 4+
* **API:** Django REST Framework
* **Auth:** JWT (SimpleJWT)
* **Database:** PostgreSQL
* **Cache & Queue:** Redis + Celery
* **Storage:** AWS S3 or DigitalOcean Spaces
* **Search:** PostgreSQL full-text (MVP)

### **Design Approach**

* Modular Django apps per domain
* Service layer for business logic
* Multi-tenant via `Church` foreign key
* Role-based access control using Django Groups & custom permissions
* Background tasks for exports + messaging
* Processing-heavy features use Celery

---

## **📂 Project Structure (MVP)**

```
parishkeeper/
│
├── core/               # Authentication, users, roles, churches
├── teachings/          # Sunday messages
├── attendance/         # Services + attendance
├── contacts/           # Members & messaging
├── accounts/           # Tithes, offerings, welfare
├── events/             # Events and programs
├── announcements/      # Weekly announcements
├── prayers/            # Prayer requests
├── welfare/            # Welfare cases
├── assets/             # Church properties
├── internships/        # Intern roles and applications
│
├── shared/             # Utilities, mixins, base classes
├── config/             # Settings, URLs, environment
├── docs/               # Documentation
├── scripts/            # Dev tasks and DB tools
│
└── README.md
```

---

## **🗄 Database & Models**

### **Key Models Across Apps**

* **Church** — root entity for multi-tenant data
* **UserProfile** — extends default user with role & church
* **TeachingNote** — Sunday sermon notes with scripture references
* **AttendanceRecord** — who attended and when
* **Transaction** — financial data for tithes, offering, building funds, welfare
* **Event** — upcoming activities
* **Announcement** — weekly information and notices
* **PrayerRequest** — anonymous or member-based requests
* **WelfareCase** — individuals requiring help
* **Asset** — church-owned properties (chairs, land, instruments)
* **InternApplication** — applicants to join the system development team

Indexes exist for:

* `(church_id, date)`
* full-text search on teachings
* JSONB indexes on flexible fields

---

## **🚀 Getting Started (Local Development)**

### **1. Clone the Repo**

```
git clone https://github.com/yourname/parishkeeper.git
cd parishkeeper
```

### **2. Create Virtual Environment**

```
python -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**

```
pip install -r requirements.txt
```

### **4. Create Environment File**

```
cp .env.example .env
```

Fill in:

* DATABASE_URL
* REDIS_URL
* AWS/S3 credentials

### **5. Run Database Migrations**

```
python manage.py migrate
```

### **6. Start Development Server**

```
python manage.py runserver
```

### **7. Start Celery Worker (Optional)**

```
celery -A config worker -l info
```

---

## **🔐 Authentication & Permissions**

### **Authentication**

Uses **JWT**:

* `POST /api/v1/auth/token/`
* `POST /api/v1/auth/refresh/`

### **Roles**

* SuperAdmin
* DioceseAdmin
* ChurchAdmin
* Clergy
* Treasurer
* Secretary
* Volunteer
* Intern

Permissions are app-specific and scoped to the user’s church.

---

## **📡 API Example Endpoints**

### Teachings

`GET /api/v1/teachings/`
`POST /api/v1/teachings/`

### Attendance

`POST /api/v1/attendance/services/`
`POST /api/v1/attendance/services/{id}/checkin/`

### Accounts

`POST /api/v1/accounts/transactions/`
`GET /api/v1/accounts/reports/summary/`

### Prayer Requests

`POST /api/v1/prayers/`
`PATCH /api/v1/prayers/{id}/status/`

---

## **📈 Reporting & Exports (MVP)**

* Attendance summary
* Weekly/monthly finance totals
* Welfare cases
* Prayer request summary
* CSV exports for members, transactions, attendance
* Background export jobs via Celery

---

## **🧪 Testing & Quality**

Use `pytest`:

```
pytest
```

Includes:

* Unit tests for services
* Serializer tests
* API integration tests

CI pipeline (GitHub Actions) handles:

* Linting
* Testing
* Migrations check

---

## **🧰 Development Philosophy**

This project is built to also **train new developers**.
Code emphasizes:

* Clean architecture
* Modularity
* Clear service boundaries
* Thoughtful naming
* Repeatable patterns
* Testability

Interns can learn:

* Django
* DRF
* Multiparty role management
* Postgres optimization
* REST design
* Background job processing
* Data import/export

---

## **🌱 Roadmap (Future Versions)**

* Member-facing mobile/web app
* Event attendance via QR code
* Advanced financial dashboards
* Multi-language support
* Push notifications & SMS
* Voice note support for teachings
* Media library for resources
* Syncing with Diocese HQ system
* Offline mode for rural churches

---

## **🤝 Contributing**

We welcome contributions from interns and developers.

1. Fork the repo
2. Create a feature branch
3. Follow code style guidelines
4. Submit PR with explanation

---

## **📜 License**

MIT License — free to use and expand for any church or ministry.
