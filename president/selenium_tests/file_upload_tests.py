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


def upload_file_test(driver):
    page = 'http://127.0.0.1:8000/polska/obw%C3%B3d/2212086/'
    if not is_logged(driver):
        try:
            driver = good_login_test(page, driver)
        except Exception:
            print('Logging in failed')

        pdf_upload_form = driver.find_element_by_id('upload')
        submit_button = pdf_upload_form.find_element_by_id('submit-upload')
        pdf_file = pdf_upload_form.find_element_by_id('id_pdf_obwod')
        pdf_file.send_keys('/home/michal/PycharmProjects/elections/president/selenium_tests/siatka.pdf')
        submit_button.click()
        assert(driver.find_elements_by_partial_link_text('Protokół'))


if __name__ == "__main__":
    if not DISPLAY_BROWSER:
        display = Display(visible=0, size=(800, 600))
        display.start()

    driver = webdriver.Firefox(executable_path='/home/michal/PycharmProjects/elections/president/selenium_tests/geckodriver')

    upload_file_test(driver)

    sleep(4)
    driver.quit()

    if not DISPLAY_BROWSER:
        display.stop()