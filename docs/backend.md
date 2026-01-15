# Backend Documentation

## Overview

Flask-based backend for the LoanLess microloan platform with 3-phase loan processing, admin management, and funding partner integration.

## Architecture

### Tech Stack
- **Framework**: Flask 3.x
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Security**: Werkzeug password hashing

### Key Components

```
backend/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── admin.py               # Admin routes
├── loan_application.py    # Loan processing
├── funding.py             # Funding partner routes
├── kyc_verification.py    # KYC routes
├── decorators.py          # Security decorators
└── requirements.txt       # Dependencies
```

## Models

### User
- Authentication and profile management
- Roles: user, admin, funding_party
- KYC status tracking

### LoanApplication
- 3-phase workflow: KYC → Financial → Decision
- Document attachments
- Status tracking and approvals

### FundingTransaction
- Investment tracking for funding partners
- Deposit/withdrawal management

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - Session termination

### Loan Processing
- `GET /loan-application/apply` - Application form
- `POST /loan-application/submit` - Submit application
- `GET /loan-application/<id>` - View application
- `POST /admin/loan-applications/<id>/approve-kyc` - Approve KYC
- `POST /admin/loan-applications/<id>/approve-financial` - Approve financial
- `POST /admin/loan-applications/<id>/make-decision` - Final decision

### Admin Management
- `GET /admin/dashboard` - Admin overview
- `GET /admin/loan-applications` - All applications
- `GET /admin/users` - User management
- `GET /admin/funding-partners` - Partner management

### Funding Partner
- `GET /funding/dashboard` - Investment overview
- `POST /funding/add-funding` - Add investment
- `GET /funding/transactions` - Transaction history

## Security

### Authentication
- Password hashing with Werkzeug
- Session-based authentication via Flask-Login
- Role-based access control decorators

### File Security
- Upload validation (type, size)
- Secure filename generation
- User ownership verification

### Data Protection
- SQL injection prevention (SQLAlchemy ORM)
- Input sanitization
- CSRF protection

## Database Schema

### Core Tables
- `users` - User accounts and profiles
- `loan_applications` - 3-phase loan processing
- `loan_documents` - File attachments
- `admin_reviews` - Admin action history
- `funding_transactions` - Investment tracking

## Development

### Setup
```bash
pip install -r requirements.txt
python app.py
```

### Testing
```bash
python test_loan_app_buttons.py  # Button functionality
python test_filters.py           # Filter testing
```

### Database Reset
```bash
python reset_database.py        # Interactive reset
python clear_db_quick.py        # Quick reset
```

## Configuration

### Environment Variables
- `FLASK_ENV` - Environment (development/production)
- `SECRET_KEY` - Session encryption key
- `UPLOAD_FOLDER` - File upload directory

### Production Settings
- Debug mode disabled
- Secure session cookies
- Database connection pooling
- File upload limits enforced

## Error Handling

### HTTP Status Codes
- `200` - Success
- `302` - Redirect (successful actions)
- `403` - Access forbidden
- `404` - Resource not found
- `500` - Server error

### Logging
- Application errors logged
- User actions tracked
- Admin review history maintained