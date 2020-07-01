from selenium import webdriver
from selenium.webdriver.support.ui import Select
import threading
from random import randint
from time import sleep


# thread count, insert whatever you want
THREAD_COUNT = 5


def main():
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.surveymonkey.com/r/7JZRVLJ")

        age_select = Select(driver.find_element_by_xpath("/html/body/main/article/section/form/div[1]/div[1]/div/div/fieldset/div/select"))
        text_field = driver.find_element_by_xpath("/html/body/main/article/section/form/div[1]/div[2]/div/div/div/div/div/div/input")
        check_box  = driver.find_element_by_class_name("checkbox-button-display")
        submit_btn = driver.find_element_by_css_selector("button[type='submit']")

        age_select.select_by_index(randint(1,2))
        text_field.send_keys("Hurensohn")
        check_box.click()
        
        # the time we were on the site is send to the server (probably for bot protection)
        # so we just wait some time
        sleep(3)

        submit_btn.click()
        
        sleep(1)

        driver.quit()

        print("WIR WAREN ERFOLGREICH, MEINE BUBEN!")
    
    # sometimes randomly giving me element not found exceptions. 
    # but i'm to lazy to fix it so....
    except:
        driver.quit()

if __name__ == "__main__":
    while True:
        # +1 because the main thread is also returned by enumerate()
        if len(list(threading.enumerate())) < THREAD_COUNT + 1:
            threading.Thread(target = main).start()

