# 🧪 TESTING GUIDE - LoanLess Application

## Quick Start Testing Guide for New KYC Features

---

## 🚀 SETUP

### 1. Start the Application

**Option A: Use Batch File (Windows)**
```bash
cd Loanless_Pay
START.bat
```

**Option B: Manual Start**
```bash
cd Loanless_Pay/backend
python app.py
```

The application will start on: **http://localhost:5000**

---

## 👥 DEFAULT ACCOUNTS

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full admin portal + user features

### Demo User Account
- **Username:** `demo`
- **Password:** `demo123`
- **Access:** User portal only

---

## 🧪 TEST SCENARIOS

### TEST 1: New User KYC Verification Flow

#### Step 1: Register New User
1. Go to http://localhost:5000
2. Click **"Register"**
3. Fill in:
   - Username: `testuser1`
   - Email: `testuser1@example.com`
   - Password: `test123`
   - Confirm Password: `test123`
4. Click **"Register"**
5. ✅ **Expected:** Redirected to login page with success message

#### Step 2: Login and Check KYC Status
1. Login with `testuser1` / `test123`
2. Click **"KYC Verification"** in the navigation menu
3. ✅ **Expected:** See "Not Submitted" status with blue info box
4. ✅ **Expected:** "Start Verification" button visible

#### Step 3: Complete KYC Verification
1. Click **"Start Verification"**
2. Fill in personal information:
   - Full Name: `John Test Doe`
   - Date of Birth: `1990-01-15`
   - Gender: `Male`
   - Nationality: `American`
   - National ID Number: `123456789`
   - Phone Number: `+1 555 123 4567`
   - Address: `123 Main St, New York, NY 10001, USA`
3. ✅ **Expected:** All fields are validated

#### Step 4: Upload Documents
1. Click **"Choose File"** under National ID/Passport
2. Upload a sample PDF or image file (< 10MB)
3. ✅ **Expected:** Progress bar appears and file uploads
4. ✅ **Expected:** Green checkmark with filename appears
5. Click **"Choose File"** under Proof of Address
6. Upload another sample PDF or image file
7. ✅ **Expected:** Progress bar appears and file uploads

#### Step 5: Submit KYC
1. Check the terms agreement checkbox
2. Click **"Submit KYC Verification"**
3. ✅ **Expected:** Redirected to KYC status page
4. ✅ **Expected:** Status shows "Under Review" (yellow badge)
5. ✅ **Expected:** Personal information is displayed
6. ✅ **Expected:** 2 documents are listed

#### Step 6: Try to Apply for Loan (Should Be Blocked)
1. Click **"Apply for Loan"** in navigation
2. ✅ **Expected:** Redirected back to KYC page
3. ✅ **Expected:** Warning message: "You must complete KYC verification..."

---

### TEST 2: Admin KYC Review Process

#### Step 1: Login as Admin
1. Logout from user account
2. Login with `admin` / `admin123`
3. ✅ **Expected:** Redirected to admin dashboard

#### Step 2: Navigate to KYC Verifications
1. Click **"KYC Verifications"** in sidebar (shield icon)
2. ✅ **Expected:** See list of users with KYC submissions
3. ✅ **Expected:** See `testuser1` with "Pending" status
4. ✅ **Expected:** Statistics cards show correct counts

#### Step 3: Review User KYC
1. Click **"Review"** button next to `testuser1`
2. ✅ **Expected:** See detailed KYC information page
3. ✅ **Expected:** Personal information displayed correctly
4. ✅ **Expected:** 2 documents listed with download buttons
5. ✅ **Expected:** Timeline shows Registration and KYC Submitted

#### Step 4: Download Documents
1. Click **"Download"** on National ID document
2. ✅ **Expected:** File downloads successfully
3. Click **"Download"** on Proof of Address document
4. ✅ **Expected:** File downloads successfully

#### Step 5: Approve KYC
1. Click **"Approve KYC"** button (green)
2. Confirm the action
3. ✅ **Expected:** Success message appears
4. ✅ **Expected:** Status badge changes to "Approved" (green)
5. ✅ **Expected:** Approval date appears in timeline

---

### TEST 3: User After KYC Approval

#### Step 1: Login as Approved User
1. Logout from admin
2. Login with `testuser1` / `test123`
3. Go to **"KYC Verification"** page
4. ✅ **Expected:** Status shows "Approved" (green badge)
5. ✅ **Expected:** "Apply for Loan" button is visible

