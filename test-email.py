import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()   

# Email Credentials
email_sender = os.getenv("MY_EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")
email_recipient = os.getenv("MY_EMAIL")

# Function to send email notifications
def send_email_notification(subject, message):
    try:
        # Set up the email content
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use Gmail's SMTP server
            server.starttls()  # Secure the connection
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_recipient, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

send_email_notification("Test Email", "This is a test email.")