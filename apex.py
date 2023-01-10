import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

params = {'TRN-Api-Key': os.getenv("API_KEY"), 'Accept': 'application/json', 'Accept-Encoding': 'gzip'}


class apexstats:
    def __init__(self, platform, nickname):
        self.response = None
        self.url = f"https://public-api.tracker.gg/v2/apex/standard/profile/{platform}/{nickname}"
        self.allStats = self.getJSON()
        if self.response == 200:
            self.avatarUrl = self.allStats["data"]["platformInfo"]["avatarUrl"]
            self.level = self.allStats["data"]["segments"][0]["stats"]["level"]["displayValue"]
            try:
                self.kills = self.allStats["data"]["segments"][0]["stats"]["kills"]["displayValue"]
            except:
                self.kills = "No data"
            try:
                self.killsAsLeader = self.allStats["data"]["segments"][0]["stats"]["killsAsKillLeader"]["displayValue"]
            except:
                self.killsAsLeader = "No data"
            try:
                self.damage = self.allStats["data"]["segments"][0]["stats"]["damage"]["displayValue"]
            except:
                self.damage = "No data"
            try:
                self.headshots = self.allStats["data"]["segments"][0]["stats"]["headshots"]["displayValue"]
            except:
                self.headshots = "No data"
            try:
                self.rangIMG = self.allStats["data"]["segments"][0]["stats"]["rankScore"]["metadata"]["iconUrl"]
            except:
                self.rangIMG = "No data"
            try:
                self.rankName = self.allStats["data"]["segments"][0]["stats"]["rankScore"]["metadata"]["rankName"]
            except:
                self.rankName = "No data"
            try:
                self.rankValue = self.allStats["data"]["segments"][0]["stats"]["rankScore"]["displayValue"]
            except:
                self.rankValue = "No data"
            try:
                self.arenaRangIMG = self.allStats["data"]["segments"][0]["stats"]["arenaRankScore"]["metadata"]["iconUrl"]
            except:
                self.arenaRangIMG = "No data"
            try:
                self.arenaRankName = self.allStats["data"]["segments"][0]["stats"]["arenaRankScore"]["metadata"]["rankName"]
            except:
                self.arenaRankName = "No data"
            try:
                self.arenaRankValue = self.allStats["data"]["segments"][0]["stats"]["arenaRankScore"]["displayValue"]
            except:
                self.arenaRankValue = "No data"
            try:
                self.peakRangIMG = self.allStats["data"]["segments"][0]["stats"]["peakRankScore"]["metadata"]["iconUrl"]
            except:
                self.peakRangIMG = "No data"
            try:
                self.peakRankName = self.allStats["data"]["segments"][0]["stats"]["peakRankScore"]["metadata"]["rankName"]
            except:
                self.peakRankName = "No data"
            try:
                self.peakRankValue = self.allStats["data"]["segments"][0]["stats"]["peakRankScore"]["displayValue"]
            except:
                self.peakRankValue = "No data"


    def getJSON(self):
        response = requests.get(self.url, headers=params)
        self.response = response.status_code
        json_response = response.json()
        return json_response
