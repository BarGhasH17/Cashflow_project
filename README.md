# Cashflow Project

A web application for managing cash flow (ДДС – движение денежных средств), built with Django and SQLite.

## Features

- **Create, edit, delete, and view** cash‑flow records.
- Record fields:
  - **Date** (auto‑filled, editable)
  - **Status** – Business, Personal, Tax (the list is fully editable)
  - **Type** – Income, Expense (the list is fully editable)
  - **Category** and **Subcategory** (hierarchical, user‑defined)
  - **Amount** in RUB
  - Optional **Comment**
- **Filter** records by date range, status, type, category, and subcategory.
- **Manage reference lists** (status, type, category, subcategory) from the admin panel or a dedicated UI.
- **Logical dependencies**
  - Categories belong to specific types.
  - Subcategories belong to specific categories.
- **Validation** on both client and server sides.

## Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Backend    | Django 4.x          |
| Database   | SQLite (plug‑and‑play with PostgreSQL) |
| Front‑end  | Django templates + Bootstrap + vanilla JS |
| Admin      | Django Admin (extended) |

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/BarGhasH17/Cashflow_project.git
cd Cashflow_project
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scriptsctivate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. (Optional) Create a super‑user
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser.

## Admin Panel

- URL: <http://127.0.0.1:8000/admin/>
- Manage statuses, types, categories, subcategories, and cash‑flow records.

## Screenshots

_Add screenshots or a demo link here._

## License

MIT License — see `LICENSE` file for details.

## Author

Your Name @YourGitHubUsername
