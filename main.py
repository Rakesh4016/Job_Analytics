from driver_manager import restart_driver
from scraper import navigate_and_scrape_jobs
from database import insert_job_details_to_db

def main():
    driver, wait = restart_driver()

    all_jobs_details = navigate_and_scrape_jobs(driver, wait, insert_job_details_to_db)

    driver.quit()

if __name__ == "__main__":
    main()
