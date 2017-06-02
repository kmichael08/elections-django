from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from president.selenium_tests.credentials import username as page_username, password as page_password
DISPLAY_BROWSER = True


def false_login_test(driver):
    try:
        page = 'http://127.0.0.1:8000/polska/województwo/pomorskie'
        driver.get(page)
        login_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'login-form'))
        )
        username = login_form.find_element_by_id('id_username')
        password = login_form.find_element_by_id('id_password')
        username.send_keys('admin')
        password.send_keys('admin')
        log_in_button = login_form.find_element_by_name('log-in')
        log_in_button.click()
        try:
            driver.find_element_by_id('logged_user')
            print('We are logged - FAIL!!!')
        except WebDriverException:
            print('We are not logged - SUCCESS!!!')

    except WebDriverException:
        print('Page not found')


def good_login_test(driver):
    try:
        page = 'http://127.0.0.1:8000/polska/województwo/podkarpackie'
        driver.get(page)
        login_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'login-form'))
        )
        try:
            username = login_form.find_element_by_id('id_username')
            password = login_form.find_element_by_id('id_password')
            username.send_keys(page_username)
            password.send_keys(page_password)
            log_in_button = login_form.find_element_by_name('log-in')
            log_in_button.click()
            try:
                logged_user = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'logged_user'))
                )
                print('We are logged - SUCCESS')
                assert(page_username in logged_user.text)
            except WebDriverException:
                print('We are not logged - FAIL!!!')

        except NoSuchElementException:
            print('Some problem with login form')

    except WebDriverException:
        print('Page not found')

    return driver


def log_out_test(driver):
    driver = good_login_test(driver)
    try:
        logged = driver.find_element_by_id('logged_user')
        logged.find_element_by_tag_name('a').click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'login-form'))
        )
        try:
            driver.find_element_by_id('logged_user')
            print('Seems that we are not logged out - FAIL')
        except NoSuchElementException:
            print('Logged out - SUCCESS')

    except NoSuchElementException:
        print('Fail to find the log out link')


if __name__ == "__main__":
    if not DISPLAY_BROWSER:
        display = Display(visible=0, size=(800, 600))
        display.start()

    driver = webdriver.Firefox(executable_path='/home/michal/PycharmProjects/elections/president/selenium_tests/geckodriver')

    false_login_test(driver)
    good_login_test(driver)
    driver.quit()

    driver = webdriver.Firefox(executable_path='/home/michal/PycharmProjects/elections/president/selenium_tests/geckodriver')
    log_out_test(driver)

    sleep(3)
    driver.quit()

    if not DISPLAY_BROWSER:
        display.stop()