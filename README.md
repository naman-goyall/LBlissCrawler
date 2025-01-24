### README.md

# Video Scraper & Notification Script

## Introduction

This Python script logs into the specified website, scrapes information about the latest video available, and sends email notifications if a new video is detected. The script uses Selenium for web scraping, `smtplib` for email notifications, and stores data in a JSON file to keep track of the last fetched video.

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Dependencies](#dependencies)
5. [Configuration](#configuration)
6. [Setting Up ChromeDriver](#setting-up-chromedriver)
7. [Creating a Cron Job](#creating-a-cron-job)
8. [Troubleshooting](#troubleshooting)
9. [Contributors](#contributors)
10. [License](#license)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up the `.env` file:
   - Create a `.env` file in the root directory:
     ```plaintext
     USERNAME=your-website-username
     PASSWORD=your-website-password
     EMAIL_PASSWORD=your-email-password
     ```
   - Replace the placeholder values with actual credentials.

---

## Usage

1. Run the script manually:
   ```bash
   python script_name.py
   ```

2. Automate the script using a cron job (explained below).

---

## Features

- Logs into the specified website.
- Scrapes the latest video information.
- Compares with the previously saved video data.
- Sends email notifications if a new video is detected.
- Stores data locally in `latest_video.json`.

---

## Dependencies

The script relies on the following libraries:

- `smtplib`
- `email`
- `requests`
- `beautifulsoup4`
- `selenium`
- `python-dotenv`
- `json`
- `os`
- `time`

To install the required Python packages:
```bash
pip install -r requirements.txt
```

---

## Configuration

1. **Environment Variables**:
   - The `.env` file should contain:
     ```plaintext
     USERNAME=your-website-username
     PASSWORD=your-website-password
     EMAIL_PASSWORD=your-email-password
     ```

2. **Email Settings**:
   - Update `email_sender` and `email_recipient` in the script:
     ```python
     email_sender = "your-email@gmail.com"
     email_recipient = "recipient-email@gmail.com"
     ```

3. **ChromeDriver Path**:
   - Update the `driver_path` variable with the absolute path to your ChromeDriver.

---

## Setting Up ChromeDriver

1. **Download ChromeDriver**:
   - Visit the [ChromeDriver downloads page](https://sites.google.com/chromium.org/driver/) and download the version that matches your Chrome browser version.

2. **Find Chrome Version**:
   - Open Chrome, go to `chrome://settings/help`, and note the version.

3. **Place ChromeDriver**:
   - Place the downloaded `chromedriver` binary in a suitable directory (e.g., `/usr/local/bin` or any custom directory).

4. **Update the Path**:
   - Set the `driver_path` variable in the script:
     ```python
     driver_path = "/path/to/chromedriver"
     ```

5. **Make Executable**:
   - Ensure ChromeDriver is executable:
     ```bash
     chmod +x /path/to/chromedriver
     ```

---

## Creating a Cron Job

To automate the script:

1. **Edit the Cron Table**:
   ```bash
   crontab -e
   ```

2. **Add the Job**:
   - Add the following line to run the script every hour:
     ```bash
     0 * * * * /usr/bin/python3 /path/to/script_name.py
     ```
   - Adjust the path to your Python interpreter and script.

3. **Save the Cron Job**:
   - Save and exit. The script will now run on the specified schedule.

---

## Troubleshooting

1. **Common Issues**:
   - **Invalid Login Credentials**: Ensure the `.env` file contains valid credentials.
   - **Incorrect ChromeDriver Version**: Ensure ChromeDriver matches your browser version.
   - **Email Not Sending**: Verify that the SMTP credentials are correct.

2. **Debugging**:
   - Run the script in verbose mode (e.g., remove `--headless` from Chrome options).
   - Check `latest_video.json` for saved data.

---

## Contributors

- **Naman Goyal**: Developer of the script.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
