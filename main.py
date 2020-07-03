from selenium import webdriver
from selenium.webdriver.support.ui import Select
import threading
from random import randint
from time import sleep

# insert whatever you want (and your pc can handle)
THREAD_COUNT = 6
# edit if chromedriver is not in path
PATH_TO_CHROMEDRIVER = "chromedriver"


def main():
    try:
        # images aren't loaded to increase performance
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER, options=chrome_options)

        # waits 10s if it doesn't find an item right away to avoid NoSuchElementException
        driver.implicitly_wait(10)

        driver.get("https://www.surveymonkey.com/r/7JZRVLJ")

        age_select = Select(driver.find_element_by_xpath(
            "/html/body/main/article/section/form/div[1]/div[1]/div/div/fieldset/div/select"))
        text_field = driver.find_element_by_xpath(
            "/html/body/main/article/section/form/div[1]/div[2]/div/div/div/div/div/div/input")
        check_box = driver.find_element_by_class_name(
            "checkbox-button-display")
        submit_btn = driver.find_element_by_css_selector(
            "button[type='submit']")

        age_select.select_by_index(randint(1, 2))
        text_field.send_keys("Hurensohn")
        check_box.click()

        # the time we were on the site is send to the server (probably for bot protection)
        # so we just wait some time
        sleep(randint(3, 10))

        submit_btn.click()

        sleep(1)

        driver.quit()

        print("WIR WAREN ERFOLGREICH, MEINE BUBEN!")

    except Exception as e:
        print(e)
        driver.quit()


if __name__ == "__main__":
    while True:
        # +1 because the main thread is also returned by enumerate()
        if len(list(threading.enumerate())) < THREAD_COUNT + 1:
            threading.Thread(target=main).start()