#### Step 2: Apply for Loan
1. Click **"Apply for Loan"** button
2. ✅ **Expected:** Redirected to loan application form
3. ✅ **Expected:** No blocking message appears
4. Fill in loan details:
   - Loan Amount: `5000`
   - Loan Purpose: `Business expansion`
   - Duration: `12` months
   - Monthly Income: `4000`
   - Employment Status: `Employed`
   - Employer Name: `ABC Company`
   - Other Loans: `No`
5. Click **"Submit Application"**
6. ✅ **Expected:** Application submitted successfully
7. ✅ **Expected:** Can upload financial documents

---

### TEST 4: KYC Rejection Flow

#### Step 1: Create Another User
1. Register new user: `testuser2` / `test123`
2. Complete KYC verification (repeat Test 1, Steps 3-5)

#### Step 2: Admin Rejects KYC
1. Login as admin
2. Go to **KYC Verifications**
3. Click **"Review"** for `testuser2`
4. Click **"Reject KYC"** button (red)
5. ✅ **Expected:** Modal appears asking for reason
6. Enter rejection reason: `Documents are unclear`
7. Click **"Reject KYC"**
8. ✅ **Expected:** Status changes to "Rejected" (red badge)

#### Step 3: User Sees Rejection
1. Login as `testuser2`
2. Go to **KYC Verification** page
3. ✅ **Expected:** Status shows "Rejected" (red badge)
4. ✅ **Expected:** Message: "Your KYC verification was not approved"
5. ✅ **Expected:** Contact support link visible

---

### TEST 5: Document Management

#### Step 1: Delete and Reupload Document
1. Login as a user with pending KYC
2. Go to **KYC Verification** → **"Update Information"**
3. Click **trash icon** on a document
4. Confirm deletion
5. ✅ **Expected:** Document is removed
6. Upload a new document
7. ✅ **Expected:** New document appears with new filename

#### Step 2: Cannot Delete After Approval
1. Login as a user with approved KYC
2. Go to **KYC Verification** page
3. ✅ **Expected:** No delete buttons visible on documents
4. ✅ **Expected:** "Update Information" button not shown

---

### TEST 6: Search and Filter (Admin)

#### Step 1: Search Users
1. Login as admin
2. Go to **KYC Verifications**
3. Enter `testuser1` in search box
4. Click **"Search"**
5. ✅ **Expected:** Only `testuser1` appears in results

#### Step 2: Filter by Status
1. Select **"Approved"** from status dropdown
2. Click **"Search"**
3. ✅ **Expected:** Only approved users appear
4. Select **"Pending Review"** from status dropdown
5. Click **"Search"**
6. ✅ **Expected:** Only pending users appear

#### Step 3: Reset Filters
1. Click **"Reset"** button
2. ✅ **Expected:** All users appear again

---

### TEST 7: Mobile Responsiveness

#### Step 1: Test on Mobile View
1. Open browser developer tools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select **iPhone 12** or similar
4. Navigate through:
   - KYC verification form
   - Document upload
   - Admin KYC review page
5. ✅ **Expected:** All elements are readable and accessible
6. ✅ **Expected:** Buttons are touch-friendly (44px+)
7. ✅ **Expected:** Forms are easy to fill on mobile

---

### TEST 8: File Upload Validation

#### Step 1: Test File Size Limit
1. Go to KYC verification form
2. Try to upload a file > 10MB
3. ✅ **Expected:** Error: "File size exceeds 10MB limit"

#### Step 2: Test File Type Validation
1. Try to upload a .txt or .exe file
2. ✅ **Expected:** Error: "Invalid file type. Please upload PDF, JPG, or PNG"

#### Step 3: Test Required Documents
1. Submit KYC without uploading National ID
2. ✅ **Expected:** Cannot proceed or warning shown
3. Upload only National ID, skip Proof of Address
4. Submit KYC
5. ✅ **Expected:** Warning about missing required document

---

### TEST 9: Pagination (Admin)

#### Step 1: Create Multiple Users (if needed)
1. Register 20+ test users
2. Complete KYC for each

#### Step 2: Test Pagination
1. Login as admin
2. Go to **KYC Verifications**
3. ✅ **Expected:** Shows 20 users per page
4. Click **"Next"** button
5. ✅ **Expected:** Shows next page of users
6. ✅ **Expected:** Page counter updates correctly

---

### TEST 10: Timeline and Statistics

