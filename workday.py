import csv 
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

DRIVER_PATH = '/Users/kartikpatil/Downloads/chromedriver'

# Load or initialize job_ids_dict from file
try:
    with open('job_ids_dict.pkl', 'rb') as f:
        job_ids_dict = pickle.load(f)
except FileNotFoundError:
    job_ids_dict = {}

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

company_urls = [
    'https://mastercard.wd1.myworkdayjobs.com/en-US/CorporateCareers', 
    ]  # Add your company URLs here

for company_url in company_urls:
    if company_url not in job_ids_dict:
        job_ids_dict[company_url] = []

while True:
    job_urls = []
    jobstosend =[]
    for company_url in company_urls:
        driver.get(company_url)

        today = True
        while today:
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))
            
            job_elements = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')

            for job_element in job_elements:
                job_title_element = job_element.find_element(By.XPATH, './/h3/a')
                job_id_element = job_element.find_element(By.XPATH, './/ul[@data-automation-id="subtitle"]/li')
                job_id = job_id_element.text
                posted_on_element = job_element.find_element(By.XPATH, './/dd[@class="css-129m7dg"][preceding-sibling::dt[contains(text(),"posted on")]]')
                posted_on = posted_on_element.text
                if 'posted today' in posted_on.lower():
                    job_href = job_title_element.get_attribute('href')
                    if job_id not in job_ids_dict[company_url]:
                        job_ids_dict[company_url].append(job_id)
                        job_urls.append(job_href)
                    else:
                        print(f"Job ID {job_id} already in job_ids_dict")
                else:
                    today = False

            next_button = driver.find_element(By.XPATH, '//button[@data-uxi-element-id="next"]')
            if "disabled" in next_button.get_attribute("class"):
                break  # exit loop if the "next" button is disabled
            
            next_button.click()

    print(len(job_ids_dict[company_urls[0]]))
    print(len(job_urls))

    jobs = []

    for job_url in job_urls:
        driver.get(job_url)
        job_posting_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-automation-id="job-posting-details"]')))
        job_posting_text = job_posting_element.text
        jobs.append(job_posting_text)

    # Write job postings to a CSV file
    with open('job_postings.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Job Posting'])
        for job in jobs:
            writer.writerow([job])

    # Save job_ids_dict to file
    with open('job_ids_dict.pkl', 'wb') as f:
        pickle.dump(job_ids_dict, f)

    # Wait for a certain period before running again
    time.sleep(600)  # Run every hour
