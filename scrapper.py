import string
from ctypes import cast
from tempfile import template

import requests
from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from database import SessionLocal, engine
from initialize import headers, params
from initialize_driver import *
from loginfunc import loaded_browser
from models import templatesinfo

# config variables here
FREELANCE_BASE_URL = config("FREELANCE_BASE_URL", cast=str)


def send_proposals(template, thejoburl):
    driver = initialize_driver()
    driver.get(thejoburl)
    print(thejoburl)
    time.sleep(100)
    try:
        proposal_text_area = driver.find_element_by_xpath("//textarea[@id='descriptionTextArea']")
        proposal_text_area.send_keys(template)
        driver.find_element_by_xpath("//button[contains(text(), 'Place Bid')]").click()
        time.sleep(300)
    except:
        return


def get_all_jobs(FREELANCE_BASE_URL, headers, params):
    response = requests.get(f"{FREELANCE_BASE_URL}/api/projects/0.1/projects/active", headers=headers, params=params)
    data = response.json()
    all_jobs = data["result"]["projects"]
    return all_jobs


def match_template(job_description, job_title):
    maxscore = 0
    winning_template = ""
    db = SessionLocal()
    alldatafromdb = db.query(templatesinfo).all()
    description_list = job_description.lower().split(" ")
    job_title_list = job_title.lower().split(" ")
    for rows in alldatafromdb:
        keyword_score = 0
        keywords = rows.keywords.split(",")
        print(keywords)
        for keyword in keywords:
            if (keyword.lower() in description_list) or (keyword.lower() in job_title_list):
                keyword_score += 1
        if keyword_score > maxscore:
            maxscore = keyword_score
            winning_template = rows.template_words
    print(winning_template)
    return winning_template


# # for using a payload approach incase we want just the api
# def process_api_data(all_jobs):
#     all_jobs_data = []
#     for job in all_jobs:
#         all_jobs_data.append(
#             {
#                 "job_id": job["id"],
#                 "job_url": f"{FREELANCE_BASE_URL}/projects/{job['id']}",
#                 "job_title": job["title"],
#                 "job_description": job["description"],
#             }
#         )
#     return all_jobs_data


def time_to_bid(all_jobs):
    total_jobs = 0
    for job in all_jobs:
        job_id = job["id"]
        job_title = job["title"]
        job_description = job["description"]
        job_url = f"https://www.freelancer.com/projects/{job_id}"
        template = match_template(job_description, job_title)
        total_jobs += 1
        if template == "":
            print("no match")
        else:
            send_proposals(template, job_url)
    print(total_jobs)


def make_params(job_skill_list):
    params = (
        ("limit", "100"),
        ("full_description", "true"),
        ("job_details", "true"),
        ("local_details", "true"),
        ("location_details", "true"),
        ("upgrade_details", "true"),
        ("user_country_details", "true"),
        ("user_details", "true"),
        ("user_employer_reputation", "true"),
        ("countries[]", ["au", "ca", "cn", "is", "jp", "my", "mu", "mc", "nz", "no", "za", "ch", "gb", "us", "vn"]),
        (
            "jobs[]",
            job_skill_list,
        ),
        ("languages[]", "en"),
        ("project_types[]", ["fixed", "hourly"]),
        ("project_upgrades[]", ["featured", "sealed", "NDA", "urgent", "fulltime", "assisted"]),
        ("reverse_sort", "true"),
        (
            "sort_field",
            "bid_count",
        ),
        ("min_avg_hourly_rate", "10"),
        ("min_avg_price", "50"),
        ("webapp", "1"),
        ("compact", "true"),
        ("new_errors", "true"),
        ("new_pools", "true"),
    )
    return params
