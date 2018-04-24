import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.action_chains import ActionChains


##  Clicks element
def click(driver,elem):
    actions = ActionChains(driver)
    actions.move_to_element(elem)
    actions.click(elem)
    actions.perform()


##  Clicks elem & types sendinfo in it
def click_send(driver,elem,sendinfo):
    elem.click()
    actions = ActionChains(driver)
    actions.move_to_element(elem)
    actions.click(elem)

    actions.send_keys(sendinfo)
    actions.perform()


def source_to_soup(page_source):
    soup = BeautifulSoup(page_source, 'html5lib')
    return soup

def request_fun(url):
    headers = {
        "referer": "https://www.just-eat.co.uk/restaurants-starofbanagal",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html5lib')
    return soup


def read_url_file(filename):
    file = open(filename, "r")
    return file.read().split('\n')