🧩 Role & Objective

You are an expert full-stack developer specialized in Flask web applications.
Your task is to build a complete, production-ready web app called Loanless.

💡 App Description

Loanless is a microloan web application that allows individuals to request small loans with 0% interest rate, only a 2% commission fee.

📄 App Structure (4 Pages)

1. Login / Register Page

User must log in or create an account.

Use SQLite to store users.

Secure passwords (hashing).

Redirect to the main page after login.

2. Main Page

Hero section with:

Background image

A short slogan

A Call to Action (CTA) button → redirects to loan simulation page

Below hero → show Top Offers (example loans like “$500 – 6 months”, “$1000 – 12 months”).

3. Loan Simulation Page

Form fields:

Loan amount

Years of work experience

Sector (dropdown)

Payment period (months)

On submit:

Calculate monthly_payment = (amount + amount \* 0.02) / payment_period

Display the result dynamically.

Buttons:

Subscribe → saves to DB with status = 'draft'

Cancel → returns to main page.

4. Dashboard Page

Show user’s loan subscriptions in a table:

Columns: amount, period, monthly payment, status.

Allow user to view or delete a loan.

Status can be draft or accepted.

🎨 Design & UI Guidelines

Minimalistic, modern design.

Colors: white (#FFFFFF) and green (#2ECC71).

Font: Poppins (Google Fonts).

Use clean spacing, rounded corners, and subtle shadows.

Responsive for both desktop and mobile.

Use Bootstrap or Tailwind CSS.

⚙️ Tech Stack

Backend: Python (Flask)

Database: SQLite

Frontend: HTML, CSS, JS (Bootstrap or Tailwind)

Templating: Jinja2

Authentication: Flask-Login (or custom sessions)

🧱 App Architecture

Use clean Flask structure with Blueprints:

loanless/
│
├── app.py
├── models.py
├── requirements.txt
├── templates/
│ ├── login.html
│ ├── main.html
│ ├── simulate.html
│ └── dashboard.html
├── static/
│ ├── css/
│ └── js/
└── database.db

Database Models:

User(id, username, email, password_hash)

Loan(id, user_id, amount, work_years, sector, payment_period, monthly_payment, status)

🧾 Deliverables

Full Flask app code (ready to run with python app.py).

SQLAlchemy models and database setup.

All HTML templates styled with Bootstrap/Tailwind.

Example test data or demo user.

A short README.md with setup instructions.

⚡ Output Requirements

✅ Output must be fully functional runnable code, not pseudocode.
✅ Include comments and explanations in code.
✅ Organize files properly.
✅ Follow the UI and logic exactly.

🗣️ Prompt Command

Build the complete Loanless Flask web application exactly as specified above.
