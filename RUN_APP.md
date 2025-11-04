# 🚀 Run Loanless Application - Updated with New Features

## Quick Start

### Step 1: Delete Old Database (IMPORTANT!)
The database schema has been updated with new fields. You must delete the old database first:

```bash
# On Windows
del instance\database.db

# On Mac/Linux
rm instance/database.db
```

### Step 2: Run the Application

```bash
python app.py
```

The application will:
- Create a new database with updated schema
- Create demo user account
- Create admin user account
- Start server on `http://localhost:5000`

### Step 3: Open in Browser

Navigate to: `http://localhost:5000`

---

## 🆕 NEW FEATURES ADDED

### 1. User Profile System ✨

**Complete your profile before applying for loans!**

- **Access:** Click "Profile" in navigation menu
- **Required Fields:**
  - Full Name
  - Date of Birth
  - Gender (Male/Female/Other)
  - Phone Number
  - Address
  - Email (pre-filled, can be updated)

**Why it matters:** Profile must be completed before you can submit loan applications.

---

### 2. Enhanced Loan Simulation 📊

**New 3-Section Application Process:**

#### Section 1: Loan Calculator (Left Side - Always Visible)
- Loan Amount ($100 - $100,000)
- Work Experience (Years)
- Sector Selection
- Payment Period (1-60 months)
- **Auto-calculates monthly payment**
- Click "Subscribe to Loan" to proceed

#### Section 2: Professional Information (Shows after Subscribe)
- **Job Title** (e.g., Software Engineer)
- **Salary Range** (dropdown):
  - < $30,000
  - $30,000 - $50,000
  - $50,000 - $75,000
  - $75,000 - $100,000
  - $100,000 - $150,000
  - > $150,000
- **Do you have other debts?** (Yes/No)
- **Do you own a house?** (Yes/No)
- **Number of Children** (0-20)

#### Section 3: Document Upload (Shows after Subscribe)
**REQUIRED DOCUMENTS:**

1. **ID or Passport** (Required)
   - Government-issued ID or passport
   - Formats: PDF, JPG, PNG
   - Max size: 5MB

2. **Last 6 Months Payment Statements** (Required)
   - Bank statements, pay slips, etc.
   - Can upload multiple files
   - Formats: PDF, JPG, PNG
   - Max size: 5MB each

---

## 🔄 User Workflow

### For New Users:

1. **Register** → Create account
2. **Complete Profile** → Fill personal information
3. **Simulate Loan** → Calculate loan terms
4. **Subscribe** → Fill professional info & upload documents
5. **Submit** → Application goes to admin for review
6. **Dashboard** → Track application status

### For Admins:

1. **Login with admin credentials**
2. **Review Applications** → See all professional info & documents
3. **Approve/Reject** → Make decisions with notes
4. **Monitor** → Track all users and loans

---

## 📁 File Uploads

All uploaded documents are stored in:
```
Loanless_Pay/static/uploads/
```

**Filename Format:**
- `{user_id}_{timestamp}_id_{original_filename}`
- `{user_id}_{timestamp}_statement_{index}_{original_filename}`

**Security:**
- Only allowed extensions: PDF, JPG, JPEG, PNG
- Maximum file size: 5MB per file
- Files are validated before upload

---

## 🔐 Default Accounts

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full admin portal + user features
- **Can:** View documents, approve/reject loans, manage users

### Demo User Account
- **Username:** `demo`
- **Password:** `demo123`
- **Access:** User portal only
- **Must:** Complete profile to apply for loans

---

## 📋 Application Process Flow

```
User Registration
      ↓
Complete Profile (REQUIRED)
      ↓
Loan Simulation (Calculator)
      ↓
Click "Subscribe to Loan"
      ↓
Fill Professional Information
      ↓
Upload Required Documents
      ↓
Submit Application (Status: Pending)
      ↓
Admin Reviews Application
      ↓
Admin Approves/Rejects
      ↓
User Notified (See in Dashboard)
```

---

## 🎯 Testing the New Features

### Test Profile System:
1. Login as demo user
2. Click "Profile" in navigation
3. Fill all required fields
4. Save profile
5. See "Profile Complete" badge

