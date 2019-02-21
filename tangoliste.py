# j = 0 -> Wochentag, [Mo, Di, Mi, Do, Fr, Sa, So]
# j = 1 -> Angabe über Regelmäßigkeit. Kann Zahl sein (jeden xten yTag oder eine Reihe von Datumsangaben)
# j = 2 -> Stadt, z.B. Köln
# j = 3 -> Lokal, z.B. La Pista
# j = 4 -> Uhrzeit, zB. 20-23:30
# j = 5 -> Hinweis, zB. Küche
# j = 6 -> Kontakt, zB Müller 0123/1234567
# j = 7 -> Kosten, zB 7,-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("https://www.tango-ruhrgebiet.de/liste.html")
bs = BeautifulSoup(html.read(), "html.parser")

data = []

class Milonga:
    weekday: str = ""
    roto: str = ""
    city: str = ""
    location: str = ""
    time: str = ""
    hint: str = ""
    contact: str = ""
    cost: str = ""

data = []

for currentColumn, tr in enumerate(bs.find_all("tr")):
    milonga = Milonga()
    for currentRow, td in enumerate(tr.find_all("td", {'bgcolor' : '#f0f0f0'})):
        if not td.text == "":
            cleanedRecord = td.text.replace(u'\xa0', u' ').replace("\n", "").replace("\r", "").replace("\t", " ").strip()
            tableRecord = " ".join(cleanedRecord.split())
            if currentRow == 0:
                milonga.weekday = cleanedRecord[:2]

            if currentRow == 1:
                rotoMatch = "Jeden \d{1,2}\. \w"
                milonga.roto = tableRecord

            if currentRow == 2:
                milonga.city = tableRecord

            if currentRow == 3:
                milonga.location = tableRecord

            if currentRow == 4:
                milonga.time = tableRecord

            if currentRow == 5:
                if tableRecord == "":
                    milonga.hint = "kein Hinweis"
                else:
                    milonga.hint = tableRecord

            if currentRow == 6:
                milonga.contact = tableRecord
                data.append(milonga)

            if currentRow == 7:
                milonga.cost = tableRecord

    # prüfen, ob wirklich Milonga. Zuverlässig zu erkennen daran, ob im 7ten Feld ein Regex passt.

    regex = "\d,-|[n,N]ix|[s,S]pende]"

    pattern = re.compile(regex)
    if pattern.match(milonga.cost):
        data.append(milonga)


for milonga in data:
    print("Milonga: {0} ({1}), in {2} im {3} für {4} Zeit: {5}. Hinweis: {6}. Auskunft gibt: {7}".format(milonga.weekday, milonga.roto, milonga.city, milonga.location, milonga.cost, milonga.time, milonga.hint, milonga.contact))
