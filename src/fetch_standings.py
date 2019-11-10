from bs4 import BeautifulSoup
import requests

url = "https://www.nycgha.org/standings/show/5180440?subseason=626023"


def get_raw_standings():
    """
    Goes the NYCGHA website and fetches the latest league standings.

    :return: list-representation of the league standings
    """
    doc = requests.get(url).text
    soup = BeautifulSoup(doc, "html.parser")

    table = soup.find_all("table")[0]
    table_rows = table.find_all("tr")

    headers = [th.text.strip() for th in table_rows.pop(0).find_all("th")][2::]

    standings = {}
    for tr in table_rows:
        td = tr.find_all("td")
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        team = row.pop(0)
        if row:
            standings[team] = dict(zip(headers, row[1::]))

    standings["key"] = "teams2"

    return standings
