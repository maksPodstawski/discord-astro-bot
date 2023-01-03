# coding: ISO-8859-1
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from csgoUser import csgoUser
from tarkov import get_item_data
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name= "clear", description= "Select the number of messages to clear", guild=discord.Object(id=1034080877615001670))
@commands.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.send_message(f"chat vacuuming in progress")
    await interaction.channel.purge(limit=amount+1)


@tree.command(name= "clearuser", description= "select the user whose messages you want to delete and enter the number of messages", guild=discord.Object(id=1034080877615001670))
@commands.has_permissions(manage_messages=True, manage_roles=True)
async def clearuser(interaction: discord.Interaction, user: discord.User, amount: int):
  def check(m):
    return m.author == user
  await interaction.response.send_message(f"chat vacuuming in progress")
  await interaction.channel.purge(limit=amount+1, check=check)
  await interaction.channel.purge(limit=1)


@tree.command(name="csgostats", description="See Your stats in CS GO", guild=discord.Object(id=1034080877615001670))
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

        

@tree.command(name= "price", description= "Check the price of Escape from Tarkov items", guild=discord.Object(id=1034080877615001670))
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
        embed.add_field(name="Price:", value=f'{format_price}{currency}\n(lowest price)', inline=True)
        embed.add_field(name="Price Per Slot:", value=f'{format_priceperslot}{currency}\n({slots}{slots1})', inline=True)
        embed.add_field(name="Price Difference:", value=f'48h change:\n{item_last48}% ', inline=True)
        embed.set_footer(text="Data povided by: https://tarkov.dev/api/")
        await interaction.response.send_message(embed=embed, view=view)
    except:
        embed = discord.Embed(title=f"ERROR 404: NOT FOUND", color=0x00bfff)
        embed.add_field(name=f'Item {search} do not exist', value=f'You probably made a typo, please try again', inline=True)
        embed.set_footer(text=f'Data povided by: https://tarkov.dev/api/')
        await interaction.response.send_message(embed=embed)
        




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
