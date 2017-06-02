from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from president.selenium_tests.login_tests import good_login_test
from president.selenium_tests.credentials import username as page_username, password as page_password
DISPLAY_BROWSER = True
from selenium.webdriver.support.ui import Select

def is_logged(driver):
    try:
        driver.find_element_by_id('logged_user')
        return True
    except NoSuchElementException:
        return False


""" Try to change votes number to negative """
def negative_votes_test(driver):
    page = 'http://127.0.0.1:8000/polska/obw%C3%B3d/2212086/'
    if not is_logged(driver):
        try:
            driver = good_login_test(page, driver)
        except Exception:
            print('Logging in failed')
    try:
        initial_value = driver.find_element_by_xpath('(//table[@class="votes"]//tr)/td[2]')
        edit_form = driver.find_element_by_id('editing')
        votes = edit_form.find_element_by_id('id_votes')
        votes.clear()
        votes.send_keys(-1)
        submit_button = edit_form.find_element_by_id('submit-edit')
        submit_button.click()
        try:
            WebDriverWait(driver, 3).until(
                lambda driver: verify_votes_test(driver, initial_value, 1)
            )
            print('Votes changed - FAIL')
        except WebDriverException:
            print('Votes not changed - SUCCESS')

    except NoSuchElementException:
        print('No edit form')

    except Exception:
        print('Logging in failed')


def proper_votes_test(driver, votes_value):
    page = 'http://127.0.0.1:8000/polska/obw%C3%B3d/2212086/'
    if not is_logged(driver):
        try:
            driver = good_login_test(page, driver)
        except Exception:
            print('Logging in failed')
    try:
        edit_form = driver.find_element_by_id('editing')
        votes = edit_form.find_element_by_id('id_votes')
        votes.clear()
        votes.send_keys(votes_value)
        submit_button = edit_form.find_element_by_id('submit-edit')
        submit_button.click()
        try:
            WebDriverWait(driver, 10).until(
                lambda driver: verify_votes_test(driver, votes_value, 1)
            )
            print('Votes changed - SUCCESS')
        except WebDriverException:
            print('Votes not changed - FAIL')

    except NoSuchElementException:
        print('No edit form')


""" Verify whether the votes number is equal to the given at the given candidate """
def verify_votes_test(driver, votes_value, cand_no):
    cand = str(cand_no + 1)
    try:
        updated_value = driver.find_element_by_xpath('(//table[@class="votes"]//tr[' + cand + '])/td[2]')
    except NoSuchElementException:
        print('No votes entry')
        return False
    return int(updated_value.text) == votes_value


def make_korwin_win_test(driver, votes_value):
    page = 'http://127.0.0.1:8000/polska/obw%C3%B3d/2212086/'
    KORWIN_NUMBER = 4
    if not is_logged(driver):
        try:
            driver = good_login_test(page, driver)
        except Exception:
            print('Logging in failed')
    try:
        edit_form = driver.find_element_by_id('editing')
        votes = edit_form.find_element_by_id('id_votes')
        votes.clear()
        votes.send_keys(votes_value)
        select = Select(driver.find_element_by_id('id_kandydat'))
        select.select_by_visible_text('Janusz KORWIN-MIKKE')

        submit_button = edit_form.find_element_by_id('submit-edit')
        submit_button.click()
        try:
            WebDriverWait(driver, 10).until(
                lambda driver: verify_votes_test(driver, votes_value, KORWIN_NUMBER)
            )
            print('Votes changed - SUCCESS')
        except WebDriverException:
            print('Votes not changed - FAIL')

    except NoSuchElementException:
        print('No edit form')



if __name__ == "__main__":
    if not DISPLAY_BROWSER:
        display = Display(visible=0, size=(800, 600))
        display.start()

    driver = webdriver.Firefox(executable_path='/home/michal/PycharmProjects/elections/president/selenium_tests/geckodriver')

    negative_votes_test(driver)
    proper_votes_test(driver, votes_value=10)
    proper_votes_test(driver, votes_value=10000)
    make_korwin_win_test(driver, 1000000)
    make_korwin_win_test(driver, 1000000000)

    sleep(10)
    driver.quit()

    if not DISPLAY_BROWSER:
        display.stop()