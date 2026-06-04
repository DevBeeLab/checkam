# Checkam 💰

> *"Check am"* — Nigerian Pidgin for "check it"

A personal finance tracker built for Nigerian users. Log income and expenses, set category budgets, visualise your spending with charts, and export your transaction history — all backed by a secure multi-user Django backend.

---

## Screenshots

| Dashboard | Transactions | Budgets |
|-----------|-------------|---------|
| Balance summary + charts | Filter, search, sort | Progress bars per category |

---

## Features

- **Authentication** — Sign up, sign in, password change, session management
- **Transactions** — Add, edit, delete; filter by type/category, search by description, sort by date or amount, paginated table
- **Budgets** — Set a monthly limit per spending category; live progress bar shows amount spent vs limit, remaining balance, and over-budget alerts
- **Dashboard** — Total balance, income, expenses, savings rate; Income vs Expense doughnut chart; Spending by Category doughnut chart
- **Reports** — Monthly Income vs Expenses bar chart (last 6 months); Category breakdown doughnut; Budget performance bar chart; CSV export
- **Settings** — Update profile name; change password
- **Security** — All views protected with `@login_required`; all queries scoped to `request.user`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Django 6 |
| Database | SQLite (dev) |
| Frontend | Vanilla JS, Chart.js |
| Fonts | Space Mono (numbers), Outfit (body) |
| Icons | Font Awesome 6 |
| Styling | Custom CSS with CSS variables |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/checkam.git
cd checkam
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Running Tests

```bash
python manage.py test checkam
```

8 tests covering model behaviour, view access control, and CRUD operations.

---

## Project Structure

```
checkam/
├── checkam/                  # Main Django app
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   ├── base.html         # Base layout + global modals
│   │   ├── dashboard/
│   │   ├── transactions/
│   │   ├── budgets/
│   │   ├── reports/
│   │   ├── settings/
│   │   └── partials/         # Sidebar, navbar, footer
│   ├── models.py             # Transactions, Budget models
│   ├── views.py              # All views + JSON APIs
│   ├── urls.py               # URL routing
│   └── tests.py              # Unit tests
├── static/
│   ├── css/                  # Per-page stylesheets + base
│   └── js/                   # modals.js, transactions.js, dashboard.js, etc.
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/transactions/` | All transactions (JSON) |
| GET | `/api/monthly-summary/` | Income & expense by month |
| GET | `/api/category-summary/` | Expense totals by category |
| GET | `/api/budget-performance/` | Budget limit vs spent |
| GET | `/export-csv/` | Download transactions as CSV |

---

## Colour Palette

| Role | Colour |
|------|--------|
| Primary (Navy) | `#0A3D62` |
| Income (Green) | `#1E8449` |
| Expense (Red) | `#C0392B` |
| Background | `#F0F4F8` |
| Card | `#FFFFFF` |

---

## Capstone Context

Built as part of the **IDA/3MTT Software Development** programme, Full Stack Track (Tasks 87–95). Covers Django models, class-based views, user authentication, ORM aggregations, CSV export, Chart.js integration, and Django unit testing.

---

## License

MIT
