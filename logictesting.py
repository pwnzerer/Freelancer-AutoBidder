import string
from tempfile import template

import requests

from initialize_driver import *

# https://stackoverflow.com/questions/29987323/how-do-i-send-data-from-js-to-python-with-flask
headers = {
    "authority": "www.freelancer.com",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "freelancer-app-platform": "web",
    "freelancer-app-is-native": "false",
    "freelancer-app-version": "gitRevision=1ec7ad2, buildTimestampInSeconds=1643001192",
    "sec-ch-ua-mobile": "?0",
    "freelancer-auth-v2": "60325445;RLCNGA2ANDHTT8hjdjQ2yZACgT5O9QsPMfOrRZL/whk=",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "freelancer-app-build-timestamp": "1643001192",
    "freelancer-app-locale": "en",
    "freelancer-tracking": "31fe04f1-eeb7-88fb-22f6-d1722572a718",
    "freelancer-app-name": "main",
    "freelancer-app-is-installed": "false",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.freelancer.com/search/projects?projectSkills=1094,208,1876,292,1665,761,1679,1112,13,323,335,1031,1087&types=fixed,hourly&projectUpgrades=featured,sealed,NDA,urgent,fulltime,assisted&projectLanguages=en&clientCountries=gb,us&projectFixedPriceMin=100&projectHourlyRateMin=10",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "__auc=e3912c5017e44206b65d0e2678a; _tracking_session=31fe04f1-eeb7-88fb-22f6-d1722572a718; uniform_id_linked=linked; seen_content_hub_email_capture_popup=true; GETAFREE_LANGUAGE=en; _gid=GA1.2.708344395.1643006071; session2=f4aec1e2c9cc775557f50142181b997d6e2c71fd8fcb80cdf4dc9758b8727d902cc992f6cf10dda4; XSRF-TOKEN=wyGchPTOtCXJthJctOWOe8aoIDLS6GERlFqIsOIsgx1qiGhQkvUlIsoaV7RJ9mL7; is_from_eu=false; is_from_eu_user_id=; GETAFREE_LOOKING_FOR=Worker; _ga=GA1.2.4da40abe-5613-ce37-7622-f4e63b29faf6; GETAFREE_USER_ID=60325445; GETAFREE_AUTH_HASH_V2=RLCNGA2ANDHTT8hjdjQ2yZACgT5O9QsPMfOrRZL%2Fwhk%3D; GETAFREE_NOTNEW=true; qfence=eyJhbGciOiJIUzI1NiIsInR5cCI6IkZyZWVsYW5jZXJcXEdBRlxcQ29yZVxcSldUXFxKV1QifQ.eyI2MDMyNTQ0NSI6MTY0MzAyMDIwNCwic3ViIjoicXVpY2tsb2dpbmZlbmNlIiwiaWF0IjoxNjQzMDIwMjA0fQ.OcBW7FljDtJCJtzNudS56JR9fHFk4jzBoVryTrP9Ock",
}

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
    # Vietnam
    # Monaco
    # Mauritius
    # South Africa
    # Malaysia
    # New Zealand
    # Australia
    # Japan
    # China
    # Iceland
    # Norway
    # Switzerland
    # Canada
    # United States
    # United Kingdom
    (
        "jobs[]",
        [
            "13",
            "208",
            "292",
            "323",
            "335",
            "761",
            "1031",
            "1087",
            "1094",
            "1112",
            "1665",
            "1679",
            "1876",
            "99",
            "500",
            "704",
            "759",
            "1314",
        ],
    ),
    # '''
    # What these jobs ids correspond to , I isolated these after several api calls just so in the future if u want narrow down search you can use this :))
    # Python = 13
    # HTML = 323
    # HTML5 = 335
    # Web Development = 1031
    # API = 1087
    # Flask = 1094
    # Machine Learning = 292
    # Data Science = 761
    # Selenium Wed Driver = 1112
    # Selenium = 1679
    # Machine vision / Video analytics = 1876
    # Fianancial Forecasting = 1665
    # Javascript = 99
    # Node.js = 500
    # AngularJS = 704
    # React.js = 759
    # React Native = 1314
    # '''
    ("languages[]", "en"),
    ("project_types[]", ["fixed", "hourly"]),
    ("project_upgrades[]", ["featured", "sealed", "NDA", "urgent", "fulltime", "assisted"]),
    ("reverse_sort", "true"),
    (
        "sort_field",
        "bid_count",
    ),  # submitdate , highestPrice , for fewest bid_count u need to use ('reverse_sort', 'true') parameter as well :)
    ("min_avg_hourly_rate", "10"),
    ("min_avg_price", "50"),
    ("webapp", "1"),
    ("compact", "true"),
    ("new_errors", "true"),
    ("new_pools", "true"),
)


response = requests.get("https://www.freelancer.com/api/projects/0.1/projects/active", headers=headers, params=params)
x = response.json()
noofjobs = 0
dict1 = {}
alljobs = x["result"]["projects"]
webtemp1 = [
    "web development",
    "website development",
    "web",
    "web developer",
    "web design",
    "full stack developer",
    "web app",
    "desktop app",
    "desktop application",
    ".Net Core",
    "MEAN Stack developer",
    "MERN Stack developer",
    "Angular developer",
    "React",
    "HTML",
    "CSS",
    "JS",
    "Bootstrap",
    "NodeJS",
    "PHP",
    "WordPress",
    "Shopify",
    "Website developer",
]


for job in alljobs[0:5]:
    webtemp1score = 0
    jobid = job["id"]
    jobtitle = job["title"]
    joburl = "https://www.freelancer.com/projects/" + str(jobid)
    Description = job["description"]
    descriptionlist = Description.lower().split(" ")
    jobtitlelist = jobtitle.lower().split(" ")
    totalkeywords = 0
    # print(descriptionlist)

    for keyword in webtemp1:
        print(keyword)
        totalkeywords += 1
        if (keyword.lower() in descriptionlist) or (keyword.lower() in jobtitlelist):
            webtemp1score += 1

    print(webtemp1score)
    print(totalkeywords)
    time.sleep(30)
