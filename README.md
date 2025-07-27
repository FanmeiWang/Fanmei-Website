# Personal Academic Portfolio Website

> A Flask‑powered site for presenting my education history, publications, projects, teaching portfolio, and presentations.
> **Private project:** the data are personal; please do **not** run or redeploy this site without my express permission.

## Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Deployment to Render](#deployment-to-render)
* [Updating Content](#updating-content)
* [License](#license)

## Features

* Multi‑page, data‑driven academic portfolio (`/`, `/about`, `/education`, `/publications`, `/projects`, `/teaching`, `/presentations`)
* Clean Jinja2 templates with Bootstrap styling
* Centralised data objects in **app.py** for one‑file maintenance
* Responsive routing and static assets (images, videos, PDFs)
* Production‑ready via **Gunicorn** WSGI server on Render

## Tech Stack

| Layer     | Technology                      |
| --------- | ------------------------------- |
| Back‑end  | Python 3.x · Flask 3 · Gunicorn |
| Front‑end | Jinja2 · Bootstrap 5            |
| Hosting   | Render Web Service              |

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── Procfile            # Render entry point
├── runtime.txt         # (optional) pin Python version
├── templates/
│   └── *.html          # Jinja2 pages
└── static/
    ├── images/
    ├── video/
    ├── css/
    └── ...
```

## Deployment to Render

1. **Prepare the repo**

   * `requirements.txt` — generated with `pip freeze`.
   * `Procfile` —

     ```Procfile
     web: gunicorn app:app --bind 0.0.0.0:$PORT
     ```
   * (Optional) `runtime.txt` — e.g. `python-3.10.14` to pin the Python version.

2. **Create a new *Web Service***
   Connect the repository in Render → set *Start Command* to the line above → choose an instance type (Free is enough) → **Create Web Service**.

3. **Automatic redeploys**
   Each push to the main branch triggers a fresh build and deployment.

> **Tip:** Check the *Logs* tab in Render for build or runtime errors if the service fails to start.

## Updating Content

All portfolio data live in Python lists/dicts inside **app.py**.
Edit them, commit, and push—Render will rebuild.

## License

Distributed under the MIT License.
