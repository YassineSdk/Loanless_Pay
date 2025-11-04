# 🏦 LoanLess - Microloan Platform

A modern, production-ready web application for managing microloans with 0% interest rate and only 2% commission fee.

---

## 🌟 Features

### 👥 User Portal
- ✅ **Modern Landing Page** - Professional homepage with hero section, features, and testimonials
- ✅ **User Authentication** - Secure registration and login system
- ✅ **Profile Management** - Complete personal information (name, DOB, address, phone, gender)
- ✅ **2-Step Loan Application**
  - Step 1: Loan details (amount, sector, experience, purpose, duration)
  - Step 2: Financial info (employment, debts, property, dependents) + Documents
- ✅ **Real-time Loan Calculator** - Instant monthly payment calculation
- ✅ **Document Upload** - Secure ID and salary statement uploads
- ✅ **Loan Dashboard** - Track all applications and their status
- ✅ **Payment Schedule** - View payment breakdown for approved loans

### 🔧 Admin Portal
- ✅ **Admin Dashboard** - Overview with statistics and KPIs
- ✅ **Loan Management** - Review, approve/reject loans with notes
- ✅ **User Management** - View and manage user accounts
- ✅ **Document Review** - Access to uploaded user documents
- ✅ **Statistics & Analytics** - Charts and financial overview
- ✅ **Search & Filter** - Advanced filtering for loans and users

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```
   
   **OR use the startup script (Windows):**
   ```bash
   START.bat
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

The app will automatically create the database and default accounts on first run.

---

## 🔑 Default Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full admin portal + user features

### Demo User Account
- **Username:** `demo`
- **Password:** `demo123`
- **Access:** User portal only

---

## 📋 User Workflow

```
1. View Landing Page
   ↓
2. Register Account
   ↓
3. Complete Profile (Required before applying)
   ↓
4. Apply for Loan
   ├─ Step 1: Loan Details
   │  - Amount ($500 - $50,000)
   │  - Working sector
   │  - Years of experience
   │  - Loan purpose
   │  - Repayment duration (6-60 months)
   │
   └─ Step 2: Financial Information
      - Job title & salary
      - Other debts status
      - Property ownership
      - Number of dependents
      - Upload ID document
      - Upload salary slips (last 3 months)
   ↓
5. Submit Application
   ↓
6. Admin Reviews & Approves/Rejects
   ↓
7. Track Status in Dashboard
   ↓
8. View Payment Schedule (if approved)
```

---

## 📁 Project Structure

```
Loanless_Pay/
├── app.py                    # Main Flask application
├── admin.py                  # Admin portal routes
├── models.py                 # Database models (User, Loan)
├── decorators.py             # Security decorators
├── requirements.txt          # Python dependencies
├── START.bat                 # Windows startup script
├── clear_db_quick.py         # Quick database reset utility
├── reset_database.py         # Interactive database reset
│
├── templates/
│   ├── base.html             # Main layout template
│   ├── landing.html          # Landing page (before login)
│   ├── login.html            # Login/Register page
│   ├── main.html             # User home page
│   ├── profile.html          # User profile page
│   ├── simulate.html         # 2-step loan application
│   ├── dashboard.html        # User dashboard
│   │
│   └── admin/                # Admin templates
│       ├── base.html
│       ├── dashboard.html
│       ├── loans.html
│       ├── loan_detail.html
│       ├── users.html
│       ├── user_detail.html
│       └── statistics.html
│
├── static/
│   ├── css/
│   │   ├── style.css         # User portal styles
│   │   └── admin.css         # Admin portal styles
│   │
│   └── uploads/              # Document storage
│       └── (user_id)_(timestamp)_(filename)
│
└── instance/
    └── database.db           # SQLite database
```

---

## 💾 Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email
- `password_hash` - Encrypted password
- `is_admin` - Admin flag (True/False)
- `is_active` - Account status (True/False)
- `full_name` - Full name
- `date_of_birth` - Date of birth
- `address` - Full address
- `gender` - Gender (male/female/other)
- `phone_number` - Phone number
- `profile_completed` - Profile completion flag
- `created_at` - Timestamp

### Loans Table
- `id` - Primary key
- `user_id` - Foreign key to Users
- `amount` - Loan amount
- `work_years` - Years of experience
- `sector` - Working sector
- `payment_period` - Duration in months
- `monthly_payment` - Monthly payment amount
- `status` - pending/approved/rejected/active/completed
- `job_title` - Job title
- `salary_range` - Monthly salary range
- `has_other_debts` - Boolean
- `owns_house` - Boolean
- `number_of_children` - Number of dependents
- `id_document` - ID document file path
- `payment_statements` - Salary slips (JSON array)
- `admin_notes` - Admin review notes
- `approved_by` - Admin user ID
- `created_at` - Timestamp
- `updated_at` - Timestamp

---

## 🔒 Security Features

- ✅ Password hashing (Werkzeug)
- ✅ Role-based access control (@admin_required decorator)
- ✅ File upload validation (type and size)
- ✅ Secure filename sanitization
- ✅ Session management (Flask-Login)
- ✅ User owns file verification
- ✅ Input sanitization
- ✅ SQL injection protection (SQLAlchemy ORM)

