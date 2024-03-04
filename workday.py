import csv 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

DRIVER_PATH = '/Users/kartikpatil/Downloads/chromedriver'

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

driver.get('https://mastercard.wd1.myworkdayjobs.com/en-US/CorporateCareers')

today = True
job_urls = []
while today:
    time.sleep(1)
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
            job_urls.append(job_href)
        else:
            today = False

    next_button = driver.find_element(By.XPATH, '//button[@data-uxi-element-id="next"]')
    if "disabled" in next_button.get_attribute("class"):
        break  # exit loop if the "next" button is disabled
    
    next_button.click()

print(len(job_urls))

# jobs = []

# for job_url in job_urls:
#     driver.get(job_url)
#     job_posting_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-automation-id="jobPostingPage"]')))
#     job_posting_text = job_posting_element.text
#     # print(job_posting_text)
#     driver.back()

driver.quit()
