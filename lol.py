import requests
from dotenv import load_dotenv
import os
from riotwatcher import LolWatcher, ApiError
import requests
import champs
import pandas as pd
from pandas import json_normalize 

load_dotenv()

watcher = LolWatcher(os.getenv("LOL_KEY"))

PLATFORM = "lolek"

params = {"api_key": os.getenv("LOL_KEY"), "timeout": 60, "kernel_url": "none", "rate_limiter": "Handlers.RateLimit.BasicRateLimiter", "deserializer": "Handlers.DictionaryDeserializer"}

class summonerstats:
    def __init__(self, nickname, region):
        my_region = region
        me = watcher.summoner.by_name(my_region, nickname)
        championMastery = watcher.champion_mastery.by_summoner(my_region, me["id"])
        rank = watcher.league.by_summoner(my_region, me["id"])
        self.championMasteryName1 = champs.get_champions_name(championMastery[0]["championId"])
        self.championMasteryLevel1 = championMastery[0]["championLevel"]
        self.championMasteryPoints1 = championMastery[0]["championPoints"]
        self.championMasteryLastplaytime1 = championMastery[0]["lastPlayTime"]
        self.championMasteryName2 = champs.get_champions_name(championMastery[1]["championId"])
        self.championMasteryLevel2 = championMastery[1]["championLevel"]
        self.championMasteryPoints2 = championMastery[1]["championPoints"]
        self.championMasteryLastplaytime2 = championMastery[1]["lastPlayTime"]
        self.championMasteryName3 = champs.get_champions_name(championMastery[2]["championId"])
        self.championMasteryLevel3 = championMastery[2]["championLevel"]
        self.championMasteryPoints3 = championMastery[2]["championPoints"]
        self.championMasteryLastplaytime3 = championMastery[2]["lastPlayTime"]
        self.username = me['name']
        self.icon = f"http://ddragon.leagueoflegends.com/cdn/12.23.1/img/profileicon/{me['profileIconId']}.png"
        self.summonerLevel = me['summonerLevel']
        df = json_normalize(rank,)
        flex = df[(df.queueType == "RANKED_FLEX_SR")]
        solo = df[(df.queueType == "RANKED_SOLO_5x5")]
        if not solo.empty:
            self.tier = solo.iloc[0]["tier"]
            self.rank = solo.iloc[0]["rank"]
            self.wins = solo.iloc[0]["wins"]
            self.losses = solo.iloc[0]["losses"]
            self.allGames = solo.iloc[0]["wins"] + solo.iloc[0]["losses"]
            self.winratio = ((solo.iloc[0]["wins"] / self.allGames) * 100) / 1
        if not flex.empty:
            self.tierFlex = flex.iloc[0]["tier"]
            self.rankFlex = flex.iloc[0]["rank"]
            self.winsFlex = flex.iloc[0]["wins"]
            self.lossesFlex = flex.iloc[0]["losses"]
            self.allGamesFlex = flex.iloc[0]["wins"] + flex.iloc[0]["losses"]
            self.winratioFlex = ((flex.iloc[0]["wins"] / self.allGamesFlex) * 100) / 1
        self.totalChampionMastery = watcher.champion_mastery.scores_by_summoner(my_region, me['id'])
        
    def getJSON(self):
            response = (requests.get(self, params=params)).json()
            return response