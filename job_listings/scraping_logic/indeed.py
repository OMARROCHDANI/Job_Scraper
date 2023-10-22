from selenium import webdriver
#Importer les modules requis :
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_indeed(query, num_pages):
    # Set up the WebDriver
    driver = webdriver.Chrome()

    items_indeed = []

    # Iterate through the pages
    for page_num in range(1, num_pages + 1):
        # Construct the URL for the current page
        url = f"https://www.indeed.com/jobs?q={query}&page={page_num}"

        # Navigate to the URL
        driver.get(url)

        # Wait for some time to ensure the page is fully loaded (you might need to adjust this)
        

        # Scrape the current page
        jobs_indeed = driver.find_elements(By.CLASS_NAME, "jobTitle")
        payment_type=driver.find_elements(By.CLASS_NAME, 'metadataContainer')
        payments_indeed = []
        # metadatas = []
        for payment in payment_type:
            try:
                salary_snippet_container = payment.find_element(By.CSS_SELECTOR, 'div.metadata.estimated-salary-container,div.metadata.salary-snippet-container')
                payments_indeed.append(salary_snippet_container.text)
                # metadata_one_job_text = []
                # metadata_one_job = payment.find_elements(By.CLASS_NAME, 'metadata')
                # for m in metadata_one_job :
                #        mtext = m.text   
                #        if '$' not in mtext :                     
                #             metadata_one_job_text.append(m.text)
                # metadatas.append(metadata_one_job_text)
            except NoSuchElementException:
                payments_indeed.append('payment not provided')
                
                
        titles_indeed = [title.text.strip() for title in jobs_indeed]
        links_indeed = [job.find_element(By.TAG_NAME, "a").get_attribute("href") for job in jobs_indeed]

        items_indeed += list(zip(titles_indeed, links_indeed, payments_indeed))



    # Close the WebDriver
    driver.quit()

    return items_indeed

# # Example usage
# query_to_search = "computer+science"
# number_of_pages_to_scrape = 3

# results = scrape_indeed(query_to_search, number_of_pages_to_scrape)
# # Print the results for the current page
# the metadatas are for additional info in indeed like job type and other data
# for title, link,payment,metadatas in results:
#     print(f"Title: {title}, Link: {link}, Payment: {payment}")
#     print('metadata :')
#     for metadata in metadatas :
#          print(metadata)
# print(f"Total results: {len(results)}")
