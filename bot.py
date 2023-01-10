# coding: ISO-8859-1
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from csgoUser import csgoUser
from apex import apexstats
from tarkov import get_item_data
from tarkov import get_tier
from datetime import datetime
from riot import summonerstats, tftstats
import os
from enum import Enum

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name= "clear", description= "Select the number of messages to clear")
@commands.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.send_message(f"chat vacuuming in progress")
    await interaction.channel.purge(limit=amount+1)


@tree.command(name= "clearuser", description= "Select the user whose messages you want to delete and enter the number of messages")
@commands.has_permissions(manage_messages=True, manage_roles=True)
async def clearuser(interaction: discord.Interaction, user: discord.User, amount: int):
  def check(m):
    return m.author == user
  await interaction.response.send_message(f"chat vacuuming in progress")
  await interaction.channel.purge(limit=amount+1, check=check)
  await interaction.channel.purge(limit=1)


@tree.command(name="csgostats", description="See Your stats in CS GO")
async def command(interaction: discord.Interaction, id: str):

    try:
        player = csgoUser(id)
        button = Button(label="Steam", style=discord.ButtonStyle.green, url=f"https://steamcommunity.com/id/{id}/")
        view = View()
        view.add_item(button)
        embed = discord.Embed(title=f"Nick: {player.username}", color=0x00bfff)
        embed.set_thumbnail(url=player.avatarURL)
        embed.add_field(name="Time in game:", value=f"{player.playtime}", inline=False)
        embed.add_field(name="Total amount of kills:", value=f"{player.kills}", inline=False)
        embed.add_field(name="Total amount of deaths:", value=f"{player.deaths}", inline=False)
        embed.add_field(name="KD:", value=f"{player.kdratio}", inline=False)
        embed.add_field(name="Shots accuracy:", value=f"{player.shotsaccuracy}", inline=False)
        embed.add_field(name="Bombs Planted:", value=f"{player.bombsPlanted}", inline=False)
        embed.add_field(name="Bombs Defused:", value=f"{player.bombsDefused}", inline=False)
        embed.add_field(name="Amount of mvp:", value=f"{player.mvp}", inline=False)
        embed.add_field(name="Rounds won:", value=f"{player.wins}", inline=False)
        embed.add_field(name="Matches Played:", value=f"{player.matchesPlayed}", inline=False)
        embed.add_field(name="Rounds Lost:", value=f"{player.losses}", inline=False)
        embed.add_field(name="Rounds Played:", value=f"{player.roundsPlayed}", inline=False)
        embed.add_field(name="Win Percentage:", value=f"{player.wlPercentage}", inline=False)
        embed.add_field(name="Percentage of headshots:", value=f"{player.headshotPct}", inline=False)
        embed.set_footer(text=f'Data povided by: https://tracker.gg/csgo')
        await interaction.response.send_message(embed=embed, view=view)
    except:
        button = Button(label="How to get a STEAM_ID", style=discord.ButtonStyle.green, url=f"https://help.steampowered.com/en/faqs/view/2816-BE67-5B69-0FEC")
        view = View()
        view.add_item(button)
        embed = discord.Embed(title=f"ERROR 404: NOT FOUND", color=0x00bfff)
        embed.add_field(name=f'User with given id {id} do not exist', value=f'You probably made a typo, please try again', inline=True)
        embed.add_field(name="Problem with getting yours STEAM_ID?", value=f"Just click the button below!", inline=False)
        embed.set_footer(text=f'Data povided by: https://tracker.gg/csgo')
        await interaction.response.send_message(embed=embed, view=view)

