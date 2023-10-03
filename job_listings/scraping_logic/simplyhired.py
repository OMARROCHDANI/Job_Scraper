from selenium import webdriver
#Importer les modules requis :
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import time




def scrape_simplyhired(query, num_pages):
    # Set up the WebDriver
    driver = webdriver.Chrome()

    items_simplyhired = []

    # Iterate through the pages
    for page_num in range(1, num_pages + 1):
        # Construct the URL for the current page
        url = f"https://www.simplyhired.com/jobs?q={query}&page={page_num}"

        # Navigate to the URL
        driver.get(url)

        # Wait for some time to ensure the page is fully loaded (you might need to adjust this)
        time.sleep(2)

        # Scrape the current page
        jobs_simplyhired  = driver.find_elements(By.CLASS_NAME, "chakra-text.css-8rdtm5")
        titles_simplyhired  = [title.text.strip() for title in jobs_simplyhired ]
        links_simplyhired  = [job.find_element(By.TAG_NAME, "a").get_attribute("href") for job in jobs_simplyhired ]

        items_simplyhired  += list(zip(titles_simplyhired , links_simplyhired ))

        # # Print the results for the current page
        # print(f"Page {page_num} results:")

        # for title, link in items_simplyhired :
        #     print(f"Title: {title}, Link: {link}")

    # Close the WebDriver
    driver.quit()

    return items_simplyhired 

# # Example usage
# query_to_search = "computer+science"
# number_of_pages_to_scrape = 3

# results = scrape_simplyhired (query_to_search, number_of_pages_to_scrape)
# print(f"Total results: {len(results)}")