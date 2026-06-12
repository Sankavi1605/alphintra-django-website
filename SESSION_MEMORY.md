# Alphintra Project — Session Memory

## Project Overview
- **Type:** Django website for Alphintra (AI-driven product engineering company)
- **Stack:** Django 6.0.5, vanilla HTML/CSS/JS, dark theme
- **Domain:** alphintrabot

## Session: Slideshow Conversion + Cleanup (2026-06-03)

### Changes Made

#### 1. Home Page → Full-Screen Auto Slideshow
- Converted the scrollable home page into a single-viewport auto-advancing slideshow
- 5 slides: Hero → Main Work → Services → Social Links → Chat & Contact
- Auto-advances every 5 seconds, loops infinitely
- Transitions: fade + slide (600ms ease)
- Navigation: dot indicators (bottom center), keyboard arrows, touch swipe, mouse wheel
- Any manual interaction resets the 5-second auto-advance timer

**Files changed:**
- `templates/website/home.html` — Slideshow structure, all JS inline
- `static/css/site.css` — Slideshow CSS (.slide, .slideshow, .slide-dot, .slide-dots)
- `templates/website/base.html` — CSS cache version bumped (`?v=4`)

#### 2. Removed Header Navigation
- Removed Home, Services, Socials links from the header nav bar
- Header now only shows the Alphintra logo (mark + wordmark)

**File changed:**
- `templates/website/base.html` — Removed `<nav class="site-nav">` block

#### 3. Updated Social Links
- X / Twitter: `https://x.com/alphintra_ai` (was `https://x.com/alphintra`)
- Facebook: `https://web.facebook.com/profile.php?id=61589295980353` (was `https://facebook.com/alphintra`)

**File changed:**
- `website/content.py` — `SOCIAL_LINKS` list updated

---

## Key Architecture Notes

### Slideshow CSS Layering Fix
- Slides use `position: absolute` to stack on top of each other
- Inline `style="position: relative; isolation: isolate"` on `<section>` elements **breaks** the stacking — was the root cause of slide 4 being invisible
- `.has-image-bg` class handles `position: relative; isolation: isolate; overflow: hidden` for background images
- Background images use `z-index: -1` to sit behind content
- `.home-shell` must have `height: 100vh; overflow: hidden` to prevent scroll

### CSS Cache Busting
- `templates/website/base.html` line: `<link rel="stylesheet" href="{% static 'css/site.css' %}?v=4">`
- Bump `?v=N` whenever CSS changes to force browser cache refresh

### File Structure
```
templates/website/
  base.html          — Base template (header, chatbot, JS)
  home.html          — Slideshow home page
  about.html         — About page
  services.html      — Services page
  socials.html       — Socials page

static/css/
  site.css           — All styles

website/
  views.py           — Django views
  content.py         — Site content data (SOCIAL_LINKS, SITE_CONTENT)
  urls.py            — URL routes

alphintra_django/
  settings.py        — Django settings
  urls.py            — Root URL config
```

### Running Server
```bash
cd C:/Users/User/OneDrive/Documents/alphintrabot
python manage.py runserver 8000
```
Server runs at `http://127.0.0.1:8000`

### Browser Cache
- Always hard-refresh (`Ctrl+Shift+R`) after CSS changes
- Django dev server has `DEBUG=True` so templates reload, but CSS is cached by browser
