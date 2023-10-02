# ProfessionPulse

## Overview

Welcome to ProfessionPulse – your dynamic gateway to an enriched job-search experience. This innovative platform, powered by Python, Django, Selenium, and BeautifulSoup, is designed to streamline and elevate your job-search process.

# Features

**User Authentication:**
- Sign up to create a personalized account.
- Securely log in to access your profile and job search preferences.

**Intelligent Job Scraping:**
- Utilize Selenium and BeautifulSoup for precise web scraping of job listings.
- Access the latest job postings from various sources in real-time.

**Save Jobs for Later:**
- Bookmark and save job listings for future reference.
- Easily access and manage your saved jobs from your profile.

## How It Works

**User Registration:**
- Create your account with a few simple steps.
- Provide your profession.

**Browse Job Listings:**
- Discover job opportunities by either inputting a specific profession into the search bar or utilizing the profession specified in your profile for customized job recommendations.

**Apply and Thrive:**
- Easily apply to job listings of interest.
- Save jobs for later review.

## Installation

Ensure you have [Python](https://www.python.org/downloads/) installed on your machine.

1. Clone the repository:
   ```bash
   git clone https://github.com/OMARROCHDANI/Profession_Pulse.git

2. Navigate to the project directory:
   ```bash
   cd ProfessionPulse
    
3. Create a virtual environment (optional but recommended):
   ```bash
    python -m venv venv

4. Activate the virtual environment:
   ```bash
   venv\Scripts\activate

5. Install dependencies:
    ```bash
    pip install -r requirements.txt

6. Create a superuser account:
    ```bash
    python manage.py createsuperuser

5. Start the development server:
    ```bash
    python manage.py runserver

Now, your ProfessionPulse instance is up and running. Open your web browser and navigate to http://localhost:8000 to access the application.

## Acknowledgments

We would like to thank the following libraries and frameworks that have been instrumental in the development of ProfessionPulse:

- [Django](https://www.djangoproject.com/)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

