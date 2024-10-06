# URL-Shortener
## Overview
URL Shortener is a Flask based application designed to allow users to create short, customisable URLs and generate QR codes for easy sharing and access. This application also includes features such as URL management and monitoring, user accounts for long term access, browser sessions for temporary tracking and Google Safe Browsing integration to ensure the safety of all URLS. This project provides a secure and efficient way to manage and share links.

## Features
- **Customised Links:**
  - **Custom Short Links:** Create personalised short URLs.
  - **Expiration Dates:** Set custom expiration dates, with a default of 30 days.
  - **Click Limits:** Limit the number of times a link can be accessed.
  - **Password Protection:** Secure short URLs with passwords.
- **QR Code Generation:** Automatically generate QR codes for each shortened URL.
- **Dashboard:** Manage, edit, track and share shortened URLs through an intuitive dashboard.
- **User Accounts:** Use an account to manage and track your URLs across different sessions and devices.
- **Browser Sessions:** Access and monitor shortened URLs without requiring an account within your current browser session.
- **Google Safe Browsing API:** Checks the safety of URLs before shortening to avoid malicious sites.

## Technologies Used
- **Python:** Main programming language used for the backend
- **Flask:** Backend framework for handling requests and routing
- **HTML, CSS, JavaScript:** Frontend development for creating user interfaces
- **MongoDB:** NoSQL database used for storing URLs and user information
- **Bootstrap:** Frontend CSS framework for styling and responsiveness
- **Google Safe Browsing API:** Ensures the URLs are checked against Google’s safety database

## File Structure
- **app/**: Contains the core application logic and routes.
    - **auth/**: Handles user authentication (routes and logic for login, registration, account management).
    - **main/**: Includes the URL shortening logic and the main routes.
    - **templates/**: Base HTML template used in all other templates.
    - **__init__.py**: 
- **config.py**: Application configuration settings.
- **requirements.txt**: Lists the dependencies required for the project.
- **run.py**: Entry point to start the Flask application.

## Getting Started
### Prerequisites
- Python 3
- MongoDB
- A Google Safe Browsing API key
### Installation
1. Clone the repository:
    `git clone https://github.com/JGardner01/URL-Shortener.git`
2. Navigate to the project directory:
   `cd URL-Shortener`
3. Set up a virtual environment and install dependencies:
   `python -m venv venv`
   `source venv/bin/activate` On Windows, use `venv\Scripts\activate`
   `pip install -r requirements.txt`
4. Create a .env file for environment variables:
   `GOOGLE_API_KEY=your_google_safe_browsing_api_key
   FLASK_APP=run.py 
   FLASK_ENV=development`
5. Run the application:
   `python run.py`

## License
This project is licensed under the MIT License.