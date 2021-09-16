import discord
from discord.ext import commands
import os
import main
import modmail
import levelsys
import music
import game

cogs = [main, modmail, levelsys, music, game]

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="~",
                      intents=intents, help_command=None, activity=discord.Activity(type=discord.ActivityType.competing, name="Vandyck#7726 兄ちゃん戦争"))

for cog in cogs:
    cog.setup(client)

client.run(os.environ.get('TOKEN'))