@tree.command(name= "tier", description= "Tiers are assigned using slot price identification")
async def tier(interaction: discord.Interaction):
    currency = "\u20BD"
    greaterorequal = '\u2265'
    embed = discord.Embed(title=f"Loot Tiers", color=0x00bfff)
    embed.add_field(name=":star:Legendary", value=f"{greaterorequal} 40�000{currency}", inline=False)
    embed.add_field(name=":green_circle:Great", value=f"{greaterorequal} 30�000{currency}", inline=False)
    embed.add_field(name=":yellow_circle:Average", value=f"{greaterorequal} 20�000{currency}", inline=False)
    embed.add_field(name=":red_circle:Poor", value=f"{greaterorequal} 10�000{currency}", inline=False)
    embed.add_field(name=":x:Trash", value=f"< 10 000{currency}",  inline=False)
    await interaction.response.send_message(embed=embed)      

@tree.command(name= "price", description= "Check the price of Escape from Tarkov items")
async def command(interaction: discord.Interaction,search: str):
    try:
        currency = "\u20BD"
        item_data = get_item_data(search)
        item_name = item_data['name']
        item_price = item_data['low24hPrice']
        item_last48 =item_data['changeLast48hPercent']
        item_icon = item_data['iconLink']
        item_link = item_data['wikiLink']
        item_width = item_data['width']
        item_height = item_data['height']
        item_update = item_data['updated']
        date = datetime.fromisoformat(item_update)
        formatted_date = date.strftime("%d %B %Y, %H:%M:%S")
        slots = item_width*item_height
        price_perslot = item_price//slots
        slots1 = "slots"
        format_price = format(item_price,',')
        format_priceperslot = format(price_perslot, ',')
        if slots == 1:
            slots1 = "slot"
        button = Button(label="TarkovWiki", style=discord.ButtonStyle.green, url=item_link)
        view = View()
        view.add_item(button)
        embed = discord.Embed(title=f"{item_name}", color=0x00bfff)
        embed.set_thumbnail(url=item_icon)
        embed.add_field(name="Price:", value=f' > {format_price}{currency}\n > (lowest price)', inline=True)
        embed.add_field(name="Per Slot:", value=f' > {format_priceperslot}{currency}\n > ({slots} {slots1})', inline=True)
        embed.add_field(name="Difference:", value=f' > 48h change:\n > {item_last48}% ', inline=True)
        embed.add_field(name="Tier:", value=get_tier(price_perslot), inline=False)
        embed.add_field(name="Last update:", value=formatted_date, inline=False)
        embed.set_footer(text="Data povided by: https://tarkov.dev/api/")
        await interaction.response.send_message(embed=embed, view=view)
    except:
        embed = discord.Embed(title=f"ERROR 404: NOT FOUND", color=0x00bfff)
        embed.add_field(name=f'Item {search} do not exist', value=f'You probably made a typo, please try again', inline=True)
        embed.set_footer(text=f'Data povided by: https://tarkov.dev/api/')
        await interaction.response.send_message(embed=embed)

class regions(Enum):
    EUNE = "EUN1"
    EUW = "EUW1"
    NA = "NA1"
    Brazil = "BR1"
    Japan = "JP1"
    Oceania = "OC1"   
    Russia = "RU"
    Turkey = "TR1"
    Koeran = "KR"
 
