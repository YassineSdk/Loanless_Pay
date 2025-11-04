# 🏦 Loanless - Microloan Platform

A complete, production-ready web application for managing microloans with 0% interest rate and only 2% commission fee.

## 🎉 LATEST UPDATES (v2.1)

### New Features:
- ✅ **Modern Landing Page** - Professional homepage with products, testimonials, and CTAs
- ✅ **Document Preview** - View uploaded ID and payment statements securely
- ✅ **Payment Schedule** - Full payment tracking for approved loans
- ✅ **Redesigned Statistics** - KPIs on top, minimalistic charts below

See `LATEST_UPDATES.md` for complete details.

---

## 🌟 Features

### 👥 User Portal
- ✅ **Modern Landing Page** - Professional homepage before login (NEW)
- ✅ **User Authentication** - Secure registration and login
- ✅ **Profile Management** - Complete personal information (name, DOB, address, phone, gender)
- ✅ **Loan Simulation** - Calculate monthly payments with real-time calculation
- ✅ **Professional Information** - Job details, salary range, financial status
- ✅ **Document Upload** - Secure ID and payment statement uploads
- ✅ **Document Preview** - View uploaded documents securely (NEW)
- ✅ **Loan Dashboard** - Track all loan applications and their status
- ✅ **Payment Schedule** - View payment breakdown for approved loans (NEW)

### 🔧 Admin Portal
- ✅ **Admin Dashboard** - Statistics, metrics, and KPIs
- ✅ **Loan Management** - Approve/reject loans with filtering and search
- ✅ **User Management** - View, activate/deactivate, and manage users
- ✅ **Statistics & Analytics** - Redesigned with KPIs on top, charts below (NEW)
- ✅ **Document Review** - Access to uploaded user documents
- ✅ **Document Preview** - View all user documents securely (NEW)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Delete old database (if exists):**
```bash
# Windows
del instance\database.db

# Mac/Linux
rm instance/database.db
```

3. **Run the application:**
```bash
python app.py
```

**OR use the startup script (Windows):**
```bash
START.bat
```

4. **Open in browser:**
```
http://localhost:5000
```

## 🔑 Default Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full admin portal + user features

### Demo User Account
- **Username:** `demo`
- **Password:** `demo123`
- **Access:** User portal only

## 📋 User Workflow

```
View Landing Page (NEW)
    ↓
Register Account
    ↓
Complete Profile (Required)
    ↓
Simulate Loan
    ↓
Fill Professional Info
    ↓
Upload Documents (ID + Statements)
    ↓
Submit Application
    ↓
Admin Reviews & Approves
    ↓
Track Status in Dashboard
    ↓
View Payment Schedule (NEW)
    ↓
Preview Documents (NEW)
```

## 🆕 Latest Features (v2.1)

### Modern Landing Page (NEW)
- Professional homepage with gradient hero section
- Feature highlights (Fast, 0% Interest, Secure)
- Product showcase with 3 loan tiers
- Customer testimonials with ratings
- Statistics section (10K+ customers, $5M+ approved)
- Clear call-to-action buttons

### Document Preview (NEW)
- View uploaded ID and payment statements
- Secure access control (users see own, admins see all)
- Opens in new tab for easy viewing
- File type indicators

### Payment Schedule (NEW)
- Full payment breakdown for approved/active loans
- Month-by-month tracking
- Paid vs Pending status indicators
- Collapsible table view
- Total amount calculation

### Redesigned Statistics Page (NEW)
- KPIs displayed prominently at top
- Minimalistic charts at bottom
- Card-based clean design
- Better visual hierarchy
- Financial overview section

### Previous Features (v2.0)
- Profile System with personal information
- Enhanced Loan Application (3-section process)
- Professional Information collection
- Document Upload (ID + Statements)

## 📁 File Structure

```
Loanless_Pay/
├── app.py                      # Main Flask application
├── admin.py                    # Admin portal routes
├── models.py                   # Database models
├── decorators.py               # Security decorators
├── requirements.txt            # Python dependencies
├── START.bat                   # Windows startup script
│
├── templates/
│   ├── admin/                  # Admin portal templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── loans.html
│   │   ├── loan_detail.html
│   │   ├── users.html
│   │   ├── user_detail.html
│   │   └── statistics.html
│   │
│   ├── main.html               # User home page
│   ├── dashboard.html          # User dashboard
│   ├── simulate.html           # Loan simulation (updated)
│   ├── profile.html            # User profile (new)
│   └── login.html              # Login/Register
│
├── static/
│   ├── css/
│   │   ├── style.css           # User portal styles
│   │   └── admin.css           # Admin portal styles
│   └── uploads/                # Document storage
│
└── instance/
    └── database.db             # SQLite database
```

## 💾 Database Schema

### Users Table
- Username, Email, Password (hashed)
- Admin flag, Active flag
- **Personal Info:** Full name, DOB, Address, Gender, Phone
- Profile completion status
- Created at timestamp

