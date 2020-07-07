import threading
import requests
import time
from bs4 import BeautifulSoup
from random import randint, choice
import argparse


THREAD_COUNT = 10
SURVEY_URL = "https://www.surveymonkey.com/r/7JZRVLJ"
WORD = "Hurensohn"

successful_votes = 0
failed_votes = 0
threads_running = 0


def get_proxies() -> list:
    res = requests.get(
        "https://api.proxyscrape.com/?request=getproxies&proxytype=http", allow_redirects=True)
    print("[*] Proxylist von Proxyscrape geladen!")
    return res.text.split("\r\n")


def get_proxies_from_proxylist(path) -> list:
    f = open(path, "r")
    l = [line.rstrip("\n") for line in f]
    f.close()
    print("[*] Proxylist aus Datei geladen!")
    return l


def vote_thread(proxy):
    global successful_votes
    global failed_votes
    global threads_running
    global SURVEY_URL
    global WORD

    threads_running += 1

    try:
        # Erster Request um Kekse und einen Validierungs-String zu holen
        session = requests.Session()
        cookie_response = session.get(SURVEY_URL, proxies=proxy)
        soup = BeautifulSoup(cookie_response.text, 'html.parser')
        # Den Schlüsselwert parsieren
        csrf_token = soup.find("input", {"id": "survey_data"})["value"]
        # Eine zufällige Nummer für die Grenznummer generieren
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
        # Eine zufällige Zeit generieren, die auf der Website verbracht wird
        start_time = int(time.time()) - randint(70, 130)
        end_time = start_time + randint(50, 100)
        time_spent = end_time - start_time + 11300
        # Ein Zufälliges alter generieren
        age = randint(1, 4)
        data = f"-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"463803414\"\r\n\r\n{str(3067519627 + age - 1)}\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"463803684\"\r\n\r\n{ WORD }\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"483089934[]\"\r\n\r\n3189794655\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"survey_data\"\r\n\r\n{ csrf_token }\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"response_quality_data\"\r\n\r\n{{\"question_info\":{{\"qid_463803414\":{{\"number\":1,\"type\":\"dropdown\",\"option_count\":5,\"has_other\":false,\"other_selected\":null,\"relative_position\":[[{ age },0]],\"dimensions\":[5,1],\"input_method\":null,\"is_hybrid\":false}},\"qid_463803684\":{{\"number\":2,\"type\":\"open_ended\",\"option_count\":null,\"has_other\":false,\"other_selected\":null,\"relative_position\":null,\"dimensions\":null,\"input_method\":\"text_typed\",\"is_hybrid\":true}},\"qid_483089934\":{{\"number\":3,\"type\":\"multiple_choice_vertical\",\"option_count\":1,\"has_other\":false,\"other_selected\":null,\"relative_position\":[[0,0]],\"dimensions\":[1,1],\"input_method\":null,\"is_hybrid\":false}}}},\"start_time\":{ start_time },\"end_time\":{ end_time },\"time_spent\":{ time_spent },\"previous_clicked\":false,\"has_backtracked\":false,\"bi_voice\":{{}}}}\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"is_previous\"\r\n\r\nfalse\r\n-----------------------------{ boundaryNumber }\r\nContent-Disposition: form-data; name=\"disable_survey_buttons_on_submit\"\r\n\r\n\r\n-----------------------------{ boundaryNumber }--\r\n"

        res = session.post(
            SURVEY_URL, headers=headers, data=data, proxies=proxy)

        # Überprüfen, ob die Anfrage erfolgreich war
        if("Dein Jugendwort ist jetzt bei uns aufgenommen." in res.text):
            successful_votes += 1
        else:
            failed_votes += 1
    except:
        failed_votes += 1

    threads_running -= 1
    pass


info_loop_stop = False

def info_msg_thread():
    global threads_running
    global successful_votes
    global failed_votes
    global info_loop_stop

    while not info_loop_stop:
        # Alle 5s den Status ausgeben
        print(f"[*] Status - Erfolgreicht: { successful_votes }, Fehlgeschlagen: { failed_votes }, Laufende Threads: { threads_running }.")
        time.sleep(5)
    pass


if __name__ == "__main__":
    # Argumente festlegen
    parser = argparse.ArgumentParser(description="Ein Programm um Umfragen für die Kerle und Kerlinnen von r/ich_iel zu 'verbessern'.",
                                    epilog="Gemacht mit Python, <3 und Hurensohn. (von hallowed, wwhtrbbtt, flohlen, Flojomojo, simonnnnnnnnnn, pascaaaal, 0x0verflow (der Typ vom @HusoBot)).")
    parser.add_argument("-threads", type=int,
                        help="Gleichzeit ausgeführte Threads. Sowas wie ne CPU-Vergewaltigung, nur regulierbar.")
    parser.add_argument("-url", type=str,
                        help="Sollte man nicht ändern, kann man aber. Damit kann man die URL zur zu manipulierenden Umfrage bearbeiten.")
    parser.add_argument("-proxylist", type=str,
                        help="Hier kannst du deine eigene Proxylist einfügen, falls du eine besitzt.")
    parser.add_argument("-word", type=str,
                        help="Hier kannst du dein eigenes Jugendwort festlegen. Möge der stärkere gewinnen. (Du nimmst aber natürlich ~Hurensohn~ Schabernack, da es das beste Wort überhaupt ist!)")

    args = parser.parse_args()

    # Argumente (falls vorhanden) einsetzen
    if args.threads:
        THREAD_COUNT = args.threads

    if args.url:
        SURVEY_URL = args.url

    if args.word:
        WORD = args.word
        
    print("[*] Lade Proxies...")
    proxies = None

    if args.proxylist:
        # Proxyliste aus Datei holen
        proxies = get_proxies_from_proxylist(args.proxylist)
    else:
        # Proxyliste von proxyscrape.com holen
        proxies = get_proxies()

    print("[*] Alles Nötige wurde vorbereitet. Lasset die Threads los!")
    # Informations-Thread starten
    threading.Thread(target=info_msg_thread, args=[]).start()

    # Abstimm-Threads starten (try um Programm beenden zu können)
    try:
        while True:
            # +1 weil der Hauptthread auch von enumerate() zurückgegeben wird
            if len(list(threading.enumerate())) < THREAD_COUNT + 1:
                threading.Thread(target=vote_thread, args=[{
                                "http": choice(proxies)}]).start()
    except KeyboardInterrupt:
        # Programm sachte beenden
        print("[!] Warte, bis alle Threads gestoppt sind!")
        info_loop_stop = True

        while threading.enumerate() > 1:
            pass
        
        exit()
    pass
