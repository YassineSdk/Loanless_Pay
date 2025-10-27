# Loanless Setup Instructions

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**

   ```bash
   python app.py
   ```

   The application will start on `http://localhost:5000`

3. **Access the Application**

   Open your web browser and navigate to: `http://localhost:5000`

## Demo User Credentials

For quick testing, a demo user has been created:

- **Username:** demo
- **Password:** demo123

## Application Structure

```
loanless/
├── app.py              # Main Flask application
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── database.db         # SQLite database (created automatically)
├── templates/          # HTML templates
│   ├── login.html
│   ├── main.html
│   ├── simulate.html
│   └── dashboard.html
└── static/
    └── css/
        └── style.css   # Custom styles
```

## Features

1. **Login/Register Page**: User authentication with password hashing
2. **Main Page**: Hero section with top loan offers
3. **Loan Simulation**: Calculate loan payments with 2% commission
4. **Dashboard**: View and manage your loan subscriptions

## Notes

- The database is SQLite and will be created automatically on first run
- All passwords are securely hashed using Werkzeug
- The app uses Bootstrap 5 for responsive design
- Styling uses the Poppins font with green (#2ECC71) and white color scheme

