# Architecture Summary
Tech Stack

Django 4+

Django REST Framework

PostgreSQL

Redis + Celery (background tasks)

JWT (SimpleJWT)

AWS S3 (optional for storage)

Application Design

Modular apps: one domain = one Django app

Multi-church support using Church foreign key on all models

Service layer for business logic

Repository-like pattern for database access via DRF serializers

Role-based access with Groups and Permissions

Key Components

config/ — global settings & environment

core/ — auth, user profiles, churches, roles

teachings/ — Sunday sermon notes

attendance/ — service and attendance logs

accounts/ — financial records

events/ — church programs

announcements/ — notices

prayers/ — prayer requests

welfare/ — welfare cases

assets/ — inventory

contacts/ — members & messaging

internships/ — contributor application system
