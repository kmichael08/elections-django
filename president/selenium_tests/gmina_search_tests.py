from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
DISPLAY_BROWSER = True


""" Acquire the web element representing the current unit in the navigation menu """
def present_unit(driver):
    present_unit = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@class='topnav']/li[last()]/a")))
    return present_unit


""" Search where results should be empty. """
def empty_search(driver):
    page = 'http://127.0.0.1:8000/polska/województwo/podlaskie'
    try:
        driver.get(page)
        try:
            first_unit = present_unit(driver).get_attribute('href')
            search_form = driver.find_element_by_id('search-form')
            name = search_form.find_element_by_name("gmina")
            name.send_keys('zzzzz')
            search_form.find_element_by_name('search-submit').click()
            WebDriverWait(driver, 10).until(
                lambda driver: driver.current_url == 'http://127.0.0.1:8000/polska/search/'
            )
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "messages")))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "subunits")))

            error = driver.find_elements_by_class_name("error")
            units = driver.find_element_by_class_name("subunits").find_elements_by_tag_name("li")
            #There should be error message and no units
            assert(error and not units)
            driver.find_element_by_name("go_back").click()
            #It should get back to source page
            assert(present_unit(driver).get_attribute('href') == first_unit)

        except NoSuchElementException:
            print('No search-form on this page!!!')

    except WebDriverException:
        print('Page not found!!!')

    except ConnectionRefusedError:
        print('Connection refused!!!')




""" Successful search """
def multi_search1(driver):
    page = 'http://127.0.0.1:8000/polska/obw%C3%B3d/0410024/'
    try:
        driver.get(page)
        try:
            first_unit = present_unit(driver).get_attribute('href')
            search_form = driver.find_element_by_id('search-form')
            name = search_form.find_element_by_name("gmina")
            name.send_keys('warszawa')
            search_form.find_element_by_name('search-submit').click()
            WebDriverWait(driver, 10).until(
                lambda driver: driver.current_url == 'http://127.0.0.1:8000/polska/search/'
            )
            WebDriverWait(driver, 10).until(
                lambda driver:
                driver.find_element_by_class_name("subunits").find_elements_by_tag_name("li"))

            error = driver.find_elements_by_class_name("error")
            units = driver.find_element_by_class_name("subunits").find_elements_by_tag_name("li")
            # There should no error message and several units
            assert (not error and units)
            rembertow = driver.find_element_by_link_text('gmina Warszawa-Rembertów')
            rembertow.click()
            assert(present_unit(driver).text == 'gmina Warszawa-Rembertów')

        except NoSuchElementException:
            print('No search-form on this page!!!')

    except WebDriverException:
        print('Page not found!!!')

    except ConnectionRefusedError:
        print('Connection refused!!!')


""" Successful search """
def multi_search2(driver):
    page = 'http://127.0.0.1:8000/polska/'
    try:
        driver.get(page)
        try:
            search_form = driver.find_element_by_id('search-form')
            name = search_form.find_element_by_name("gmina")
            name.send_keys('amo')
            search_form.find_element_by_name('search-submit').click()
            WebDriverWait(driver, 10).until(
                lambda driver: driver.current_url == 'http://127.0.0.1:8000/polska/search/'
            )

            error = driver.find_elements_by_class_name("error")
            unit = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_class_name('subunits').find_element_by_tag_name('li'))
            link = unit.find_element_by_tag_name('a')
            # There should no error message and several units
            assert (not error and unit)
            link.click()
            assert ('gmina' in present_unit(driver).text)

        except NoSuchElementException:
            print('No search-form on this page!!!')

    except WebDriverException:
        print('Page not found!!!')

    except ConnectionRefusedError:
        print('Connection refused!!!')


""" Failed search, due to too short name"""
def failed_search(driver):
    page = 'http://127.0.0.1:8000/polska/powiat/nakielski-okr-5/'
    try:
        driver.get(page)
        WebDriverWait(driver, 10).until(lambda driver: driver.current_url == page)
        try:
            first = present_unit(driver).get_attribute('href')
            search_form = driver.find_element_by_id('search-form')
            name = search_form.find_element_by_name("gmina")
            name.send_keys('sz')
            search_form.find_element_by_name('search-submit').click()
            assert(first == present_unit(driver).get_attribute('href'))

        except NoSuchElementException:
            print('No search-form on this page!!!')

    except ConnectionRefusedError:
        print('Connection refused!!!')



def no_name_inserted(driver):
    page = 'http://127.0.0.1:8000/polska/województwo/podlaskie'
    try:
        driver.get(page)
        WebDriverWait(driver, 10).until(lambda driver: 'podlaskie' in driver.current_url)
        first = present_unit(driver).get_attribute('href')
        try:
            search_form = driver.find_element_by_id('search-form')
            search_form.find_element_by_name('search-submit').click()
            assert(first == present_unit(driver).get_attribute('href'))

        except NoSuchElementException:
            print('No search-form on this page!!!')

    except WebDriverException:
        print("Bad link!!!")

    except ConnectionRefusedError:
        print('Connection refused!!!')



if __name__ == "__main__":
    if not DISPLAY_BROWSER:
        display = Display(visible=0, size=(800, 600))
        display.start()

    driver = webdriver.Firefox(executable_path='/home/michal/PycharmProjects/elections/president/selenium_tests/geckodriver')

    empty_search(driver)
    multi_search1(driver)
    multi_search2(driver)
    failed_search(driver)
    no_name_inserted(driver)

    sleep(3)
    driver.quit()

    if not DISPLAY_BROWSER:
        display.stop()