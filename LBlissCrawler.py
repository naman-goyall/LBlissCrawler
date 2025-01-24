import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# Selenium and Website Details
driver_path = '/Users/namangoyal/Desktop/LBlissCrawler/chromedriver-mac-arm64/chromedriver'  # Replace with your path
login_url = "https://leelabliss.org"
videos_url = "https://leelabliss.org/liveimagevideo.aspx"

load_dotenv()
# Login credentials for the website
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Email Credentials
email_sender = "namangoyal1008@gmail.com"
email_password = os.getenv("EMAIL_PASSWORD")
email_recipient = "namangoyal1008@gmail.com"

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

# Function to log in and scrape the website
def login_and_scrape():
    # Initialize the Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Recommended for headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # Fix potential resource issues
    chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering (optional)
    chrome_options.add_argument("--window-size=1920x1080")  # Optional: Set a virtual screen size

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(login_url)

    # Login process
    driver.find_element(By.ID, "txtUserId").send_keys(username)  # Replace with actual ID
    driver.find_element(By.ID, "txtPassword").send_keys(password)  # Replace with actual ID
    driver.find_element(By.ID, "btnLogin").click()  # Replace with actual ID

    # Wait for the videos page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "labelt"))  # Adjust class name
    )

    # Navigate to the videos page
    driver.get(videos_url)

    # Wait for the video title to appear
    latest_video_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "labelt"))  # Replace with actual class
    )

    # Extract the text of the element
    video_title = latest_video_element.text.strip()
    print("Latest Video Title:", video_title)

    # Find the parent element containing the video URL
    video_url_element = latest_video_element.find_element(By.XPATH, "..")  # Navigate to the parent link if needed
    video_url = video_url_element.get_attribute("href")
    print("Video URL:", video_url)

    # Quit the driver
    driver.quit()

    # Return the extracted details
    return {"title": video_title, "url": "https://leelabliss.org"}

# Compare with the last fetched video and send email if there's a new one
def check_for_new_video():
    latest_video = login_and_scrape()

    # Load the previously saved video data
    if os.path.exists("latest_video.json"):
        with open("latest_video.json", "r") as file:
            last_video = json.load(file)
    else:
        last_video = {}

    # Compare and notify if a new video is found
    if latest_video != last_video:
        print(f"New video found: {latest_video['title']}")
        # Save the new video details
        with open("latest_video.json", "w") as file:
            json.dump(latest_video, file)

        # Send an email notification
        subject = "New Video Posted on Rasik.org"
        message = f"Title: {latest_video['title']}\nURL: {latest_video['url']}"
        send_email_notification(subject, message)
    else:
        print("No new video found.")

# Run the script
if __name__ == "__main__":
    check_for_new_video()

