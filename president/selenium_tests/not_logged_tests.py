from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from president.selenium_tests.credentials import username as page_username, password as page_password
DISPLAY_BROWSER = True


def no_edit_when_logged_out(driver):
    page = 'http://127.0.0.1:8000/polska/obw%C3%B3d/2212087/'
    try:
        driver.get(page)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'login-form'))
            )
            try:
                driver.find_element_by_id('editing')
                print('We can edit votes being logged out - FAIL')
            except NoSuchElementException:
                print('No edit form - SUCCESS')
        except WebDriverException:
            print('We are probably logged - FAIL!!!')

    except WebDriverException:
        print('Page not found')


def no_upload_when_logged_out(driver):
    page = 'http://127.0.0.1:8000/polska/obw%C3%B3d/2212086/'
    try:
        driver.get(page)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'login-form'))
            )
            try:
                driver.find_element_by_id('upload')
                print('We can upload file being logged out - FAIL')
            except NoSuchElementException:
                print('No upload form - SUCCESS')
        except WebDriverException:
            print('We are probably logged - FAIL!!!')

    except WebDriverException:
        print('Page not found')


if __name__ == "__main__":
    if not DISPLAY_BROWSER:
        display = Display(visible=0, size=(800, 600))
        display.start()

    driver = webdriver.Firefox(executable_path='/home/michal/PycharmProjects/elections/president/selenium_tests/geckodriver')

    no_edit_when_logged_out(driver)
    no_upload_when_logged_out(driver)

    sleep(3)
    driver.quit()

    if not DISPLAY_BROWSER:
        display.stop()