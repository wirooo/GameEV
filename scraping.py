from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

@dataclass
class ChampStats:
    wr: float
    games: int

class UggChampScraper:
    champion: str
    url: str
    page_content: str
    soup: BeautifulSoup

    def __init__(self, champion: str) -> None:
        self.champion = champion
        self.url = f"https://u.gg/lol/champions/{champion}/build"
        self.page_content = requests.get(self.url).content
        self.soup = BeautifulSoup(self.page_content, "html.parser")

    def get_stats(self) -> ChampStats:
        content = self.soup.find("div", class_="content-section")
        wr_s = content.find("div", class_="win-rate").find("div", class_="value").text
        games_s = content.find("div", class_="matches").find("div", class_="value").text
        wr = float(wr_s[:-1]) / 100
        games = int(games_s.replace(",", ""))
        return ChampStats(wr, games)

    def get_matchup_stats(self, matchup: str) -> ChampStats:
        matchup = matchup.lower().strip()
        url = f"https://u.gg/lol/champions/{self.champion}/matchups"
        page_content = requests.get(url).content
        soup = BeautifulSoup(page_content, "html.parser")
        table = soup.find("div", class_="rt-table")
        rows = table.find("div", class_="rt-tbody").find_all("div", attrs={"class": "rt-tr-group", "role": "rowgroup"})
        for row in rows:
            champ = row.find("div", attrs={"class": "champion-name"}).text.lower().strip()
            if champ == matchup:
                matchup_wr = float(row.find("div", attrs={"class": "winrate"}).text[:-1]) / 100
                matchup_games = int(row.find_all("div", attrs={"class": "rt-td"})[-1].text.replace(",", ""))
                return ChampStats(matchup_wr, matchup_games)
        raise RuntimeError("Couldn't find champ")

    def get_duo_stats(self, duo: str) -> ChampStats:
        duo = duo.lower().strip()
        url = f"https://u.gg/lol/champions/{self.champion}/duos"
        page_content = requests.get(url).content
        soup = BeautifulSoup(page_content, "html.parser")
        table = soup.find("div", class_="rt-table")
        rows = table.find("div", class_="rt-tbody").find_all("div", attrs={"class": "rt-tr-group", "role": "rowgroup"})
        for row in rows:
            champ = row.find("div", attrs={"class": "champion"}).text.lower().strip()
            if champ == duo:
                duo_wr = float(row.find("div", attrs={"class": "winrate"}).text[:-1]) / 100
                duo_games = int(row.find_all("div", attrs={"class": "rt-td"})[-1].text.replace(",", ""))
                return ChampStats(duo_wr, duo_games)
        raise RuntimeError("Couldn't find champ")

