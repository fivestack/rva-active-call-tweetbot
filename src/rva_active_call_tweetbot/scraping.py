import time
from typing import List

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

RVA_ACTIVE_CALLS_URL = "https://apps.richmondgov.com/applications/activecalls/"
SECONDS_TO_LET_JS_LOAD = 2


def get_firefox_driver() -> 'webdriver.Firefox':
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    options = Options()
    options.add_argument("--headless")
    return webdriver.Firefox(firefox_profile=profile, options=options)


def parse_all_calls_into_list_of_calls(all_calls: 'List[str]') -> 'List[List[str]]':
    length = 7
    list_of_calls = []
    for i in range(0, len(all_calls), length):
        list_of_calls.append(all_calls[i:i + length])
    return list_of_calls


def parse_active_call(call_attributes: 'List[str]') -> dict:
    parsed_call = {
        "time_received": call_attributes[0],
        "agency": call_attributes[1],
        "dispatch_area": call_attributes[2],
        "unit": call_attributes[3],
        "call_type": call_attributes[4],
        "location": call_attributes[5],
        "status": call_attributes[6]
    }
    return parsed_call


def get_active_calls() -> 'List[dict]':
    driver = get_firefox_driver()
    driver.get(RVA_ACTIVE_CALLS_URL)
    time.sleep(SECONDS_TO_LET_JS_LOAD)
    active_calls_div = driver.find_element_by_id("tblActiveCallsListing")
    active_calls_rows = active_calls_div.find_elements_by_xpath("//tbody/tr/td")
    all_call_attributes = [attribute.text for attribute in active_calls_rows]
    driver.close()

    list_of_calls = parse_all_calls_into_list_of_calls(all_call_attributes)
    active_calls = [parse_active_call(call) for call in list_of_calls]
    return active_calls
