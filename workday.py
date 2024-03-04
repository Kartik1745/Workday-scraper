import csv 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = '/Users/kartikpatil/Downloads/chromedriver'
# options = Options()
# options.headless = True
# options.add_argument("--window-size=0,0")
driver = webdriver.Chrome()

# Adjust the timeout as per your requirement
wait = WebDriverWait(driver, 10)

driver.get('https://mastercard.wd1.myworkdayjobs.com/en-US/CorporateCareers')

# Wait until at least one job element is present on the page
wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))

job_elements = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')

jobs = []

for job_element in job_elements:
    job_title_element = job_element.find_element(By.XPATH, './/h3/a')
    job_title = job_title_element.text
    job_href = job_title_element.get_attribute('href')
    
    # location_element = job_element.find_element(By.XPATH, './/dd[@class="css-129m7dg"]')
    # location = location_element.text

    # job_id_element = job_element.find_element(By.XPATH, './/ul[@data-automation-id="subtitle"]/li')
    # job_id = job_id_element.text
    
    posted_on_element = job_element.find_element(By.XPATH, './/dd[@class="css-129m7dg"][preceding-sibling::dt[contains(text(),"posted on")]]')
    posted_on = posted_on_element.text
    
    if "posted today" in posted_on.lower():
        job_title_element.click()
        
        # Wait for the job description to load
        job_description_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Job Posting Description"]')))
        
        # Extract job description
        job_description = job_description_element.text

        locations_elements = job_description_element.find_elements(By.CSS_SELECTOR, "div[data-automation-id='locations'] dd.css-129m7dg")
        locations = []
        for location_element in locations_elements:
            locations.append(location_element.text)
       
        # Append job details to the list
        # jobs.append({'title': job_title,'job-id':job_id ,'href': job_href, 'location': locations, 'posted_on': posted_on, 'description': job_description})
        
        jobs.append({'title': job_title,'href': job_href, 'location': locations, 'posted_on': posted_on, 'description': job_description})

        # Go back to the previous page
        driver.back()
        
        # Wait until the job elements are loaded again
        wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))
        
        # Re-find the job elements
        job_elements = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')
        
    # jobs.append({'title': job_title,'job-id':job_id ,'href': job_href, 'location': location, 'posted_on': posted_on, 'description': job_description})

driver.quit()

# Write the jobs to a CSV file
with open('jobs.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['title', 'job-id', 'href', 'location', 'posted_on', 'description']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for job in jobs:
        writer.writerow(job)

print("Jobs saved to jobs.csv")




# v1 code

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# DRIVER_PATH = '/Users/kartikpatil/Downloads/chromedriver'
# options = Options()
# options.headless = True
# options.add_argument("--window-size=0,0")
# driver = webdriver.Chrome(options=options)

# # Adjust the timeout as per your requirement
# wait = WebDriverWait(driver, 5)

# driver.get('https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal')

# # Wait until at least one job element is present on the page
# wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))

# # print(driver.page_source)

# job_info = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')

# # print(job_info)

# jobs = []

# for job in job_info:
#     jobs.append(job.text)

# driver.quit()

# print(jobs[0])

# previous code

# from selenium import webdriver
# from selenium.webdriver.common.by import By

# DRIVER_PATH = '/Users/kartikpatil/Downloads/chromedriver'
# driver = webdriver.Chrome()

# # driver = webdriver.Chrome(executable_path='/Users/kartikpatil/Downloads/chromedriver')

# driver.get('https://mastercard.wd1.myworkdayjobs.com/en-US/CorporateCareers')

# print(driver.page_source)

# job_info = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')

# print(job_info)

# jobs = []

# for job in job_info:
#     jobs.append(job.text)

# driver.quit()

# print(jobs)