### Test Loan Application:
1. Go to "Simulate Loan"
2. Enter loan details (amount, period, etc.)
3. Click "Subscribe to Loan" button
4. Professional info section appears
5. Fill job title, salary range, etc.
6. Document upload section appears
7. Upload ID document (any PDF/image)
8. Upload payment statements (can select multiple)
9. See file preview
10. Click "Submit Loan Application"
11. Check Dashboard for new application

### Test Admin Review:
1. Logout and login as admin
2. Go to Admin Portal → Loans
3. See new application with all details
4. Click "View Details" to see professional info
5. Documents are stored (paths shown in database)
6. Approve or reject the loan

---

## 🗄️ Database Changes

### User Model - New Fields:
```python
full_name           # String(200)
date_of_birth       # Date
address             # Text
gender              # String(20) - male/female/other
phone_number        # String(20)
profile_completed   # Boolean - auto-set when profile filled
```

### Loan Model - New Fields:
```python
# Professional Information
job_title           # String(200)
salary_range        # String(50)
has_other_debts     # Boolean
owns_house          # Boolean
number_of_children  # Integer

# Documents (file paths)
id_document         # String(500) - path to ID file
payment_statements  # Text - JSON array of file paths
```

---

## ⚠️ Important Notes

### Before Running:
- ✅ Delete old database (schema changed!)
- ✅ Ensure `static/uploads/` folder exists (auto-created)
- ✅ Python 3.8+ installed
- ✅ All dependencies installed (`pip install -r requirements.txt`)

### Profile Requirements:
- ⚠️ Users CANNOT apply for loans without completing profile
- ⚠️ All profile fields are mandatory
- ⚠️ Date of birth must be valid date

### Document Requirements:
- ⚠️ ID document is MANDATORY
- ⚠️ At least 1 payment statement required
- ⚠️ Only PDF, JPG, JPEG, PNG accepted
- ⚠️ 5MB max per file
- ⚠️ Application will not submit without documents

---

## 🎨 UI Updates

### New Pages:
- **Profile Page** (`/profile`) - Complete personal information
- **Enhanced Simulate Page** - 3-column layout with conditional sections

### Navigation Updates:
All pages now include "Profile" link in navigation menu.

### Visual Indicators:
- ✅ Green badge: Profile Complete
- ⚠️ Yellow badge: Profile Incomplete
- 📁 File preview: Shows selected files with icons and sizes
- 🔒 Disabled submit: Until profile is complete

---

## 🐛 Troubleshooting

### "Profile Incomplete" Error:
- Go to Profile page
- Fill ALL required fields
- Click "Save Profile"
- Try loan application again

### "Upload Failed" Error:
- Check file format (PDF, JPG, PNG only)
- Check file size (max 5MB)
- Ensure file is not corrupted

### Documents Not Showing in Admin:
- Documents are stored as file paths in database
- Actual files in `static/uploads/` folder
- Admin sees the file paths (future: add download links)

### Database Error on Startup:
- Old database exists with different schema
- Delete `instance/database.db`
- Run `python app.py` again

---

## 📞 Support

For issues:
1. Check this guide
2. Review `README_ADMIN.md` for admin features
3. Check console for error messages
4. Ensure all dependencies installed

---

## 🔄 Migration from Old Version

If you have existing data:

1. **Backup your old database:**
   ```bash
   cp instance/database.db instance/database_backup.db
   ```

2. **Delete old database:**
   ```bash
   rm instance/database.db
   ```

3. **Run app to create new schema:**
   ```bash
   python app.py
   ```

4. **Note:** Old data will be lost. This is a schema upgrade.

---

## ✅ Checklist Before First Run

- [ ] Old database deleted
- [ ] Virtual environment activated (if using)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Port 5000 available
- [ ] Browser ready (Chrome/Firefox/Edge)

---

**Ready to start!** 🎉

Run: `python app.py`
Open: `http://localhost:5000`
Login: `demo` / `demo123` or `admin` / `admin123`

Enjoy the enhanced Loanless application with profile system, professional information, and document uploads! 🚀