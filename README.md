# Job Scraper

This project is a job scraper that collects all third party job details from Dice.com and stores as a dataframe >>CSV file and then loaded into PostgreSQL database. The scraper uses Selenium for web scraping and the psycopg2 library for database operations.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Modules](#modules)

## Installation

1. Clone the repository
   git clone <repository-url>
   cd repository-directory

2. Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate

3. Install the required packages
   pip install -r requirements.txt

4. Set up the environment variables
   Create a .env file in the root directory of the project and add the following lines, replacing the placeholder values with your actual database credentials:

   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=your_host
   DB_PORT=your_port
   DB_NAME=your_database_name

5. Download the ChromeDriver
   Make sure you have the ChromeDriver installed and it's in your system's PATH.

## Usage

To run the job scraper, use the following command:

python main.py

## Project Structure

.
├── .env                # Environment variables
├── database.py         # Database operations
├── main.py             # Main script
├── scraper.py          # Web scraping functions
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

## Environment Variables

The project requires a .env file in the root directory with the following variables:
* DB_USER: PostgreSQL username
* DB_PASSWORD: PostgreSQL password
* DB_HOST: PostgreSQL host
* DB_PORT: PostgreSQL port
* DB_NAME: PostgreSQL database name

## Modules

database.py
Contains functions for database operations:
* get_db_connection(): Establishes a connection to the PostgreSQL database.
* insert_job_details(job_details): Inserts job details into the job_details table.

scraper.py
Contains functions for web scraping:
* restart_driver(): Initializes the Selenium WebDriver.
* scrape_job_details(driver, wait): Scrapes job details from the job listing page.

main.py
Main script that orchestrates the scraping and database operations.

