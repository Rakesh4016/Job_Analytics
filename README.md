# Job Scraping Project

This project is designed to scrape job postings from Dice.com, extract relevant job details, and store them in a PostgreSQL database. The project is modularized into separate components for web scraping, database operations, and WebDriver management.

## Project Structure

- scraper.py: Contains functions to scrape job details from the web pages.
- database.py: Manages database connections and insertion of job details.
- driver_manager.py: Manages the WebDriver instance for Selenium.
- main.py: The main entry point that orchestrates the entire scraping process.

## Requirements

- Python 3.7+
- PostgreSQL
- Google Chrome
- ChromeDriver
- Python libraries:
  - selenium
  - psycopg2

## Setup Instructions
### 1. Install Python Libraries

Install the required Python libraries using pip:

pip install selenium psycopg2

### 2. Set Up PostgreSQL

1. Install PostgreSQL from the official website.
2. Create a database named `Job_Scraping`:

CREATE DATABASE Job_Scraping;

3. Create a table for storing job details:

CREATE TABLE job_details (
    id SERIAL PRIMARY KEY,
    title TEXT,
    location TEXT,
    date_posted TEXT,
    work_setting TEXT,
    work_mode TEXT,
    job_description TEXT,
    position_id TEXT,
    company_name TEXT,
    company_url TEXT,
    job_url TEXT,
    data_scraped TIMESTAMP
);

### 3. Download ChromeDriver

Download ChromeDriver from the official site and ensure it's in your system's PATH.

### 4. Update Database Credentials

Update the database credentials in `database.py`:

# database.py
connection = psycopg2.connect(
    user="postgres",
    password="your_password_here",
    host="127.0.0.1",
    port="5432",
    database="Job_Scraping"
)

### 5. Running the Scraper

Run the scraper using the following command:

python main.py

## Usage

1. The script will navigate to Dice.com, apply the "Today" filter for job postings, and scrape job details.
2. The scraped job details will be inserted into the `job_details` table in the PostgreSQL database.

## Troubleshooting

* Ensure ChromeDriver version matches your installed Google Chrome version.
* Ensure PostgreSQL service is running.
* Check database credentials if connection errors occur.


