# StockFlow — Inventory Management System

A full-stack web application for tracking stock and managing inventory, with hashed authentication and role-based access for administrators and employees. Built with Python and Flask, backed by a normalised SQLite database.

## Screenshots

<h3 align="center">Login</h3>
<p align="center">
  <img width="850" alt="Login screen" src="https://github.com/user-attachments/assets/894f6dbf-8cb1-4a13-b144-804a212d67d8" />
</p>

<h3 align="center">User Management</h3>
<p align="center">
  <img width="850" alt="User management screen" src="https://github.com/user-attachments/assets/39823935-8d11-4ccb-b41b-a0f22e167157" />
</p>

<h3 align="center">Live Inventory Tracking</h3>
<p align="center">
  <img width="850" alt="Live inventory tracking screen" src="https://github.com/user-attachments/assets/772c9174-f0a2-4a16-8c9a-b57a85716b83" />
</p>

<h3 align="center">Product Management</h3>
<p align="center">
  <img width="850" alt="Product management screen" src="https://github.com/user-attachments/assets/9352ead7-a641-4e01-b827-b845d6990ddc" />
</p>

<h3 align="center">Inventory Reporting</h3>
<p align="center">
  <img width="850" alt="Inventory reporting screen" src="https://github.com/user-attachments/assets/41a04ff5-5d12-4dd8-886c-9e89ca2ed497" />
</p>

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
