### README.md

# LBlissCrawler

## Introduction

**LBlissCrawler** is a Python script designed to automate the process of logging into the [Leela Bliss](https://leelabliss.org) website, scraping information about the latest videos, and sending email notifications if a new video is detected. This tool ensures that users are kept up-to-date with new content as it is published on the site.

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

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/LBlissCrawler.git
   cd LBlissCrawler
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory:
     ```plaintext
     USERNAME=your-leela-bliss-username
     PASSWORD=your-leela-bliss-password
     EMAIL_PASSWORD=your-email-password
     ```
   - Replace placeholders with actual credentials.

---

## Usage

1. **Run the Script Manually**:
   ```bash
   python LBlissCrawler.py
   ```

2. **Automate Using Cron Job** (explained below).

---

## Features

- Logs into the Leela Bliss website.
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
     USERNAME=your-leela-bliss-username
     PASSWORD=your-leela-bliss-password
     EMAIL_PASSWORD=your-email-password
     MY_EMAIL=you-email-address
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
     0 * * * * /usr/bin/python3 /path/to/LBlissCrawler.py
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
