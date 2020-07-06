import threading
import requests
import time
from bs4 import BeautifulSoup
from random import randint, choice

# insert whatever you want (and your pc can handle)
# don't set this too high, otherwise the website will get dosed on accident
THREAD_COUNT = 10

SURVEY_URL = "https://www.surveymonkey.com/r/7JZRVLJ"


def get_proxies():
    # parse free proxies (only german proxies)
    res = requests.get(
        "https://api.proxyscrape.com/?request=getproxies&proxytype=http&country=de", allow_redirects=True)

    return res.text.split("\r\n")


def main(proxy):
    try:
        # first make request to get validation string (csrf) and cookies
        session = requests.Session()
        cookie_response = session.get(SURVEY_URL)
        soup = BeautifulSoup(cookie_response.text, 'html.parser')
        # parse the token
        csrf_token = soup.find("input", {"id": "survey_data"})["value"]
        # generate random boundary number (necessary for the valid form data)
        boundaryNumber = str(randint(10**29, 10**30))
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
                   "Accept-Encoding": "gzip, deflate",
                   "Content-Type": "multipart/form-data; boundary=---------------------------" + boundaryNumber,
                   "Origin": "https://www.surveymonkey.com",
                   "Connection": "close",
                   "Referer": "https://www.surveymonkey.com/r/7JZRVLJ",
                   "Upgrade-Insecure-Requests": "1"}
        # generate random time spent on website
        start_time = int(round(time.time() * 1000)) - randint(70, 130)
        end_time = start_time + randint(50, 100)
        # make time always positiv
        # add 11300, because something weird is going on and this fixes it
        time_spent = end_time - start_time + 11300
        # generate random age (1: 10-15; 2: 16-20; ...)
        age = randint(1, 4)
        data = f"-----------------------------{boundaryNumber}\r\nContent-Disposition: form-data; name=\"463803414\"\r\n\r\n{str(3067519627 + age - 1)}\r\n-----------------------------{boundaryNumber}\r\nContent-Disposition: form-data; name=\"463803684\"\r\n\r\nHurensohn\r\n-----------------------------{boundaryNumber}\r\nContent-Disposition: form-data; name=\"483089934[]\"\r\n\r\n3189794655\r\n-----------------------------{boundaryNumber}\r\nContent-Disposition: form-data; name=\"survey_data\"\r\n\r\n{csrf_token}\r\n-----------------------------{boundaryNumber}\r\nContent-Disposition: form-data; name=\"response_quality_data\"\r\n\r\n{{\"question_info\":{{\"qid_463803414\":{{\"number\":1,\"type\":\"dropdown\",\"option_count\":5,\"has_other\":false,\"other_selected\":null,\"relative_position\":[[{age},0]],\"dimensions\":[5,1],\"input_method\":null,\"is_hybrid\":false}},\"qid_463803684\":{{\"number\":2,\"type\":\"open_ended\",\"option_count\":null,\"has_other\":false,\"other_selected\":null,\"relative_position\":null,\"dimensions\":null,\"input_method\":\"text_typed\",\"is_hybrid\":true}},\"qid_483089934\":{{\"number\":3,\"type\":\"multiple_choice_vertical\",\"option_count\":1,\"has_other\":false,\"other_selected\":null,\"relative_position\":[[0,0]],\"dimensions\":[1,1],\"input_method\":null,\"is_hybrid\":false}}}},\"start_time\":{start_time},\"end_time\":{end_time},\"time_spent\":{time_spent},\"previous_clicked\":false,\"has_backtracked\":false,\"bi_voice\":{{}}}}\r\n-----------------------------{boundaryNumber}\r\nContent-Disposition: form-data; name=\"is_previous\"\r\n\r\nfalse\r\n-----------------------------{boundaryNumber}\r\nContent-Disposition: form-data; name=\"disable_survey_buttons_on_submit\"\r\n\r\n\r\n-----------------------------{boundaryNumber}--\r\n"

        res = session.post(
            SURVEY_URL, headers=headers, data=data, proxies=proxy)
        print(proxy)

        # if this string is in the reponse, the request was successful
        if("Dein Jugendwort ist jetzt bei uns aufgenommen." in res.text):
            print("WIR WAREN ERFOLGREICH, MEINE BUBEN!")
        else:
            raise Exception("Etwas ist schiefgelaufen!")
    except Exception as e:
        print(e)
        print("EIN FEHLER IST AUFGETRETEN, MEINE BUBEN!")


if __name__ == "__main__":
    proxies = get_proxies()
    while True:
        # +1 because the main thread is also returned by enumerate()
        # use a random proxy every thread
        if len(list(threading.enumerate())) < THREAD_COUNT + 1:
            threading.Thread(target=main, args=[{
                             "http": choice(proxies)}]).start()
