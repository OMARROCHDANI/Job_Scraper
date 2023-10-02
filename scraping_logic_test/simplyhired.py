
from selenium import webdriver
#Importer les modules requis :
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_page(driver):
    # Find all the job titles on the page
    jobs_simplyhired = driver.find_elements(By.CLASS_NAME, "chakra-text.css-8rdtm5")
    titles_simplyhired = [title.text.strip() for title in jobs_simplyhired]
    
    links_simplyhired = []
    for job in jobs_simplyhired:
        a_tag = job.find_element(By.TAG_NAME, "a")
        links_simplyhired.append(a_tag.get_attribute("href"))

    return list(zip(titles_simplyhired, links_simplyhired))

# Set up the WebDriver
driver = webdriver.Chrome()

# Define the number of pages you want to scrape
num_pages_to_scrape = 3

items_simplyhired = []

# Iterate through the pages
for page_num in range(1, num_pages_to_scrape + 1):
    # Construct the URL for the current page
    url = f"https://www.simplyhired.com/jobs?q=computer+science&page={page_num}"

    # Navigate to the URL
    driver.get(url)

    # Wait for some time to ensure the page is fully loaded (you might need to adjust this)
    time.sleep(2)

    # Scrape the current page
    items_simplyhired += scrape_page(driver)

    # Print the results for the current page
    print(f"Page {page_num} results:")

    for title, link in items_simplyhired:
        print(f"Title: {title}, Link: {link}")
print(len(items_simplyhired))
# Close the WebDriver
driver.quit()