@tree.command(name="summonerstats", description="See your stats in League of Legends")
async def command(interaction: discord.Interaction, nickname: str, region: regions):
    try:
        player = summonerstats(nickname, region.value) 
        view = View()
        embed = discord.Embed(title=f"Nick: {player.username}", color=0x00bfff)
        embed.set_thumbnail(url=player.icon)
        ts1 = int(f'{player.championMasteryLastplaytime1}')
        ts2 = int(f'{player.championMasteryLastplaytime2}')
        ts3 = int(f'{player.championMasteryLastplaytime3}')
        ts1 /= 1000
        ts2 /= 1000
        ts3 /= 1000
        date1 = datetime.utcfromtimestamp(ts1).strftime('%d-%m-%Y')
        date2 = datetime.utcfromtimestamp(ts2).strftime('%d-%m-%Y')
        date3 = datetime.utcfromtimestamp(ts3).strftime('%d-%m-%Y')
        embed.add_field(name="Summoner level:", value=f"{player.summonerLevel}", inline=False)
        if hasattr(player,'tier') != 0:
            embed.add_field(name="Rank Solo/Duo:", value=f"{player.tier} {player.rank}\n\n **Wins:** {player.wins}\n **Losses:** {player.losses}\n **All Games:** {player.allGames}\n **Winratio:** {round(player.winratio,2)}%",inline=True)
        if hasattr(player,'tierFlex') != 0:
            embed.add_field(name="Rank Flex:", value=f"{player.tierFlex} {player.rankFlex}\n\n **Wins:** {player.winsFlex}\n **Losses:** {player.lossesFlex}\n **All Games:** {player.allGamesFlex}\n **Winratio:** {round(player.winratioFlex,2)}%",inline=True)
        embed.add_field(name="Total mastery points:", value=f"{player.totalChampionMastery}", inline=False)
        embed.add_field(name="***Top 3 champions by mastery points:***", value="\u200b", inline=False)
        embed.add_field(name=f"**Top 1**", value=f"> **Name:**\n>  {player.championMasteryName1}\n> **Lvl:** {player.championMasteryLevel1}\n> **Mastery Points:**\n> {format(player.championMasteryPoints1,',')}\n> **Last played in:** {date1}",inline=True)
        embed.add_field(name=f"**Top 2**", value=f"> **Name:**\n> {player.championMasteryName2}\n> **Lvl:** {player.championMasteryLevel2}\n> **Mastery Points:**\n> {format(player.championMasteryPoints2,',')}\n> **Last played in:** {date2}",inline=True)
        embed.add_field(name=f"**Top 3**", value=f"> **Name:**\n> {player.championMasteryName3}\n> **Lvl:** {player.championMasteryLevel3}\n> **Mastery Points:**\n> {format(player.championMasteryPoints3,',')}\n> **Last played in:** {date3}",inline=True)
        embed.add_field(name="Data povided by:", value = "https://www.leagueoflegends.com/", inline=False)
        await interaction.response.send_message(embed=embed, view=view)
    except:
        view = View()
        embed = discord.Embed(title="ERROR 404: NOT FOUND", color=0x00bfff)
        embed.add_field(name=f"User {nickname} on region {region.name} do not exist", value="Check the spelling, or try with other region", inline=False)
        embed.set_footer(text="Data povided by: https://www.leagueoflegends.com/")
        await interaction.response.send_message(embed=embed, view=view)

@tree.command(name="tftstats", description="See your stats in Teamfight Tactics")
async def command(interaction: discord.Interaction, nickname: str, region: regions):
    try:
        player = tftstats(nickname, region.value)
        view = View()
        embed = discord.Embed(title=f"Nick: {player.tftUsername}", color=0x00bfff)
        embed.set_thumbnail(url=player.tftIcon)
        embed.add_field(name="Summoner level:", value=f"{player.tftSummonerLevel}", inline=False)
        if hasattr(player,'tftTier') != 0:
            embed.add_field(name="Rank Solo:", value=f"{player.tftTier} {player.tftRank}\n\n> **Wins:** {player.tftWins}\n> **Losses:** {player.tftLosses}\n> **All Games:** {player.tftAllGames}\n> **Winratio:** {round(player.tftWinratio,2)}%",inline=True)
        if hasattr(player,'tftTurboTier') != 0:    
            embed.add_field(name="Rank Turbo:", value=f"{player.tftTurboTier} {player.tftTurboRank}\n\n> **Wins:** {player.tftTurboWins}\n> **Losses:** {player.tftTurboLosses}\n> **All Games:** {player.tftTurboAllGames}\n> **Winratio:** {round(player.tftTurboWinratio,2)}%",inline=True)
        if hasattr(player,'tftDoubleTier') != 0:    
            embed.add_field(name="Rank Double:", value=f"{player.tftDoubleTier} {player.tftDoubleRank}\n\n> **Wins:** {player.tftDoubleWins}\n> **Losses:** {player.tftDoubleLosses}\n> **All Games:** {player.tftDoubleAllGames}\n> **Winratio:** {round(player.tftDoubleWinratio,2)}%",inline=True)
        embed.add_field(name="Data povided by:", value = "https://developer.riotgames.com/", inline=False)
        await interaction.response.send_message(embed=embed, view=view)
    except:
        view = View()
        embed = discord.Embed(title="ERROR 404: NOT FOUND", color=0x00bfff)
        embed.add_field(name=f"User {nickname} on region {region.name} do not exist", value="Check the spelling, or try with other region", inline=False)
        embed.set_footer(text="Data povided by: https://developer.riotgames.com/")
        await interaction.response.send_message(embed=embed, view=view)   

