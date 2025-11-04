# 🚀 Quick Start Guide - Loanless with Admin Portal

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

---

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

---

## Step 2: Run the Application

```bash
python app.py
```

The application will:
- Initialize the database (`database.db`)
- Create demo user account
- Create admin user account
- Start the server on `http://localhost:5000`

---

## Step 3: Access the Application

### For Regular Users:
1. Open browser: `http://localhost:5000`
2. Click "Register" or use demo account:
   - **Username:** `demo`
   - **Password:** `demo123`
3. Access: Main page, Simulate Loan, Dashboard

### For Administrators:
1. Open browser: `http://localhost:5000`
2. Login with admin account:
   - **Username:** `admin`
   - **Password:** `admin123`
3. Automatically redirected to Admin Dashboard

---

## Default Accounts

| Type | Username | Password | Email | Access |
|------|----------|----------|-------|--------|
| Admin | `admin` | `admin123` | admin@loanless.com | Full admin + user portal |
| User | `demo` | `demo123` | demo@loanless.com | User portal only |

---

## Admin Portal Routes

- **Dashboard:** `/admin/dashboard` or `/admin/`
- **Loans:** `/admin/loans`
- **Users:** `/admin/users`
- **Statistics:** `/admin/statistics`

---

## Quick Admin Tasks

### Approve a Loan:
1. Go to `/admin/loans`
2. Filter by status: "Pending"
3. Click approve button (green checkmark)
4. Add optional notes
5. Confirm

### View User Details:
1. Go to `/admin/users`
2. Click eye icon next to user
3. View loans and statistics

### Switch Portals:
- **User → Admin:** Click "Admin Portal" in navigation
- **Admin → User:** Click "User Portal" in sidebar

---

## Project Structure

```
Loanless_Pay/
├── app.py                 # Main Flask application
├── admin.py               # Admin routes
├── models.py              # Database models
├── decorators.py          # Security decorators
├── templates/             # HTML templates
│   ├── admin/            # Admin portal templates
│   └── *.html            # User portal templates
├── static/
│   └── css/
│       ├── admin.css     # Admin styles
│       └── style.css     # User styles
└── instance/
    └── database.db       # SQLite database
```

---

## Common Commands

### Reset Database:
```bash
# Delete database and restart
rm instance/database.db
python app.py
```

### Create New Admin (Python):
```python
from app import app
from models import db, User

with app.app_context():
    admin = User(username='newadmin', email='new@admin.com', is_admin=True)
    admin.set_password('password123')
    db.session.add(admin)
    db.session.commit()
```

---

## Testing Workflow

1. **Login as demo user** → Create loan application
2. **Switch to admin account** → Approve/reject loan
3. **Switch back to demo** → See updated status
4. **Check admin statistics** → View analytics

---

## Important URLs

- **Home:** `http://localhost:5000/`
- **Login:** `http://localhost:5000/login`
- **Register:** `http://localhost:5000/register`
- **User Dashboard:** `http://localhost:5000/dashboard`
- **Admin Dashboard:** `http://localhost:5000/admin/dashboard`

---

## Need Help?

- **Admin Guide:** See `README_ADMIN.md`
- **Setup Guide:** See `README_SETUP.md`
- **Implementation Details:** See `IMPLEMENTATION_SUMMARY.md`

---

## Security Notes

⚠️ **Before Production:**
1. Change default admin password
2. Update `SECRET_KEY` in `app.py`
3. Use environment variables for secrets
4. Enable HTTPS
5. Set `debug=False`

---

## Troubleshooting

### Port Already in Use:
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Locked:
- Close all connections to database
- Restart the application

### Cannot Access Admin Portal:
- Verify user has `is_admin=True` in database
- Check if account is active (`is_active=True`)

---

**Ready to go! 🎉**

Start with `python app.py` and login with `admin`/`admin123` to explore the admin portal.