---

## 📊 Loan Statuses

| Status | Description | Color |
|--------|-------------|-------|
| **pending** | Awaiting admin review | Yellow |
| **approved** | Approved by admin | Green |
| **rejected** | Rejected by admin | Red |
| **active** | Currently being repaid | Blue |
| **completed** | Fully repaid | Gray |

---

## 🎨 Design & Tech Stack

### Colors
- **Primary Teal:** `#0a6d5d` (main brand color)
- **Primary Dark:** `#085648` (hover states)
- **Primary Light:** `#0d8a75` (borders)
- **Primary Lighter:** `#e6f4f2` (backgrounds)
- **Accent Orange:** `#f59e0b` (highlights)

### Technology Stack
- **Backend:** Flask 3.x (Python web framework)
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** Flask-Login
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Tailwind CSS (via CDN)
- **Icons:** Font Awesome
- **Font:** Satoshi (via Fontshare)

---

## 🛠️ Utility Scripts

### Quick Database Reset
```bash
python clear_db_quick.py
```
- Drops all tables
- Creates fresh tables
- Creates default admin and test user
- No confirmation prompts

### Interactive Database Reset
```bash
python reset_database.py
```
- Asks for confirmation
- Option to create custom admin account
- Detailed progress output

---

## 🧪 Testing Guide

### Test User Features:
1. Open `http://localhost:5000`
2. Register new account or login as `demo` / `demo123`
3. Complete profile at `/profile`
4. Apply for loan at `/simulate`
   - Fill Step 1 (loan details)
   - Fill Step 2 (financial info + upload documents)
5. Submit and check dashboard at `/dashboard`

### Test Admin Features:
1. Login as `admin` / `admin123`
2. Access admin portal (automatic redirect)
3. Review pending loans at `/admin/loans`
4. Approve/reject applications
5. View user details at `/admin/users`
6. Check statistics at `/admin/statistics`

---

## 💡 Important Notes

### Profile Requirements
- ⚠️ Users **MUST** complete profile before applying for loans
- All profile fields are mandatory
- Validates before allowing loan application

### Document Requirements
- ✅ ID/Passport is **required**
- ✅ At least 1 salary slip **required**
- ✅ Accepted formats: PDF, JPG, JPEG, PNG only
- ✅ Maximum 5MB per file
- ✅ Multiple files allowed for salary slips

### Loan Calculation
- **Commission:** 2% of loan amount
- **Interest:** 0%
- **Formula:** Monthly Payment = (Amount + 2%) / Duration

---

## 🐛 Troubleshooting

### Database Error on Startup
**Problem:** Old database with outdated schema  
**Solution:**
```bash
# Windows
del instance\database.db
python app.py

# Mac/Linux
rm instance/database.db
python app.py
```

### Cannot Apply for Loan
**Problem:** Profile not completed  
**Solution:** Visit `/profile`, fill all fields, and save

### File Upload Failed
**Problem:** Invalid file type or size  
**Solution:** Use PDF/JPG/PNG format, max 5MB per file

### 403 Forbidden Error
**Problem:** Accessing admin route without admin privileges  
**Solution:** Login with admin account or contact administrator

### Port Already in Use
**Problem:** Port 5000 is occupied  
**Solution:** Stop other Flask apps or change port in `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)
```

---

## 🔄 Admin Portal Access

### For Admin Users:
- **Login:** Automatic redirect to `/admin/dashboard`
- **Switch to User Portal:** Click "User Portal" in sidebar
- **Access:** All user features + admin features

### For Regular Users:
- **Login:** Redirected to `/main`
- **No Admin Access:** Admin links hidden
- **Upgrade to Admin:** Set `is_admin=True` in database

---

## 📱 Responsive Design

- ✅ Mobile: Optimized for phones (320px+)
- ✅ Tablet: Enhanced layout (768px+)
- ✅ Desktop: Full features (1024px+)
- ✅ Touch-friendly: 48px minimum tap targets
- ✅ Adaptive grids: Single/multi-column layouts

---

## 🎯 Key Highlights

- 🚀 Production-ready codebase
- 🔒 Secure file handling
- 👥 Complete user management
- 📊 Real-time analytics
- 📱 Fully responsive design
- 🎨 Modern, minimalistic UI
- ✅ Form validation (client + server)
- 🔐 Role-based access control
- 💾 Persistent data storage
- 📄 Comprehensive documentation

---

## 📞 Support

For issues:
1. Check error messages in terminal
2. Verify all dependencies installed: `pip install -r requirements.txt`
3. Ensure fresh database (delete and recreate)
4. Check Python version: `python --version` (must be 3.8+)

---

## 📜 License

© 2024 LoanLess. All rights reserved.

---

## 🎉 Getting Started

**Ready to launch?**

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open browser
http://localhost:5000
```

**Default Logins:**
- Admin: `admin` / `admin123`
- User: `demo` / `demo123`

Enjoy! 🚀