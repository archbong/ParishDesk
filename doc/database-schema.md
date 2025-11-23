Entity Relationship Overview
Core Entities

Church

UserProfile → FK: Church, User

Role/Group → Permissions

Teachings

TeachingNote → Church, User, Scriptures (JSONB)

Attendance

Service → Church, date, type

AttendanceRecord → Service, User/Contact, category

Accounts

Transaction → Church, type, amount, date
Types: tithe, offering, welfare, building support

Events

Event → Church, start date, description

Announcements

Announcement → Church, week, message

Prayers

PrayerRequest → Church, submitted_by, status

Welfare

WelfareCase → Church, person, need, status

Assets

Asset → Church, category, value, description

Contacts

Contact → Church, name, email, phone

Internships

InternApplication → name, skills, status
