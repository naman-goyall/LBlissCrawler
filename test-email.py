import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()   

# Email Credentials
email_sender = os.getenv("MY_EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")
email_recipient = os.getenv("MY_EMAIL")


def send_email_notification(subject, message, image_url=None):
    try:
        # Set up the email content
        msg = MIMEMultipart('related')  # 'related' allows inline images
        msg['From'] = email_sender
        msg['To'] = email_recipient
        msg['Subject'] = subject

        # Create HTML content with an embedded image
        html = f"""
        <html>
            <body>
                <p>{message}</p>
                {"<br><img src='cid:image1' width='500'>" if image_url else ""}
            </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        # Attach an image if provided
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                img_data = response.content
                image = MIMEImage(img_data)
                image.add_header('Content-ID', '<image1>')
                image.add_header('Content-Disposition', 'inline', filename='video_thumbnail.jpg')
                msg.attach(image)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_recipient, msg.as_string())
            server.sendmail(email_sender, "eashan.sinha@gmail.com", msg.as_string())
            server.sendmail(email_sender, "udgam.goyal10@gmail.com", msg.as_string())
            server.sendmail(email_sender, "ritikagehani1107@gmail.com", msg.as_string())
            server.sendmail(email_sender, "tanvishanbhag01@gmail.com", msg.as_string())
            server.sendmail(email_sender, "shelly.soumya@gmail.com", msg.as_string())

        print("Email sent successfully with inline image!")
    except Exception as e:
        print(f"Failed to send email: {e}")
