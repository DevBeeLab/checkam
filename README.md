# Checkam 💰

> *"Check am"* — Nigerian Pidgin for "check it"

A full-stack personal finance tracker built for Nigerian users. Log income and expenses, set category budgets, visualise your spending with charts, and export your transaction history — all backed by a secure multi-user Django backend.

🌐 **Live Demo:** [devbee-checkam.onrender.com](https://devbee-checkam.onrender.com/)

---

## 🎥 Demo Video

| Platform | Link |
|----------|------|
| YouTube  | [Watch on YouTube](https://youtu.be/O6kaVjec9T8) |
| Loom     | [Watch on Loom](https://www.loom.com/share/cbbfe043e4194c3f961204a3cb769de5) |

---

## 📸 Screenshots

| Dashboard | Transactions | Budgets |
|-----------|-------------|---------|
| Balance summary + charts | Filter, search, sort | Progress bars per category |

---

## ✨ Features

- **Landing Page** — Marketing page with hero section, features overview, and sign-up CTA
- **Authentication** — Sign up with username, sign in, password change, session management
- **Dashboard** — Total balance, income, expenses, savings rate; Income vs Expense doughnut chart; Spending by Category doughnut chart
- **Transactions** — Add, edit, delete; filter by type/category, search by description, sort by date or amount, paginated; responsive card layout on mobile
- **Budgets** — Set a monthly limit per spending category; live progress bar shows amount spent vs limit, remaining balance, and over-budget alerts
- **Reports** — Monthly Income vs Expenses bar chart (last 6 months); category breakdown doughnut; budget performance bar chart; CSV export
- **Settings** — Update profile name and password
- **Error Pages** — Custom 404 and 500 error pages
- **Security** — All views protected with `@login_required`; all queries scoped to `request.user`

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Django 6 |
| Database | Neon (PostgreSQL) |
| Frontend | Vanilla JavaScript, Chart.js |
| Fonts | Space Mono, Sora, Outfit |
| Icons | Font Awesome 6 |
| Styling | Custom CSS — no frameworks |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/DevBeeLab/checkam.git
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

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your-database-url-here
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

## 🧪 Running Tests

```bash
python manage.py test checkam
```

8 tests covering model behaviour, view access control, and CRUD operations.

---

## 📁 Project Structure

```
checkam/
├── checkam/                  # Main Django app
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   ├── base.html         # Base layout + global modals
│   │   ├── landing/          # Landing page
│   │   ├── auth/             # Sign in / Sign up
│   │   ├── dashboard/
│   │   ├── transactions/
│   │   ├── budgets/
│   │   ├── reports/
│   │   ├── settings/
│   │   ├── partials/         # Sidebar, navbar, footer
│   │   ├── 404.html
│   │   └── 500.html
│   ├── models.py             # Transactions, Budget models
│   ├── views.py              # All views + JSON APIs
│   ├── urls.py               # URL routing
│   └── tests.py              # Unit tests
├── static/
│   ├── css/                  # Per-page stylesheets
│   └── js/                   # modals.js, transactions.js, dashboard.js, reports.js, etc.
├── core/                     # Django project settings
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 🔌 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/transactions/` | All transactions (JSON) |
| GET | `/api/monthly-summary/` | Income & expense grouped by month |
| GET | `/api/category-summary/` | Expense totals by category |
| GET | `/api/budget-performance/` | Budget limit vs spent per category |
| GET | `/export-csv/` | Download transactions as CSV |

---

## 🎨 Colour Palette

| Role | Colour |
|------|--------|
| Primary (Navy) | `#0A3D62` |
| Income (Green) | `#1E8449` |
| Expense (Red) | `#C0392B` |
| Background | `#F0F4F8` |
| Card | `#FFFFFF` |

---

## 🎓 Capstone Context

Built as part of the **IDA/3MTT Software Development** programme, Full Stack Track (Tasks 87–95). Covers Django models, class-based and function-based views, user authentication, ORM aggregations, CSV export, Chart.js data visualisation, and Django unit testing.

---

## 👨‍💻 Author

**Ibrahim Ganiyu (DevBee)**
- Portfolio: [dev-bee.vercel.app](https://dev-bee.vercel.app)
- GitHub: [@DevBeeLab](https://github.com/DevBeeLab)

---

## 📄 License

MIT
