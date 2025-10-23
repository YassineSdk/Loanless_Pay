import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from models import Payment, User, Advance
from app import db
import os

class EmailReminder:
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None):
        """
        Initialize the email reminder system.
        
        Args:
            smtp_server (str): SMTP server address
            smtp_port (int): SMTP server port
            username (str): SMTP username
            password (str): SMTP password
        """
        # Use provided credentials or environment variables
        self.smtp_server = smtp_server or os.environ.get('SMTP_SERVER', 'smtp.example.com')
        self.smtp_port = smtp_port or int(os.environ.get('SMTP_PORT', 587))
        self.username = username or os.environ.get('SMTP_USERNAME', 'notifications@loanlesspay.com')
        self.password = password or os.environ.get('SMTP_PASSWORD', 'password')
    
    def send_email(self, recipient, subject, message):
        """
        Send an email to a recipient.
        
        Args:
            recipient (str): Recipient email address
            subject (str): Email subject
            message (str): Email message (HTML)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = recipient
            
            # Attach HTML message
            html_part = MIMEText(message, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_payment_reminder(self, payment, user, advance):
        """
        Send a payment reminder email.
        
        Args:
            payment (Payment): Payment object
            user (User): User object
            advance (Advance): Advance object
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        subject = f"Payment Reminder: ${payment.amount:.2f} due on {payment.due_date.strftime('%Y-%m-%d')}"
        
        message = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}
                .content {{ padding: 20px; }}
                .footer {{ background-color: #f1f1f1; padding: 10px; text-align: center; font-size: 12px; }}
                .button {{ background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>LoanlessPay Payment Reminder</h2>
                </div>
                <div class="content">
                    <p>Dear {user.first_name} {user.last_name},</p>
                    <p>This is a friendly reminder that your payment of <strong>${payment.amount:.2f}</strong> is due on <strong>{payment.due_date.strftime('%Y-%m-%d')}</strong>.</p>
                    <p>Payment details:</p>
                    <ul>
                        <li>Advance ID: {advance.id}</li>
                        <li>Payment Number: {payment.id}</li>
                        <li>Amount Due: ${payment.amount:.2f}</li>
                        <li>Due Date: {payment.due_date.strftime('%Y-%m-%d')}</li>
                    </ul>
                    <p>Please ensure your payment is made on time to maintain your good standing.</p>
                    <p>Thank you for choosing LoanlessPay for your financial needs.</p>
                    <p><a href="http://localhost:5000/dashboard" class="button">View Your Dashboard</a></p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email.</p>
                    <p>&copy; {datetime.now().year} LoanlessPay. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user.email, subject, message)
    
    def check_upcoming_payments(self, days_before=3):
        """
        Check for upcoming payments and send reminders.
        
        Args:
            days_before (int): Number of days before due date to send reminder
            
        Returns:
            int: Number of reminders sent
        """
        # Calculate the target date
        target_date = datetime.now() + timedelta(days=days_before)
        
        # Find payments due on the target date that haven't had reminders sent
        upcoming_payments = Payment.query.filter(
            Payment.due_date >= target_date,
            Payment.due_date < target_date + timedelta(days=1),
            Payment.status == 'pending',
            Payment.reminder_sent == False
        ).all()
        
        reminders_sent = 0
        
        for payment in upcoming_payments:
            advance = Advance.query.get(payment.advance_id)
            user = User.query.get(advance.user_id)
            
            if self.send_payment_reminder(payment, user, advance):
                payment.reminder_sent = True
                db.session.commit()
                reminders_sent += 1
        
        return reminders_sent

def send_overdue_reminders():
    """
    Send reminders for overdue payments.
    
    Returns:
        int: Number of reminders sent
    """
    reminder = EmailReminder()
    
    # Find overdue payments
    overdue_payments = Payment.query.filter(
        Payment.due_date < datetime.now(),
        Payment.status == 'pending'
    ).all()
    
    reminders_sent = 0
    
    for payment in overdue_payments:
        advance = Advance.query.get(payment.advance_id)
        user = User.query.get(advance.user_id)
        
        subject = f"OVERDUE Payment: ${payment.amount:.2f} was due on {payment.due_date.strftime('%Y-%m-%d')}"
        
        message = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f44336; color: white; padding: 10px; text-align: center; }}
                .content {{ padding: 20px; }}
                .footer {{ background-color: #f1f1f1; padding: 10px; text-align: center; font-size: 12px; }}
                .button {{ background-color: #f44336; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>OVERDUE Payment Notice</h2>
                </div>
                <div class="content">
                    <p>Dear {user.first_name} {user.last_name},</p>
                    <p>Your payment of <strong>${payment.amount:.2f}</strong> was due on <strong>{payment.due_date.strftime('%Y-%m-%d')}</strong> and is now overdue.</p>
                    <p>Please make your payment as soon as possible to avoid any further issues.</p>
                    <p>Payment details:</p>
                    <ul>
                        <li>Advance ID: {advance.id}</li>
                        <li>Payment Number: {payment.id}</li>
                        <li>Amount Due: ${payment.amount:.2f}</li>
                        <li>Due Date: {payment.due_date.strftime('%Y-%m-%d')}</li>
                        <li>Days Overdue: {(datetime.now() - payment.due_date).days}</li>
                    </ul>
                    <p><a href="http://localhost:5000/dashboard" class="button">Make Payment Now</a></p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email.</p>
                    <p>&copy; {datetime.now().year} LoanlessPay. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        if reminder.send_email(user.email, subject, message):
            reminders_sent += 1
    
    return reminders_sent