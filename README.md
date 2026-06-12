# Alphintra Django Website

This project is now a Django-only implementation of the Alphintra website for lighter server-rendered delivery and simpler deployment.

## Django pages

- `/` home page
- `/about/` company details
- `/services/` service details
- `/socials/` official social links

## Run locally

1. Install Python dependencies:
   `pip install -r requirements.txt`
2. Run migrations:
   `python manage.py migrate`
3. Start the Django server:
   `python manage.py runserver`
4. Open `http://127.0.0.1:8000`

## Notes

- The site uses remote brand assets and a remote background video.
- Company content is stored in `website/content.py`.
- Static styling is in `static/css/site.css`.
