import threading
import requests
import time
from bs4 import BeautifulSoup
from random import randint, choice
import argparse

# standard values
THREAD_COUNT = 10
SURVEY_URL = "https://www.surveymonkey.com/r/7JZRVLJ"
WORD = "Hurensohn"

# global variables for info thread
successful_votes = 0
failed_votes = 0


def get_proxies() -> list:
    res = requests.get(
        "https://api.proxyscrape.com/?request=getproxies&proxytype=http", allow_redirects=True)
    print("[*] Proxylist von Proxyscrape geladen!")
    return res.text.split("\r\n")


def get_proxies_from_proxylist(path) -> list:
    file = open(path, "r")
    proxies = [proxie.rstrip("\n") for proxie in file]
    file.close()
    print("[*] Proxylist aus Datei geladen!")
    return proxies


def vote_thread(proxy):
    global successful_votes
    global failed_votes
    global threads_running
    global SURVEY_URL
    global WORD

    try:
        # first make request to get validation string (csrf) and cookies
        session = requests.Session()
        cookie_response = session.get(SURVEY_URL, proxies=proxy)
        soup = BeautifulSoup(cookie_response.text, 'html.parser')

        # parse the token
        csrf_token = soup.find("input", {"id": "survey_data"})["value"]

        # generate random boundary number (necessary for the valid form data)
        boundaryNumber = str(randint(10**29, 10**30))
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "multipart/form-data; boundary=---------------------------" + boundaryNumber,
            "Origin": "https://www.surveymonkey.com",
            "Connection": "close",
            "Referer": "https://www.surveymonkey.com/r/7JZRVLJ",
            "Upgrade-Insecure-Requests": "1"
        }

        # generate random time for "website visit"
        start_time = int(time.time()) - randint(70, 130)
        end_time = start_time + randint(50, 100)
        time_spent = end_time - start_time + 11300

        # generate random age (1: 10-15; 2: 16-20; ...)
        age = randint(1, 4)
        data = f"-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"463803414\"\r\n\r\n{str(3067519627 + age - 1)}\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"463803684\"\r\n\r\n{ WORD }\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"483089934[]\"\r\n\r\n3189794655\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"survey_data\"\r\n\r\n{ csrf_token }\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"response_quality_data\"\r\n\r\n{{\"question_info\":{{\"qid_463803414\":{{\"number\":1,\"type\":\"dropdown\",\"option_count\":5,\"has_other\":false,\"other_selected\":null,\"relative_position\":[[{ age },0]],\"dimensions\":[5,1],\"input_method\":null,\"is_hybrid\":false}},\"qid_463803684\":{{\"number\":2,\"type\":\"open_ended\",\"option_count\":null,\"has_other\":false,\"other_selected\":null,\"relative_position\":null,\"dimensions\":null,\"input_method\":\"text_typed\",\"is_hybrid\":true}},\"qid_483089934\":{{\"number\":3,\"type\":\"multiple_choice_vertical\",\"option_count\":1,\"has_other\":false,\"other_selected\":null,\"relative_position\":[[0,0]],\"dimensions\":[1,1],\"input_method\":null,\"is_hybrid\":false}}}},\"start_time\":{ start_time },\"end_time\":{ end_time },\"time_spent\":{ time_spent },\"previous_clicked\":false,\"has_backtracked\":false,\"bi_voice\":{{}}}}\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"is_previous\"\r\n\r\nfalse\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"disable_survey_buttons_on_submit\"\r\n\r\n\r\n-----------------------------{ boundaryNumber }--\r\n"

        res = session.post(
            SURVEY_URL, headers=headers, data=data, proxies=proxy)

        # if this string is in the reponse, the request was successful
        if("Dein Jugendwort ist jetzt bei uns aufgenommen." in res.text):
            successful_votes += 1
        else:
            failed_votes += 1
    except:
        failed_votes += 1


info_loop_stop = False


def info_msg_thread():
    global successful_votes
    global failed_votes
    global info_loop_stop

    while not info_loop_stop:
        # prints threads_running, successful_votes, failed_votes
        print(
            f"[*] Status - Erfolgreicht: { successful_votes }, Fehlgeschlagen: { failed_votes }, Laufende Vote-Threads: { len(threading.enumerate()) - 2 }.", end="\r")
        time.sleep(1)


if __name__ == "__main__":
    # init argparse
    parser = argparse.ArgumentParser(description="Ein Programm um Umfragen für die Kerle und Kerlinnen von r/ich_iel zu 'verbessern'.",
                                     epilog="Gemacht mit Python, <3 und Hurensohn. (von hallowed, wwhtrbbtt, flohlen, Flojomojo, simonnnnnnnnnn, pascaaaal, 0x0verflow).")
    parser.add_argument("-threads", type=int,
                        help="Gleichzeit ausgeführte Vote-Threads. Sowas wie ne CPU-Vergewaltigung, nur regulierbar.")
    parser.add_argument("-url", type=str,
                        help="Sollte man nicht ändern, kann man aber. Damit kann man die URL zur zu manipulierenden Umfrage bearbeiten.")
    parser.add_argument("-proxylist", type=str,
                        help="Hier kannst du deine eigene Proxylist einfügen, falls du eine besitzt.")
    parser.add_argument("-word", type=str,
                        help="Hier kannst du dein eigenes Jugendwort festlegen. Möge der stärkere gewinnen. (Du nimmst aber natürlich ~Hurensohn~ Zensurensohn, da es das beste Wort überhaupt ist!)")

    args = parser.parse_args()

    # setting args
    if args.threads:
        THREAD_COUNT = args.threads

    if args.url:
        SURVEY_URL = args.url

    if args.word:
        WORD = args.word

    # print: loading proxies
    print("[*] Lade Proxies...")
    proxies = None

    if args.proxylist:
        # proxylist from file
        proxies = get_proxies_from_proxylist(args.proxylist)
    else:
        # proxylist from proxyscrape
        proxies = get_proxies()

    # print: starting threads
    print("[*] Alles Nötige wurde vorbereitet. Lasset die Threads los!")
    # start info_msg_thread
    threading.Thread(target=info_msg_thread, args=[]).start()

    # start vote_threads
    try:
        while True:
            # +2 because the main thread and the info_msg_thread are also returned by enumerate()
            if len(list(threading.enumerate())) < THREAD_COUNT + 2:
                threading.Thread(target=vote_thread, args=[{
                    "http": choice(proxies)}]).start()
    except KeyboardInterrupt:
        # stopping programm
        # print: waiting for all threads to be stopped
        # this is really ugly... there has to be a better way to override the characters
        # i could use sys and clear the line but I don't really want to use two ways of printing
        # and I'm to lazy to swap out everything
        # also, this works perfectly
        print("[!] Warte, bis alle Threads gestoppt sind!" + 40*" ")
        
        info_loop_stop = True

        while len(threading.enumerate()) > 1:
            pass

        exit()
