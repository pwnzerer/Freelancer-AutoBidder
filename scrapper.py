import string
from ctypes import cast
from tempfile import template

import requests
from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import database
import models
from initialize import headers, params
from initialize_driver import *
from loginfunc import loaded_browser

# config variables here
FREELANCE_BASE_URL = config("FREELANCE_BASE_URL", cast=str)


def send_proposals(template, thejoburl):
    driver = loaded_browser()
    driver.get(thejoburl)
    print(thejoburl)
    time.sleep(100)
    try:

        proposal_text_area = driver.find_element_by_xpath("//textarea[@id='descriptionTextArea']")
        proposal_text_area.send_keys(template)
        driver.find_element_by_xpath("//button[contains(text(), 'Place Bid')]").click()
        time.sleep(50)
    except:
        return


def get_all_jobs(FREELANCE_BASE_URL, headers, params):
    response = requests.get(f"{FREELANCE_BASE_URL}/api/projects/0.1/projects/active", headers=headers, params=params)
    data = response.json()
    all_jobs = data["result"]["projects"]
    return all_jobs


def match_template(job_description, job_title):
    keyword_score = 0
    description_list = job_description.lower().split(" ")
    job_title_list = job_title.lower().split(" ")
    for keyword in keywords:
        if (keyword.lower() in description_list) or (keyword.lower() in job_title_list):
            keyword_score += 1

    return keyword_score


def process_api_data(all_jobs):
    all_jobs_data = []
    for job in all_jobs:
        all_jobs_data.append(
            {
                "job_id": job["id"],
                "job_url": f"{FREELANCE_BASE_URL}/projects/{job['id']}",
                "job_title": job["title"],
                "job_description": job["description"],
            }
        )
    return all_jobs_data


def jobs_scoring(all_jobs, payload):
    listofjobs = []

    all_jobs_data = process_api_data(all_jobs)

    for job in all_jobs_data:

        # # init here
        mltemp1score = 0
        nlptemp1score = 0
        webtemp1score = 0
        mobtemp1score = 0
        wordpresstemp1score = 0

        if payload["ml"]["is_ml"]:
            mltemp1score = match_template(payload["ml"]["ml_keywords"], job["job_description"], job["job_title"])
        if payload["wb"]["is_wb"]:
            webtemp1score = match_template(payload["wb"]["wb_keywords"], job["job_description"], job["job_title"])
        if payload["mb"]["is_mb"]:
            mobtemp1score = match_template(payload["mb"]["mb_keywords"], job["job_description"], job["job_title"])
        if payload["wp"]["is_wp"]:
            wordpresstemp1score = match_template(
                payload["wp"]["wp_keywords"], job["job_description"], job["job_title"]
            )
        scoredict = {
            wordpresstemp1score: "wordpresstemp1",
            webtemp1score: "webtemp1",
            mltemp1score: "mltemp1",
            mobtemp1score: "mobtemp1",
        }
        maxscore = scoredict.get(max(scoredict))
        maxvalue = max(scoredict)
        if job["job_id"] not in listofjobs:
            listofjobs.append(job["job_id"])
            if maxvalue != 0:
                filename = maxscore + ".txt"
                print(maxvalue)
                print(job["job_title"])
                # print(job_description)
                print(filename)
                templatefile = open(filename, "r")
                templateitself = templatefile.readlines()
                send_proposals(templateitself, job["job_url"])
                time.sleep(30)
            else:
                print("all scores are null")


def main(payload):
    all_jobs = get_all_jobs(FREELANCE_BASE_URL, headers, params)
    jobs_scoring(all_jobs, payload)