#### Step 1: Check User Timeline
1. Admin views user KYC detail
2. ✅ **Expected:** Timeline shows:
   - Registration date
   - KYC submission date
   - Approval date (if approved)

#### Step 2: Check Statistics
1. Admin dashboard shows KYC statistics
2. ✅ **Expected:** Correct counts for:
   - Total users
   - Pending reviews
   - Approved
   - Rejected
   - Not submitted

---

## 🐛 COMMON ISSUES & SOLUTIONS

### Issue: "Port already in use"
**Solution:** Change port in `app.py` or close other Flask apps

### Issue: "Database error"
**Solution:** Delete `instance/database.db` and restart app

### Issue: "File upload fails"
**Solution:** Check `static/kyc_documents/` folder exists and has write permissions

### Issue: "Documents not showing"
**Solution:** Verify files exist in `static/kyc_documents/` folder

### Issue: "Cannot apply for loan after KYC approval"
**Solution:** Check `user.kyc_status` in database is set to `'approved'`

---

## 📊 VERIFICATION CHECKLIST

### User Features
- [ ] User registration works
- [ ] KYC form validation works
- [ ] Document upload works (both types)
- [ ] Upload progress shows correctly
- [ ] Document delete works (before approval)
- [ ] KYC submission updates status
- [ ] Status page shows correct information
- [ ] Loan application blocks without KYC
- [ ] Loan application allows after KYC approval
- [ ] Navigation menu shows KYC link

### Admin Features
- [ ] KYC verifications list loads
- [ ] Search functionality works
- [ ] Filter by status works
- [ ] Pagination works (if 20+ users)
- [ ] User detail page loads
- [ ] Document download works
- [ ] Approve KYC works
- [ ] Reject KYC works
- [ ] Statistics update correctly
- [ ] Timeline shows correct dates
- [ ] Admin navigation shows KYC link

### Security Features
- [ ] Cannot access KYC routes when logged out
- [ ] Cannot access admin routes as regular user
- [ ] Cannot delete documents after approval
- [ ] Cannot modify approved KYC
- [ ] File size limit enforced (10MB)
- [ ] File type validation works
- [ ] Document ownership verified

### UI/UX Features
- [ ] Status badges show correct colors
- [ ] Icons display correctly
- [ ] Buttons have hover effects
- [ ] Forms have proper validation
- [ ] Error messages are clear
- [ ] Success messages show
- [ ] Mobile view is responsive
- [ ] All text is readable

---

## 📝 TEST DATA SUGGESTIONS

### Sample Users
- `testuser1` - Complete KYC, get approved
- `testuser2` - Complete KYC, get rejected
- `testuser3` - Register but don't complete KYC
- `testuser4` - Complete KYC, test document upload
- `testuser5` - Complete KYC, apply for loan after approval

### Sample Documents
- **National ID:** Any PDF or JPG file (rename to `national_id.pdf`)
- **Proof of Address:** Any PDF or JPG file (rename to `utility_bill.pdf`)
- **Test Files:** Create various sizes to test 10MB limit

---

## 🎯 PERFORMANCE CHECKS

### Page Load Times
- [ ] Landing page loads < 2 seconds
- [ ] KYC form loads < 1 second
- [ ] Admin list loads < 2 seconds (with 100+ users)
- [ ] Document download starts immediately

### Upload Performance
- [ ] 1MB file uploads in < 5 seconds
- [ ] 10MB file uploads in < 30 seconds
- [ ] Progress bar updates smoothly
- [ ] Multiple uploads don't interfere

---

## 📞 SUPPORT

### For Issues
1. Check browser console (F12) for JavaScript errors
2. Check Flask terminal for Python errors
3. Verify database exists: `instance/database.db`
4. Verify upload folders exist and have permissions
5. Try clearing browser cache and cookies

### Test Environment
- **Browser:** Chrome, Firefox, Safari, Edge
- **Python Version:** 3.8+
- **Operating System:** Windows, macOS, Linux

---

## ✅ SIGN-OFF CHECKLIST

Before considering testing complete:

- [ ] All 10 test scenarios passed
- [ ] All verification checklist items checked
- [ ] No console errors
- [ ] No broken images or links
- [ ] All forms submit correctly
- [ ] All buttons work
- [ ] Mobile view tested
- [ ] Documents upload and download
- [ ] Admin can approve/reject
- [ ] Users can apply for loans after KYC
- [ ] Security checks passed

---

**Happy Testing! 🎉**

*Last Updated: January 14, 2026*
*Version: 1.0*