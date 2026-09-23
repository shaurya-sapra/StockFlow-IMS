# StockFlow — Inventory Management System

A full-stack web application for tracking stock and managing inventory, with hashed authentication and role-based access for administrators and employees. Built with Python and Flask, backed by a normalised SQLite database.

<!-- Add a screenshot to make this pop — run the app, take a screenshot of the inventory
     or reporting page, save it as screenshots/dashboard.png, and uncomment the line below. -->
<!-- ![StockFlow dashboard](screenshots/dashboard.png) -->

---

## Overview

StockFlow lets a team keep on top of physical stock in one place: staff can view live inventory, update stock levels and inspect product details, while administrators additionally manage the product catalogue and user accounts. An inventory reporting page turns the underlying data into charts and metrics so trends are visible at a glance.

The application is organised around a normalised relational schema (users, categories, products, stock and an inventory log), a Flask API, and a set of server-rendered pages, with unit tests covering the authentication and database layers.

## Features

- **Authentication** - login is required for every page; only registered users can access the system, with passwords stored as hashes (never in plain text).
- **Role-based access** - administrators and employees see different capabilities; admin-only actions (managing users and the product catalogue) are protected server-side.
- **Live inventory tracking** - view current stock, update quantities, and inspect full product details.
- **Product management** *(admin)* - add and remove products from the catalogue.
- **User management** *(admin)* - add users and promote, demote or remove them.
- **Inventory reporting** - category distribution and stock-history visualisations, plus key metrics.
- **Audit logging** - stock changes are recorded in an inventory-log table for traceability.

## Tech Stack

- **Backend:** Python, Flask, Werkzeug (password hashing)
- **Database:** SQLite (normalised schema)
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** pytest

## Getting Started

**Prerequisites:** Python 3.9+

```bash
# 1. Clone the repository
git clone https://github.com/shaurya-sapra/StockFlow-IMS
cd stockflow-ims

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python run.py
```

Then open **http://127.0.0.1:5001** in your browser. The database is created and seeded automatically on first run.

### Demo logins

| Role     | Email                    | Password           |
|----------|--------------------------|--------------------|
| Admin    | `tester1@stockflow.com`  | `tester1password`  |
| Employee | `tester3@stockflow.com`  | `tester3password`  |

## Running the Tests

```bash
pytest
```

The pytests covers login, logout and the database layer.

## Project Structure

```
StockFlow-IMS/
├── app/
│   ├── routes/          # Flask routes and API endpoints
│   ├── templates/       # HTML pages
│   ├── static/          # CSS, JavaScript and images
│   └── database.py      # Schema definition and seeding
├── tests/               # pytest test suite
├── run.py               # Application entry point
└── requirements.txt
```

## Possible Improvements

- Move the Flask secret key and configuration into environment variables (would be done in a fully deployed real-case scenario)
- Add pagination and search to the inventory table
- Containerise with Docker for one-command setup
