### Hexlet tests and linter status:
[![Actions Status](https://github.com/vikatresk/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vikatresk/python-project-83/actions)

## Description
Page Analyzer is a Flask web application that allows users to analyze webpages for SEO effectiveness. The application checks whether the webpage is available and analyzes elements such as headers, description, and H1 tags.

## Live App
To view the live Page Analyzer application, [click here](https://python-project-83-1zas.onrender.com).

## Technology stack
- Python
- Flask
- PostgreSQL
- HTML
- Bootstrap
- uv
- gunicorn

## Installation:
1. To install the application:

```git clone git@github.com:vikatresk/python-project-83.git```

2. Create .env file and set SECRET_KEY and DATABASE_URL as in 'env.example'

Then follow these commands:
3. Install dependencies

```make install```

4. Run development server

```make dev```

5. Run production server

```make start```