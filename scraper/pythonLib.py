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


def read_url_file(filename):
    file = open(filename, "r")
    return file.read().split('\n')