class ApexPlatforms(Enum):
    Origin = "origin"
    XboxLive = "xbl"
    PlayStationNetwork = "psn"

@tree.command(name="apexstats", description="See your stats in Apex")
async def command(interaction: discord.Interaction, nickname: str, platform: ApexPlatforms):
    apexPlayer = apexstats(platform=platform.value, nickname=nickname)
    print(apexPlayer.response)
    if apexPlayer.response == 200:
        view = View()
        apexPlayer = apexstats(platform=platform.value, nickname=nickname)
        embed = discord.Embed(title=f"{nickname}", color=0x00bfff)
        embed.set_thumbnail(url=apexPlayer.avatarUrl)
        embed.add_field(name="Kills: ", value=apexPlayer.kills, inline=True)
        embed.add_field(name="Level: ", value=apexPlayer.level, inline=True)
        embed.add_field(name="Damage: ", value=apexPlayer.damage, inline=True)
        embed.add_field(name=f"**Ranked**", value=f"> **Rank:**\n>  {apexPlayer.rankName}\n> **MMR:**\n> {apexPlayer.rankValue}\n", inline=True)
        embed.add_field(name=f"**Arena**", value=f"> **Rank:**\n>  {apexPlayer.arenaRankName}\n> **MMR:**\n> {apexPlayer.arenaRankValue}\n", inline=True)
        embed.add_field(name=f"**Ranked peak**", value=f"> **Rank peak:**\n>  {apexPlayer.peakRankName}\n> **MMR peak:**\n> {apexPlayer.peakRankValue}\n", inline=True)
        embed.set_footer(text="Data povided by: https://tracker.gg/apex")
        await interaction.response.send_message(embed=embed, view=view)

    else:
        view = View()
        embed = discord.Embed(title="ERROR 404: NOT FOUND", color=0x00bfff)
        embed.add_field(name=f"User {nickname} on platform {platform.name} do not exist", value="Check the spelling, or try with other platform", inline=False)
        embed.set_footer(text="Data povided by: https://tracker.gg/apex")
        await interaction.response.send_message(embed=embed, view=view)

@tree.command(name="help", description="Help for all commands")
async def command(interaction: discord.Interaction):
    view = View()
    embed = discord.Embed(title="Help", color=0x00bfff)
    embed.add_field(name="/clear", value="Clearing specific amount of messages", inline=False)
    embed.add_field(name="/clearuser", value="Select the user whose messages you want to delete and enter the number of messages", inline=False)
    embed.add_field(name="/csgostats", value="See Your stats in Counter Strike Global Offensive", inline=False)
    embed.add_field(name="/price", value="Check the price of Escape from Tarkov items", inline=False)
    embed.add_field(name="/tier", value="Tiers are assigned using slot price identification used in price command", inline=False)
    embed.add_field(name="/summonerstats", value="See your stats in League of Legends", inline=False)
    embed.add_field(name="/tftstats", value="See your stats in Teamfight Tactics", inline=False)
    embed.add_field(name="/apexstats", value="See your stats in Apex", inline=False)
    embed.add_field(name="/weather", value="See weather in specific city", inline=False)
    await interaction.response.send_message(embed=embed, view=view)

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(status=discord.Status.online, activity=discord.Game("/help"))
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: {user_message} on: {channel}")


client.run(os.getenv("TOKEN"))
