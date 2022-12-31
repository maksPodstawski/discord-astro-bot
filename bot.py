from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ui import Button, View
from csgoUser import csgoUser
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="csgostats", description="See Your stats in CS GO", guild=discord.Object(id=1034080877615001670))
async def command(interaction: discord.Interaction, id: str):
    player = csgoUser(id)
    try:
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
        await interaction.response.send_message(embed=embed, view=view)

    except:
        await interaction.response.send_message(
            f'User with given id {id} does not exist or was misspelled,\n if you cant find your steam id, use the '
            f'information here https://help.steampowered.com/en/faqs/view/2816-BE67-5B69-0FEC')

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1034080877615001670))
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
