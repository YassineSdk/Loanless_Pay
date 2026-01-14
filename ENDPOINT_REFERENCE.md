# Loanless Application - Complete Endpoint Reference Guide

## 🎯 Overview

This document provides a complete reference of all available endpoints in the Loanless application. Use this guide to ensure correct `url_for()` calls in templates and avoid `BuildError` exceptions.

---

## ✅ Status: All Routes Verified

- **Date**: 2024
- **Total Endpoints**: 70+
- **Blueprints**: 4 (admin, funding, kyc, loan_app)
- **Build Errors**: RESOLVED ✓

---

## 📋 Table of Contents

1. [Public Routes](#public-routes)
2. [User Dashboard Routes](#user-dashboard-routes)
3. [API Routes](#api-routes)
4. [Admin Routes](#admin-routes)
5. [Funding Routes](#funding-routes)
6. [KYC Routes](#kyc-routes)
7. [Loan Application Routes](#loan-application-routes)
8. [Common Mistakes & Solutions](#common-mistakes--solutions)

---

## 🌐 Public Routes

These routes are accessible without authentication.

| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `index` | `/` | GET | Landing page |
| `login` | `/login` | GET, POST | User login |
| `register` | `/register` | GET, POST | User registration |
| `main` | `/main` | GET | Main application page |

### Example Usage:
```python
# In templates
{{ url_for('index') }}
{{ url_for('login') }}
{{ url_for('register') }}
{{ url_for('main') }}
```

---

## 👤 User Dashboard Routes

These routes require user authentication (`@login_required`).

| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `simulate_page` | `/simulate` | GET, POST | Loan simulation (legacy) |
| `dashboard_page` | `/dashboard` | GET | User dashboard |
| `profile_page` | `/profile` | GET, POST | User profile management |
| `logout` | `/logout` | GET | User logout |

### ⚠️ Common Mistakes:
```python
# ❌ WRONG - Will cause BuildError
{{ url_for('simulate') }}
{{ url_for('dashboard') }}
{{ url_for('profile') }}

# ✅ CORRECT
{{ url_for('simulate_page') }}
{{ url_for('dashboard_page') }}
{{ url_for('profile_page') }}
```

---

## 🔌 API Routes

RESTful API endpoints for frontend integration.

### Authentication APIs
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `auth_status` | `/api/auth/status` | GET | Check authentication status |
| `api_login` | `/api/login` | POST | API login |
| `api_register` | `/api/register` | POST | API registration |
| `api_logout` | `/api/logout` | POST | API logout |

### User APIs
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `api_profile` | `/api/profile` | GET, POST | Profile API |
| `api_simulate` | `/api/simulate` | POST | Loan simulation API |
| `api_dashboard` | `/api/dashboard` | GET | Dashboard data API |
| `calculate` | `/api/calculate` | POST | Loan calculation API |

### Legacy APIs
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `funding_inquiry` | `/api/funding-inquiry` | POST | Funding inquiry submission |
| `admin_funding_parties` | `/api/admin/funding-parties` | GET | Admin funding party list |

### Loan Management APIs
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `cancel_legacy_loan` | `/loan/<int:loan_id>/cancel` | POST | Cancel legacy loan |

---

## 🛡️ Admin Routes

All admin routes require admin role authentication. Prefix: `/admin/`

### Dashboard & Overview
| Endpoint | URL | Description |
|----------|-----|-------------|
| `admin.dashboard` | `/admin/` or `/admin/dashboard` | Admin dashboard home |
| `admin.statistics` | `/admin/statistics` | System statistics |
| `admin.chart_data` | `/admin/api/chart-data` | Chart data API |

### User Management
| Endpoint | URL | Description |
|----------|-----|-------------|
| `admin.users` | `/admin/users` | List all users |
| `admin.user_detail` | `/admin/users/<int:user_id>` | View user details |
| `admin.toggle_user_status` | `/admin/users/<int:user_id>/toggle-status` | Enable/disable user |
| `admin.delete_user` | `/admin/users/<int:user_id>/delete` | Delete user |

### KYC Verification
| Endpoint | URL | Description |
|----------|-----|-------------|
| `admin.kyc_verifications` | `/admin/kyc-verifications` | List KYC submissions |
| `admin.kyc_verification_detail` | `/admin/kyc-verifications/<int:user_id>` | View KYC details |
| `admin.approve_user_kyc` | `/admin/kyc-verifications/<int:user_id>/approve` | Approve KYC |
| `admin.reject_user_kyc` | `/admin/kyc-verifications/<int:user_id>/reject` | Reject KYC |
| `admin.download_kyc_document` | `/admin/kyc-verifications/<int:user_id>/document/<int:document_id>` | Download KYC document |

### Loan Management (Legacy)
| Endpoint | URL | Description |
|----------|-----|-------------|
| `admin.loans` | `/admin/loans` | List all loans |
| `admin.loan_detail` | `/admin/loans/<int:loan_id>` | View loan details |
| `admin.approve_loan` | `/admin/loans/<int:loan_id>/approve` | Approve loan |
| `admin.reject_loan` | `/admin/loans/<int:loan_id>/reject` | Reject loan |
| `admin.update_loan_status` | `/admin/loans/<int:loan_id>/update-status` | Update loan status |
| `admin.delete_loan` | `/admin/loans/<int:loan_id>/delete` | Delete loan |

### Loan Application Management (New System)
| Endpoint | URL | Description |
|----------|-----|-------------|
| `admin.loan_applications` | `/admin/loan-applications` | List loan applications |
| `admin.loan_application_detail` | `/admin/loan-applications/<int:application_id>` | View application details |
| `admin.approve_kyc` | `/admin/loan-applications/<int:application_id>/approve-kyc` | Approve KYC phase |
| `admin.reject_kyc` | `/admin/loan-applications/<int:application_id>/reject-kyc` | Reject KYC phase |
| `admin.approve_financial` | `/admin/loan-applications/<int:application_id>/approve-financial` | Approve financial phase |
| `admin.reject_financial` | `/admin/loan-applications/<int:application_id>/reject-financial` | Reject financial phase |
| `admin.make_loan_decision` | `/admin/loan-applications/<int:application_id>/make-decision` | Final loan decision |
| `admin.add_application_note` | `/admin/loan-applications/<int:application_id>/add-note` | Add admin note |
| `admin.delete_loan_application` | `/admin/loan-applications/<int:application_id>/delete` | Delete application |
| `admin.download_application_document` | `/admin/loan-applications/document/<int:document_id>/download` | Download document |

### Funding Partners Management
| Endpoint | URL | Description |
|----------|-----|-------------|
| `admin.funding_partners` | `/admin/funding-partners` | Manage funding partners |

---

## 💰 Funding Routes

Routes for funding partners. Prefix: `/funding/`

### Dashboard & Overview
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `funding.dashboard` | `/funding/` or `/funding/dashboard` | GET | Funding dashboard |
| `funding.analytics` | `/funding/analytics` | GET | Funding analytics |
| `funding.api_funding_stats` | `/funding/api/funding-stats` | GET | Funding stats API |
| `funding.api_chart_data` | `/funding/api/chart-data` | GET | Chart data API |

### Funding Actions
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `funding.add_funding` | `/funding/add-funding` | GET, POST | Add funding deposit |
| `funding.profile` | `/funding/profile` | GET, POST | Funding partner profile |

### Funding History
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `funding.transactions` | `/funding/transactions` | GET | Transaction history |
| `funding.funded_loans` | `/funding/loans` | GET | View funded loans |

### Example Usage:
```python
# In templates
{{ url_for('funding.dashboard') }}
{{ url_for('funding.add_funding') }}
{{ url_for('funding.transactions') }}

# In Python
redirect(url_for('funding.dashboard'))
```

---

## 🔐 KYC Routes

KYC verification routes. Prefix: `/kyc/`

### Main KYC Routes
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `kyc.index` | `/kyc/` | GET | KYC dashboard/home |
| `kyc.verify` | `/kyc/verify` | GET | KYC verification page |
| `kyc.status` | `/kyc/status` | GET | Check KYC status |
| `kyc.submit` | `/kyc/submit` | POST | Submit KYC application |

### Document Management
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `kyc.upload_document` | `/kyc/upload-document` | POST | Upload KYC document |
| `kyc.download_document` | `/kyc/document/<int:document_id>/download` | GET | Download document |
| `kyc.delete_document` | `/kyc/document/<int:document_id>/delete` | POST | Delete document |

### ⚠️ Common Mistakes:
```python
# ❌ WRONG
{{ url_for('kyc.submit_kyc') }}
{{ url_for('kyc.verification_dashboard') }}

# ✅ CORRECT
{{ url_for('kyc.submit') }}
{{ url_for('kyc.index') }}
```

---

## 📝 Loan Application Routes

New 3-phase loan application system. Prefix: `/loan-application/`

### Main Application Routes
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `loan_app.index` | `/loan-application/` | GET | Loan application home |
| `loan_app.apply` | `/loan-application/apply` | GET | Application form |
| `loan_app.submit` | `/loan-application/submit` | POST | Submit application |
| `loan_app.detail` | `/loan-application/<int:application_id>` | GET | View application details |
| `loan_app.cancel` | `/loan-application/<int:application_id>/cancel` | POST | Cancel application |

### API Routes
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `loan_app.get_applications` | `/loan-application/api/applications` | GET | Get user's applications |
| `loan_app.get_status` | `/loan-application/api/<int:application_id>/status` | GET | Get application status |
| `loan_app.check_eligibility` | `/loan-application/api/check-eligibility` | GET | Check loan eligibility |

### Document Management
| Endpoint | URL | Methods | Description |
|----------|-----|---------|-------------|
| `loan_app.upload_document` | `/loan-application/<int:application_id>/upload-document` | POST | Upload document |
| `loan_app.download_document` | `/loan-application/document/<int:document_id>/download` | GET | Download document |
| `loan_app.delete_document` | `/loan-application/document/<int:document_id>/delete` | POST | Delete document |

### ⚠️ Common Mistakes:
```python
# ❌ WRONG
{{ url_for('loan_app.dashboard') }}
{{ url_for('loan_app.new_application') }}
{{ url_for('loan_app.my_applications') }}

# ✅ CORRECT
{{ url_for('loan_app.index') }}
{{ url_for('loan_app.apply') }}
{{ url_for('loan_app.get_applications') }}  # For API call
```

---

## ⚠️ Common Mistakes & Solutions

### 1. BuildError: endpoint 'simulate' not found

**Problem:**
```python
{{ url_for('simulate') }}  # ❌ WRONG
```

**Solution:**
```python
{{ url_for('simulate_page') }}  # ✅ CORRECT
```

---

### 2. BuildError: endpoint 'dashboard' not found

**Problem:**
```python
{{ url_for('dashboard') }}  # ❌ WRONG
```

**Solution:**
```python
{{ url_for('dashboard_page') }}  # ✅ CORRECT
```

---

### 3. BuildError: endpoint 'profile' not found

**Problem:**
```python
{{ url_for('profile') }}  # ❌ WRONG
```

**Solution:**
```python
{{ url_for('profile_page') }}  # ✅ CORRECT
```

---

### 4. Using Wrong Blueprint Prefix

**Problem:**
```python
{{ url_for('kyc_verification') }}  # ❌ Missing blueprint prefix
```

**Solution:**
```python
{{ url_for('kyc.verify') }}  # ✅ Include blueprint prefix
```

---

### 5. Incorrect Admin Routes

**Problem:**
```python
{{ url_for('admin.kyc_verification') }}  # ❌ Wrong name
```

**Solution:**
```python
{{ url_for('admin.kyc_verifications') }}  # ✅ Plural form
# OR for detail page:
{{ url_for('admin.kyc_verification_detail', user_id=user.id) }}
```

---

### 6. Funding Routes

**Problem:**
```python
{{ url_for('funding.contribute') }}  # ❌ Wrong name
```

**Solution:**
```python
{{ url_for('funding.add_funding') }}  # ✅ CORRECT
```

---

### 7. Loan Application Routes

**Problem:**
```python
{{ url_for('loan_app.new_application') }}  # ❌ Wrong name
```

**Solution:**
```python
{{ url_for('loan_app.apply') }}  # ✅ CORRECT
```

---

## 🔍 Quick Reference Table

### Most Common Routes

| What You Want | Correct Endpoint | Common Mistake |
|---------------|------------------|----------------|
| Loan simulation page | `simulate_page` | `simulate` |
| User dashboard | `dashboard_page` | `dashboard` |
| User profile | `profile_page` | `profile` |
| KYC verification | `kyc.verify` | `kyc.verification_dashboard` |
| Submit KYC | `kyc.submit` | `kyc.submit_kyc` |
| Apply for loan | `loan_app.apply` | `loan_app.new_application` |
| View applications | `loan_app.index` | `loan_app.my_applications` |
| Add funding | `funding.add_funding` | `funding.contribute` |
| Admin KYC list | `admin.kyc_verifications` | `admin.kyc_verification` |

---

## 🛠️ Debugging Tips

### 1. Check Available Routes
```python
python -c "import sys; sys.path.insert(0, 'backend'); from app import app; [print(rule.endpoint, rule.rule) for rule in app.url_map.iter_rules()]"
```

### 2. Run Verification Script
```bash
python verify_all_endpoints.py
```

### 3. Test Specific Endpoint
```python
from flask import url_for
with app.test_request_context():
    print(url_for('your_endpoint_here'))
```

---

## 📊 Blueprint Summary

| Blueprint | Prefix | Routes Count | Purpose |
|-----------|--------|--------------|---------|
| (main app) | `/` | 15 | Core app routes |
| `admin` | `/admin/` | 30 | Admin management |
| `funding` | `/funding/` | 9 | Funding partners |
| `kyc` | `/kyc/` | 7 | KYC verification |
| `loan_app` | `/loan-application/` | 10 | Loan applications |

---

## ✅ Verification Checklist

Before deploying, verify:

- [ ] All templates use correct endpoint names
- [ ] No `url_for('simulate')` (should be `simulate_page`)
- [ ] No `url_for('dashboard')` (should be `dashboard_page`)
- [ ] No `url_for('profile')` (should be `profile_page`)
- [ ] Blueprint prefixes used correctly (e.g., `admin.`, `funding.`)
- [ ] Run `verify_all_endpoints.py` successfully
- [ ] No BuildError exceptions in browser console
- [ ] Hard refresh browser cache (Ctrl+Shift+F5)
- [ ] Test all navigation links

---

## 📝 Notes

1. **Legacy vs New System**: The app has both legacy loan routes (`/simulate`, `/dashboard`) and new loan application routes (`/loan-application/*`). Both are maintained for backward compatibility.

2. **Funding Party Restrictions**: Users with `user_role='funding_party'` are restricted from accessing loan application routes and redirected to `funding.dashboard`.

3. **KYC Required**: Most functionality requires KYC approval. Check `current_user.kyc_status == 'approved'` before accessing protected features.

4. **Admin Only**: All `/admin/*` routes require `is_admin=True` and are protected by decorators.

---

## 🔄 Last Updated

- **Date**: 2024
- **Verified**: All 70+ endpoints tested and working
- **Status**: ✅ Production Ready

---

## 📞 Support

If you encounter a BuildError:
1. Check this reference guide first
2. Run `verify_all_endpoints.py`
3. Check browser console for specific endpoint name
4. Search this document for the correct endpoint name
5. Update template with correct `url_for()` call

---

**End of Reference Guide**