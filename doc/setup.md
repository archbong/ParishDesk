# Setup Guide
1. Requirements

Python 3.10+

PostgreSQL

Redis

Git

2. Installation
git clone <repo>
cd parishkeeper
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Environment Variables

Copy from .env.example:

SECRET_KEY=
DATABASE_URL=
REDIS_URL=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_BUCKET=

4. Migrate
python manage.py migrate

5. Run
python manage.py runserver

6. Optional: Celery
celery -A config worker -l info
