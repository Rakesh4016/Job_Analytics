import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def insert_job_details_to_db(job_details):
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()

        postgres_insert_query = """
        INSERT INTO job_details (title, location, date_posted, work_setting, work_mode, job_description, position_id, company_name, company_url, job_url, data_scraped)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        record_to_insert = (
            job_details['title'],
            job_details['location'],
            job_details['date_posted'],
            job_details['work_setting'],
            job_details['work_mode'],
            job_details['job_description'],
            job_details['position_id'],
            job_details['company_name'],
            job_details['company_url'],
            job_details['job_url'],
            job_details['data_scraped']
        )

        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into job_details table", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
