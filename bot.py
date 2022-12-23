from dotenv import load_dotenv
import discord
from discord import app_commands
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



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