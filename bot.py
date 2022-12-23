from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
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