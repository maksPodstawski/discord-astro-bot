import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

PLATFORM = "steam"

headers = {'TRN-Api-Key': os.getenv("API_KEY"), 'Accept': 'application/json', 'Accept-Encoding': 'gzip'}


class csgoUser:
    def __init__(self, steamID):
        self.response = None
        self.url = f"https://public-api.tracker.gg/v2/csgo/standard/profile/{PLATFORM}/{steamID}"
        self.allStats = self.getJSON()
        if self.response == 200:
            self.username = self.allStats["data"]["platformInfo"]["platformUserHandle"]
            self.avatarURL = self.allStats["data"]["platformInfo"]["avatarUrl"]
            self.playtime = self.allStats["data"]["segments"][0]["stats"]["timePlayed"]["displayValue"]
            self.kills = self.allStats["data"]["segments"][0]["stats"]["kills"]["displayValue"]
            self.deaths = self.allStats["data"]["segments"][0]["stats"]["deaths"]["displayValue"]
            self.kdratio = self.allStats["data"]["segments"][0]["stats"]["kd"]["displayValue"]
            self.damage = self.allStats["data"]["segments"][0]["stats"]["damage"]["displayValue"]
            self.headshots = self.allStats["data"]["segments"][0]["stats"]["headshots"]["displayValue"]
            self.shotsaccuracy = self.allStats["data"]["segments"][0]["stats"]["shotsAccuracy"]["displayValue"]
            self.bombsPlanted = self.allStats["data"]["segments"][0]["stats"]["bombsPlanted"]["displayValue"]
            self.bombsDefused = self.allStats["data"]["segments"][0]["stats"]["bombsDefused"]["displayValue"]
            self.mvp = self.allStats["data"]["segments"][0]["stats"]["mvp"]["displayValue"]
            self.wins = self.allStats["data"]["segments"][0]["stats"]["wins"]["displayValue"]
            self.matchesPlayed = self.allStats["data"]["segments"][0]["stats"]["matchesPlayed"]["displayValue"]
            self.losses = self.allStats["data"]["segments"][0]["stats"]["losses"]["displayValue"]
            self.roundsPlayed = self.allStats["data"]["segments"][0]["stats"]["roundsPlayed"]["displayValue"]
            self.wlPercentage = self.allStats["data"]["segments"][0]["stats"]["wlPercentage"]["displayValue"]
            self.headshotPct = self.allStats["data"]["segments"][0]["stats"]["headshotPct"]["displayValue"]

    def getJSON(self):
        response = requests.get(self.url, headers=headers)
        self.response = response.status_code
        json_response = response.json()
        return json_response

