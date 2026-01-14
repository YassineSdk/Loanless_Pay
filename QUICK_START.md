# 🚀 Quick Start Guide - Loanless Pay

## ⚡ Start the Application (30 seconds)

### Windows Users:
```bash
# Double-click or run:
START.bat
```

### Manual Start:
```bash
cd backend
python app.py
```

### Then open your browser:
```
http://localhost:5000
```

---

## 🔐 Login Credentials

### Admin Access
- Username: `admin`
- Password: `admin123`
- Features: Full admin dashboard + loan management

### Demo User
- Username: `demo`
- Password: `demo123`
- Features: User portal only

---

## 📱 First Time User Journey (5 minutes)

### 1. Register (1 min)
1. Go to http://localhost:5000
2. Click "Sign Up"
3. Fill in:
   - Username
   - Email
   - Password
   - Confirm Password
4. Click "Sign Up"

### 2. Login (30 sec)
1. Enter your username and password
2. Click "Log In"

### 3. Complete Profile (2 min)
1. Go to "Profile" in the menu
2. Fill in all required fields (*):
   - Full Name
   - Date of Birth
   - Gender
   - Phone Number
   - Address
3. Click "Save Changes"

### 4. Apply for Loan (2 min)
1. Click "Apply for Loan"
2. **Step 1:** Enter loan details
   - Amount: $500 - $50,000
   - Sector (e.g., Technology)
   - Years of experience
   - Payment period (6-60 months)
3. Click "Next Step"
4. **Step 2:** Enter financial info
   - Job title
   - Salary range
   - Upload ID document (PDF/JPG/PNG)
   - Upload salary slips (1-3 files)
5. Click "Submit Application"

### 5. Track Your Loan
1. Go to "My Loans"
2. See your application status
3. View payment schedule (if approved)

---

## 👨‍💼 Admin Access

### Login as Admin
1. Username: `admin`
2. Password: `admin123`
3. Auto-redirects to admin dashboard

### Admin Features
- ✅ View all loans and users
- ✅ Approve/Reject loan applications
- ✅ View uploaded documents
- ✅ See statistics and charts
- ✅ Manage user accounts

---

## 🎯 Key Pages

| Page | URL | Description |
|------|-----|-------------|
| **Home** | `/` | Landing page |
| **Login** | `/login` | Sign in |
| **Register** | `/register` | Create account |
| **User Home** | `/main` | User dashboard |
| **Profile** | `/profile` | Edit profile |
| **Apply Loan** | `/simulate` | Loan application |
| **My Loans** | `/dashboard` | Track loans |
| **Admin** | `/admin/dashboard` | Admin portal |

---

## 💡 Tips

### Profile Completion
- ⚠️ **Must complete profile before applying for loans**
- All fields with * are required
- Use format YYYY-MM-DD for date of birth

### File Uploads
- ✅ Accepted formats: PDF, PNG, JPG, JPEG
- ✅ Maximum size: 5MB per file
- ✅ Required: ID document + at least 1 salary slip
- ✅ Can upload multiple salary slips

### Loan Calculation
- Commission: 2% of loan amount
- Interest: 0%
- Formula: Monthly Payment = (Amount + 2%) ÷ Duration

---

## 🔧 Troubleshooting

### App won't start
```bash
# Make sure you're in the right directory
cd backend
python app.py
```

### Can't apply for loan
- Complete your profile first!
- Go to `/profile` and fill all fields

### File upload fails
- Check file size (max 5MB)
- Use only PDF, PNG, JPG, JPEG
- Upload at least 1 ID and 1 salary slip

### Forgot to create admin account
```bash
cd backend
python reset_database.py
```

---

## 📦 Database Reset

### Quick Reset (No prompts)
```bash
cd backend
python clear_db_quick.py
```

### Interactive Reset
```bash
cd backend
python reset_database.py
```

This recreates:
- ✅ Admin user (admin/admin123)
- ✅ Demo user (demo/demo123)
- ✅ Fresh database

---

## 🎨 Features Overview

### User Portal
- Modern landing page
- Secure login/registration
- Profile management
- 2-step loan application
- Real-time loan calculator
- Document uploads
- Loan tracking dashboard
- Payment schedules

### Admin Portal
- Dashboard with statistics
- Loan approval/rejection
- User management
- Document viewing
- Search and filters
- Analytics charts

---

## 🌐 Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS (Tailwind), JavaScript
- **Authentication:** Flask-Login
- **Templates:** Jinja2

---

## ✅ Quick Checklist

Before using the app:
- [ ] Python installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] App started (`START.bat` or `python app.py`)
- [ ] Browser open (`http://localhost:5000`)

As a new user:
- [ ] Registered account
- [ ] Logged in
- [ ] Completed profile
- [ ] Applied for loan
- [ ] Tracking in dashboard

As an admin:
- [ ] Logged in as admin
- [ ] Viewed dashboard
- [ ] Reviewed pending loans
- [ ] Approved/Rejected applications

---

## 🆘 Common Questions

**Q: Can I change my username?**
A: No, username is permanent. Only profile info is editable.

**Q: How long for loan approval?**
A: Admin reviews manually. Typically within 24 hours.

**Q: Can I apply for multiple loans?**
A: Yes! You can track all loans in "My Loans" dashboard.

**Q: What if I forgot my password?**
A: Currently no reset feature. Contact admin or recreate account.

**Q: How do I become an admin?**
A: Set `is_admin=True` in database or use default admin account.

---

## 🎉 You're Ready!

The app is fully integrated and ready to use. Enjoy exploring Loanless Pay!

**Need help?** Check the README.md or INTEGRATION_SUMMARY.md for detailed documentation.

---

*Happy Lending! 💰*