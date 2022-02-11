
from initialize_driver import initialize_driver
from helpers import *
import time
import math
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from extract_jobs import *
import dbutils
import schedule
import sheets_helpers


email = 'muhammad.haris@thdinfinity.com'
password = 'Password@1'


# function for logging in
def login_handling(chrome_driver):
    try:
        login_button_xpath = "//a[contains(text(), 'Log In')]"
        wait_for_xpath(xpath=login_button_xpath, timeout=5, driverr=chrome_driver)
        chrome_driver.find_element_by_xpath(login_button_xpath).click()
        email_input_selector = 'body > app-root > app-logged-out-shell > app-login-page > fl-container > fl-bit > app-login > app-credentials-form > form > fl-input.ng-tns-c189-10.ng-star-inserted > fl-bit > fl-bit > fl-bit > input'
        wait_for_selector(selector=email_input_selector, timeout=5, driverr=chrome_driver)
        chrome_driver.find_element_by_css_selector(email_input_selector).send_keys(email)
        chrome_driver.find_element_by_css_selector(
            'body > app-root > app-logged-out-shell > app-login-page > fl-container > fl-bit > app-login > app-credentials-form > form > fl-input.ng-tns-c189-11.ng-star-inserted > fl-bit > fl-bit > fl-bit > input').send_keys(
            password)
        time.sleep(4)
        chrome_driver.find_element_by_css_selector(
            'body > app-root > app-logged-out-shell > app-login-page > fl-container > fl-bit > app-login > app-credentials-form > form > app-login-signup-button > fl-button > button').click()
        time.sleep(4)
    except Exception as e:
        print(e)
        print('already logged in')


# extract project links using selenium. i am not using this approach
def extract_project_links(chrome_driver):
    print('extract links')
    job_links = []
    wait_for_xpath(xpath="//fl-bit[@class='BitsListItemContent ng-star-inserted']", driverr=chrome_driver, timeout=20)
    print('1')
    time.sleep(3)
    chrome_driver.execute_script("window.scrollBy(0, 300)")
    time.sleep(4)
    chrome_driver.execute_script("window.scrollTo(300, 500)")
    time.sleep(4)
    wait_for_xpath(
        xpath="//fl-bit[@class='BitsListItemContent ng-star-inserted']//a[@class='LinkElement ng-star-inserted']",
        driverr=chrome_driver, timeout=20)
    main_job_elements = chrome_driver.find_elements_by_xpath("//fl-bit[@class='BitsListItemContent ng-star-inserted']")
    print('2')
    for el in main_job_elements:
        print('3')
        try:
            print('4')
            anchor_tag = el.find_element_by_xpath(".//a[@class='LinkElement ng-star-inserted']")
            job_links.append(anchor_tag.get_attribute('href'))
            print('4')
            # print(anchor_tag.get_attribute('href'))
        except Exception as e:
            print(e)
            print('anchor tag not found')
        print('5')
    print(job_links)
    return job_links


# extract job links using private api and save them to DB
def extract_all_jobs():
    query_terms_data = sheets_helpers.get_all_query_terms()
    try:
        for query_term_data in query_terms_data:
            try:
                jobs_found = search_jobs(query_term_data["Query Term"], sheets_helpers.remove_white_spaces(query_term_data['Keywords'].split(',')))
                dbutils.save_jobs_to_db(jobs_found)
            except Exception as ee:
                print(ee)
                print('error occured while extracting in loop')
                continue
    except Exception as e:
        print(e)
        print('error occured while extracting all jobs')


# send proposals to jobs saved in DB
def send_proposals():
    jobs = dbutils.get_pending_jobs()
    # print('jobs found => ', jobs.count())
    for job in jobs:
        try:
            # send proposal
            driver = initialize_driver()
            # login_handling(driver)
            driver.get(job['url'])
            print(job['url'])
            time.sleep(100)
            # checking if project open or not
            try:
                driver.find_element_by_xpath("//div[contains(text(), ' This project is closed for bidding ')]")
                dbutils.update_project_open_status(job['_id'])
                is_closed = True
            except:
                is_closed = False
            # checking if we can bid on job or not
            try:
                driver.find_element_by_xpath("//fl-bit[@class='BannerAlertBox-inner']")
                dbutils.update_project_restricted_status(job['_id'])
                is_restricted = True
            except:
                is_restricted = False
            # if we can bid on job
            if not is_restricted and not is_closed:
                proposal_text_area = driver.find_element_by_xpath("//textarea[@id='descriptionTextArea']")
                proposal_text_area.send_keys('hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal hi there this is a proposal')
                time.sleep(50)
                driver.find_element_by_xpath("//button[contains(text(), 'Place Bid')]").click()
                time.sleep(4)
                # update the status of job in DB
                dbutils.update_status_of_job(job['_id'])
            else:
                print('cannot bid on project')
            if driver:
                driver.quit()
        except Exception as e:
            if driver:
                driver.quit()
            print(e)
            print('error occurred in send proposals function')


def main_func():
    print('main func')
    # extract_all_jobs()
    send_proposals()


schedule.every(3).seconds.do(main_func)

while True:
    schedule.run_pending()
    time.sleep(1)



# //fl-button[@fltrackinglabel='PlaceBidButton']

# //button[contains(text(), 'Place Bid')]

# closed project xpath
# //div[contains(text(), ' This project is closed for bidding ')]

# closed project
# https://www.freelancer.com/projects/software-architecture/Technical-Founder-CTO-Software-Architect


# Search jobs using selenium

# driver = initialize_driver()
# login_handling(driver)
# driver.get(f'https://www.freelancer.com/search/projects?q={bid["keyword"]}')
# result_count_selector = 'body > app-root > app-logged-in-shell > div > fl-container > div > div > app-search > app-search-projects > fl-bit > fl-container > fl-bit > fl-bit.ResultsContainer > app-search-results > fl-card > fl-bit > fl-bit.CardHeader.ng-star-inserted > fl-bit > fl-heading > h2 > fl-card-header-title > fl-bit > fl-bit.SearchResultsHeader-title > fl-text > div'
# wait_for_selector(selector=result_count_selector, driverr=driver, timeout=10)
# result_count_text = driver.find_element_by_css_selector(result_count_selector).text
# total_count = result_count_text.split('of ')[1].split(' results')[0]
# no_of_pages = math.ceil(int(total_count)/20)
# print(no_of_pages)
# links = extract_project_links(driver)
# for x in range(2, no_of_pages+1):
#     button_parent_xpath = f"//fl-bit[@class='NumeralContainer ng-star-inserted']/fl-bit[{x}]//button"
#     button_parent = driver.find_element_by_xpath(button_parent_xpath).click()
#     wait_for_xpath(timeout=20, xpath=button_parent_xpath, driverr=driver)
#     extracted_links = extract_project_links(driver)
#     links.extend(extracted_links)
#     # time.sleep(100)
# print(links)
# print(len(links))
# time.sleep(100)
# if driver:
#     driver.quit()
