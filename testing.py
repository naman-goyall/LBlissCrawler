import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import json
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from PIL import Image, ImageGrab
from io import BytesIO
import re

# Website Details
login_url = "https://leelabliss.org"
videos_url = "https://leelabliss.org/liveimagevideo.aspx"

load_dotenv()
# Login credentials for the website
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Email Credentials
email_sender = os.getenv("MY_EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")
email_recipient = os.getenv("MY_EMAIL")


def get_vimeo_thumbnail(video_url):
    try:
        # Extract video ID from URL using regex pattern
        match = re.search(r'(vimeo\.com\/|player\.vimeo\.com\/video\/)(\d+)', video_url)
        if not match:
            print(f"No Vimeo video ID found in URL: {video_url}")
            return None
            
        video_id = match.group(2)
        
        # First try using a direct thumbnail URL (most reliable)
        thumbnail_url = f"https://i.vimeocdn.com/video/{video_id}_640.jpg"
        
        # For hosting in email, we'll save it locally
        screenshot_path = f"thumbnail_{video_id}.png"
        
        # If we already have this thumbnail, return it
        if os.path.exists(screenshot_path):
            print(f"✅ Using existing thumbnail: {screenshot_path}")
            return screenshot_path
        
        # Otherwise, try to get it from vimeocdn
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Try to load the thumbnail directly
                page.goto(thumbnail_url, timeout=10000)
                
                # Take a screenshot of the entire page
                page.screenshot(path=screenshot_path)
                browser.close()
                
                print(f"✅ Thumbnail saved to {screenshot_path}")
                return screenshot_path
                
        except Exception as e:
            print(f"❌ Failed to get thumbnail from vimeocdn: {e}")
            
            # If direct thumbnail fails, use a default image
            # This is better than sending no image
            default_image_path = "default_thumbnail.png"
            if not os.path.exists(default_image_path):
                # Create a simple default image
                img = Image.new('RGB', (640, 360), color=(73, 109, 137))
                img.save(default_image_path)
                
            print(f"✅ Using default thumbnail")
            return default_image_path

    except Exception as e:
        print(f"❌ Failed to get thumbnail: {e}")
        return None



# Function to send email notifications
def send_email_notification(subject, message, video_url=None):
    try:
        # Read the CSS and HTML templates
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        with open(os.path.join(templates_dir, 'email_styles.css'), 'r') as f:
            css_styles = f.read()
        
        with open(os.path.join(templates_dir, 'email_template.html'), 'r') as f:
            html_template = f.read()

        # If no video URL is provided, use a simpler template without video section
        if not video_url:
            html_template = html_template.replace(
                '<!-- Video Thumbnail -->', ''
            ).replace(
                '<!-- Call to Action Button -->', ''
            )

        # Format the HTML with the provided content
        html = html_template.format(
            styles=css_styles,
            message=message,
            video_url=video_url,
            year=2025
        )

        # Create message container
        msg = MIMEMultipart('alternative')
        msg['From'] = email_sender
        msg['To'] = email_recipient
        msg['Subject'] = subject

        # Attach the HTML content to the message
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)

        # Attach the static image if available
        static_image_path = "/Users/namangoyal/Documents/GitHub/LBlissCrawler/IMG_6792.JPG"
        if os.path.exists(static_image_path):
            with open(static_image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', '<video_thumbnail>')
                image.add_header('Content-Disposition', 'inline', filename="thumbnail.jpg")
                msg.attach(image)
                print(f"✅ Attached static image thumbnail")
        else:
            print(f"❌ Static image file not found: {static_image_path}")
            
        # Attach the logo image if available
        logo_path = "/Users/namangoyal/Documents/GitHub/LBlissCrawler/images.jpg"
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as logo_file:
                logo_data = logo_file.read()
                logo = MIMEImage(logo_data)
                logo.add_header('Content-ID', '<logo>')
                logo.add_header('Content-Disposition', 'inline', filename="logo.jpg")
                msg.attach(logo)
                print(f"✅ Attached logo image")
        else:
            print(f"❌ Logo file not found: {logo_path}")

        # Connect to SMTP and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            recipients = [email_recipient]
            server.sendmail(email_sender, recipients, msg.as_string())

        print("✅ Email sent successfully with video thumbnail!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# Function to log in and scrape the website
def login_and_scrape():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()
            
            # Navigate to login page
            page.goto(login_url)
            
            # Login process
            page.fill("#txtUserId", username)
            page.fill("#txtPassword", password)
            page.click("#btnLogin")
            
            # Wait for the dashboard to load
            page.wait_for_selector(".labelt")
            
            # Navigate to the videos page
            page.goto(videos_url)
            
            video_title = None
            video_url = None
            
            try:
                # First try extracting the video URL from an iframe
                iframe_element = page.query_selector("iframe")
                if iframe_element:
                    video_url = iframe_element.get_attribute("src")
                    print(f"Extracted video URL from iframe: {video_url}")
                    
                    # Extract video title from the page
                    video_title_element = page.query_selector(".labelt")
                    if video_title_element:
                        video_title = video_title_element.inner_text().strip()
                        print(f"✅ Latest Video Title: {video_title}")
                        print(f"✅ Video URL: {video_url}")
                    
            except Exception as e:
                print(f"Failed to extract video URL from iframe: {e}")
                
                try:
                    # Fallback to extracting from the parent element
                    latest_video_element = page.query_selector(".labelt")
                    if latest_video_element:
                        video_title = latest_video_element.inner_text().strip()
                        video_url_element = page.query_selector(".labelt >> xpath=..")
                        if video_url_element:
                            video_url = video_url_element.get_attribute("href")
                            print(f"Extracted video URL from fallback method: {video_url}")
                
                except Exception as e:
                    print(f"Failed to extract video URL from fallback method: {e}")
            
            browser.close()
            
            if video_url and video_title:
                return {"title": video_title, "url": video_url}
            else:
                print("❌ No video found.")
                return None
                
    except Exception as e:
        print(f"❌ Login and scrape failed: {e}")
        return None


# Function to check for new videos and send email
def check_for_new_video():
    latest_video = login_and_scrape()

    # Load last saved video data
    if os.path.exists("latest_video.json"):
        with open("latest_video.json", "r") as file:
            last_video = json.load(file)
    else:
        last_video = {}

    # Check if a new video is found
    if latest_video and latest_video != last_video:
        print(f"New video found: {latest_video['title']}")

        # Save new video details
        with open("latest_video.json", "w") as file:
            json.dump(latest_video, file)

        # Send email with video link
        subject = "New Video Posted on Leelabliss"
        message = latest_video['title']
        send_email_notification(subject, message, latest_video['url'])
    else:
        print("No new video found.")

# Run the script
if __name__ == "__main__":
    check_for_new_video()