### Loans Table
- Amount, Work years, Sector, Payment period
- Monthly payment, Status
- **Professional Info:** Job title, Salary range, Debts, House, Children
- **Documents:** ID path, Payment statements (JSON)
- Admin notes, Approved by
- Created/Updated timestamps

## 🔒 Security Features

- ✅ Password hashing (werkzeug)
- ✅ Role-based access control
- ✅ File upload validation
- ✅ Secure filename sanitization
- ✅ Session management (Flask-Login)
- ✅ CSRF protection
- ✅ Input sanitization
- ✅ SQL injection protection (SQLAlchemy ORM)

## 📊 Loan Statuses

| Status | Description |
|--------|-------------|
| **pending** | Awaiting admin review |
| **approved** | Approved by admin |
| **rejected** | Rejected by admin |
| **active** | Currently being repaid |
| **completed** | Fully repaid |

## 🎨 Design

- **User Portal:** White + Green theme (#2ECC71)
- **Admin Portal:** Dark sidebar + Teal accent (#16a085)
- **Font:** Poppins (Google Fonts)
- **Framework:** Bootstrap 5
- **Icons:** Bootstrap Icons
- **Responsive:** Mobile, Tablet, Desktop

## 📖 Documentation

- **Quick Start:** `RUN_APP.md` - How to run with new features
- **Admin Guide:** `README_ADMIN.md` - Complete admin documentation
- **New Features:** `NEW_FEATURES.md` - Detailed feature breakdown
- **Complete Guide:** `COMPLETE_FEATURES.md` - All features summary
- **Setup Guide:** `README_SETUP.md` - Installation instructions

## 🧪 Testing

### Test User Features:
1. Login as `demo` / `demo123`
2. Complete profile (/profile)
3. Simulate loan (/simulate)
4. Upload sample documents
5. Submit application
6. Check dashboard

### Test Admin Features:
1. Login as `admin` / `admin123`
2. View admin dashboard (/admin/dashboard)
3. Review pending loans (/admin/loans)
4. Approve/reject applications
5. View user details (/admin/users)
6. Check statistics (/admin/statistics)

## ⚠️ Important Notes

### Before Running:
- Delete old database if schema changed
- Ensure Python 3.8+ installed
- Install all dependencies from requirements.txt
- Port 5000 must be available

### Profile Requirements:
- Users MUST complete profile before loan applications
- All profile fields are mandatory
- Profile completion tracked automatically

### Document Requirements:
- ID/Passport is MANDATORY
- At least 1 payment statement required
- Accepted formats: PDF, JPG, JPEG, PNG only
- Maximum 5MB per file

## 🐛 Troubleshooting

### Database Error on Startup
**Problem:** Old database with different schema  
**Solution:** Delete `instance/database.db` and run `python app.py`

### Cannot Apply for Loan
**Problem:** Profile not completed  
**Solution:** Go to Profile page, fill all fields, save

### File Upload Failed
**Problem:** Invalid file type or size  
**Solution:** Check format (PDF/JPG/PNG) and size (max 5MB)

### 403 Forbidden on Admin Routes
**Problem:** User is not admin  
**Solution:** Account must have `is_admin=True` in database

## 🔄 Portal Switching

### For Admin Users:
- **User → Admin:** Click "Admin Portal" in navigation
- **Admin → User:** Click "User Portal" in sidebar

Regular users don't see admin links.

## 📞 Support

For issues or questions:
1. Check documentation in project folder
2. Review error messages in console
3. Verify all dependencies installed
4. Ensure database is fresh (delete and recreate)

## 📜 License

© 2024 Loanless. All rights reserved.

## 🎯 Tech Stack

- **Backend:** Flask 3.x
- **Database:** SQLite (SQLAlchemy ORM)
- **Authentication:** Flask-Login
- **Frontend:** HTML5, CSS3, JavaScript
- **Framework:** Bootstrap 5
- **Icons:** Bootstrap Icons
- **Fonts:** Google Fonts (Poppins)

## ✨ Key Highlights

- 🚀 Production-ready code
- 🔒 Secure file uploads
- 👥 Complete user management
- 📊 Real-time analytics
- 📱 Fully responsive
- 🎨 Modern UI/UX
- 📝 Comprehensive documentation
- ✅ Form validation
- 🔐 Role-based access
- 💾 Automatic data persistence

## 🎉 Version History

**v2.1** (Current)
- Modern landing page before login
- Document preview for users and admins
- Payment schedule for approved loans
- Redesigned statistics page (KPIs + charts)

**v2.0**
- Added user profile system
- Enhanced loan application with professional info
- Document upload functionality
- Improved admin review process

**v1.0**
- Initial release
- Basic loan simulation
- Admin portal
- User dashboard

---

**Ready to get started?** Run `python app.py` or `START.bat` (Windows) and open `http://localhost:5000`!

For detailed guides, see the documentation files in the project folder.