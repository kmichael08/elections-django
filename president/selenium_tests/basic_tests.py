#!/usr/bin/env python3
from selenium import webdriver
from pyvirtualdisplay import Display
from collections import deque
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from functools import reduce
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re

""" First list has smaller corresponding elements than the other. """
def all_smaller(a, b):
    def conjunction(p, q):
        return p and q
    return reduce(conjunction, [p <= q for p, q in zip(a, b)], True)


class Page:
    def __init__(self, url, parent=None):
        self.url = url
        self.parent = parent
        self.results = None

    def smaller_than_parent(self):
        if self.parent is None:
            return True
        else:
            return all_smaller(self.results, self.parent.results)


DISPLAY_BROWSER = True

if not DISPLAY_BROWSER:
    display = Display(visible=0, size=(800, 600))
    display.start()

driver = webdriver.Firefox(executable_path='/home/michal/geckodriver/geckodriver')

init_page = 'http://127.0.0.1:8000/polska/kraj/Polska'

pages = deque([Page(init_page)])


def bfs():
    while len(pages) != 0:
        page_obj = pages.popleft()
        url = page_obj.url
        try:
            driver.get(url)
            present_unit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@class='topnav']/li[last()]/a")))
            print(present_unit.text + ': ')
            home_page = driver.find_element_by_xpath("//ul[@class='topnav']/li[1]/a")

            if home_page.get_attribute('href') == init_page:
                print('     correct link to homepage')
            else:
                print('     no link to homepage!!!')

            try:
                votes = driver.find_element_by_class_name('votes')
                print('     vote results found')
                page_obj.results = [int(re.sub(',', '', el.text)) for el in votes.find_elements_by_xpath('//tr/td[2]')[:12]]
                if page_obj.smaller_than_parent():
                    print('     results seem to be correct')
                else:
                    print('     results are incorrect!!!')

            except NoSuchElementException:
                print('     no vote results!!!')

            sub_pages = driver.find_elements_by_xpath("//div[@class='subunits']/ul/li/a")
            for sub_page in sub_pages:
                pages.append(Page(sub_page.get_attribute('href'), parent=page_obj))


        except WebDriverException:
            print('We have a broken link!!!')

        except ConnectionRefusedError:
            print('Connection refused', url)

bfs()

driver.quit()

if not DISPLAY_BROWSER:
    display.stop()