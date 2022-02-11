import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def wait_for_class_name(class_name, driverr, timeout):
    """
    :param driverr:
    :param class_name:
    :param timeout: time to wait for element
    :return:
    """
    WebDriverWait(driver=driverr, timeout=timeout).until(
        expected_conditions.element_to_be_clickable((By.CLASS_NAME, class_name))
    )


def wait_for_selector(selector, driverr, timeout):
    """
    :param driverr:
    :param selector:
    :param timeout: time to wait for element
    :return:
    """
    WebDriverWait(driver=driverr, timeout=timeout).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )


def wait_for_xpath(xpath, driverr, timeout):
    """
    :param driverr:
    :param xpath:
    :param timeout: time to wait for element
    :return:
    """
    WebDriverWait(driver=driverr, timeout=timeout).until(
        expected_conditions.element_to_be_clickable((By.XPATH, xpath))
    )


# def extract_data_from_csv():
#     """

#     :return: bids data
#     """
#     rows = []
#     try:
#         with open("keywords.csv", 'r') as file:
#             csv_reader = csv.reader(file)
#             for row in csv_reader:
#                 rows.append(row)
#     except Exception as e:
#         print(e)
#         print('error while trying to read csv')
#     bids_data = []
#     for i in range(1, len(rows)):
#         bids_data.append({'keyword': rows[i][0], 'proposal': rows[i][1]})

#     return bids_data

# def calculate_bid_score(description: str, title: str, keywords):
#     """

#     :param description:
#     :param title:
#     :param keywords: array of strings
#     :return:
#     """
#     score = 0
#     for keyword in keywords:
#         if keyword.lower() in description.lower() or keyword.lower() in title.lower():
#             score = score + 1
#     return score
