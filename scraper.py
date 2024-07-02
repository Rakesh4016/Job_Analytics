import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_job_details(driver, wait):
    job_details = {}

    try:
        job_details['title'] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[data-cy='jobTitle']"))).text
    except:
        job_details['title'] = None

    try:
        job_details['location'] = driver.find_element(By.CSS_SELECTOR, "li[data-cy='location']").text
    except:
        job_details['location'] = None

    try:
        job_details['date_posted'] = driver.find_element(By.CSS_SELECTOR, "li[data-cy='postedDate'] span#timeAgo").text
    except:
        job_details['date_posted'] = None

    try:
        job_details['work_setting'] = driver.find_element(By.CSS_SELECTOR, "div.chip_chip__cYJs6 span[id^='location']").text
    except:
        job_details['work_setting'] = None

    try:
        job_details['work_mode'] = driver.find_element(By.CSS_SELECTOR, "div.chip_chip__cYJs6 span[id^='employmentDetailChip']").text
    except:
        job_details['work_mode'] = None

    try:
        read_full_description_button = driver.find_element(By.ID, "descriptionToggle")
        driver.execute_script("arguments[0].click();", read_full_description_button)
        time.sleep(1)
        job_description_html = driver.find_element(By.CSS_SELECTOR, "div[data-cy='jobDescription']").text
        job_details['job_description'] = job_description_html

        position_id_prefix = "Position Id: "
        position_id_start = job_description_html.find(position_id_prefix)
        if position_id_start != -1:
            position_id_start += len(position_id_prefix)
            position_id_end = job_description_html.find("\n", position_id_start)
            if position_id_end == -1:
                position_id_end = len(job_description_html)
            job_details['position_id'] = job_description_html[position_id_start:position_id_end].strip()
        else:
            job_details['position_id'] = None
    except:
        job_details['job_description'] = None
        job_details['position_id'] = None

    try:
        job_details['company_name'] = driver.find_element(By.CSS_SELECTOR, "li.job-header_jobDetailFirst__xI_5S a[data-cy='companyNameLink']").text
    except:
        job_details['company_name'] = None

    try:
        job_details['company_url'] = driver.find_element(By.CSS_SELECTOR, "li.job-header_jobDetailFirst__xI_5S a[data-cy='companyNameLink']").get_attribute("href")
    except:
        job_details['company_url'] = None

    job_details['job_url'] = driver.current_url
    job_details['data_scraped'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return job_details

def navigate_and_scrape_jobs(driver, wait, insert_job_details_to_db):
    all_jobs_details = []
    jobs_processed = 0
    job_search_url = 'https://www.dice.com/jobs'
    driver.get(job_search_url)

    try:
        today_option = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-cy='posted-date-option' and contains(text(), 'Today')]")))
        driver.execute_script("arguments[0].click();", today_option)
        print("Today option clicked directly")
    except Exception as e:
        print(f"Failed to click 'Today' option: {e}")
        return

    time.sleep(5)  # Wait for the filter to apply

    try:
        total_jobs_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-cy='search-count-mobile']")))
        total_jobs = driver.execute_script("return arguments[0].textContent;", total_jobs_element).strip()
        if total_jobs:
            print(f"Total jobs found: {total_jobs}")
        else:
            print("Total jobs element found but text is empty")
            return
    except Exception as e:
        print("Unable to find total jobs count:", e)
        return

    while True:
        try:
            job_elements = driver.find_elements(By.XPATH, "//a[@data-cy='card-title-link']")

            for job_element in job_elements:
                original_window = driver.current_window_handle

                driver.execute_script("arguments[0].scrollIntoView(true);", job_element)
                driver.execute_script("arguments[0].click();", job_element)

                wait.until(EC.number_of_windows_to_be(2))

                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)
                        break

                job_url = driver.current_url
                print(f"Navigated to job URL: {job_url}")

                time.sleep(2)

                job_details = scrape_job_details(driver, wait)
                insert_job_details_to_db(job_details)
                all_jobs_details.append(job_details)
                jobs_processed += 1

                driver.close()
                driver.switch_to.window(original_window)
                time.sleep(4)

            try:
                next_page_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.pagination-next.page-item.ng-star-inserted a.page-link[rel='nofollow']")))
                if 'disabled' in next_page_element.get_attribute('class'):
                    print("No more pages to navigate.")
                    break
                current_url = driver.current_url
                driver.execute_script("arguments[0].click();", next_page_element)
                print("Navigated to the next page")
                wait.until(EC.url_changes(current_url))
                time.sleep(4)
            except Exception as e:
                print("No more pages found or unable to navigate to the next page:", e)
                break
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            break

    return all_jobs_details
