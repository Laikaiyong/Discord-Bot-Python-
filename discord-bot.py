import discord
from discord.ext import commands
import json
import requests
import re
import youtube_dl
import os
# import datetime
# import random
# import asyncio


# Prefix set up
def get_prefix(client, message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=get_prefix,
                      intents=intents, help_command=None)


# Join a new server and set prefix
@client.event
async def on_guild_join(guild):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "~"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)


@client.command()
@commands.has_permissions(administrator=True)
async def settings(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)

    await ctx.send(f"The prefix was changed to {prefix}.")


# # Error handling example
# @commands.command(name="kick")
# @commands.has_permissions(kick_members=True)
# async def kick(ctx, members, *, reason=None):
#     await member.kick(reason=reason)

# @kick.error
# async def kick_error(error, ctx):
#     if isinstance(error, commands.MissingPermissions):
#         owner = ctx.guild.owner
#         direct_message = await owner.create_dm()
#         await direct_message.send("Missing Permissions")

# Discord Presence
@client.event
async def on_ready():

    ''' Note
    discord.Game display playing
    discord.Streaming display streaming
    discord.Activity:
    set type = watching / listening
    '''
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Code Simping'))


# Minecraft API Thingy
@client.command()
async def minecraft(ctx, arg):
    r = requests.get('https://api.minehut.com/server/' + arg + '?byName=true')
    json_data = r.json()

    description = json_data["server"]["motd"]
    online = str(json_data["server"]["online"])
    playerCount = str(json_data["server"]["playerCount"])

    embed = discord.Embed(
        title=arg.capitalize() + " Server Info",
        description='Description: ' + description +
        '\nOnline: ' + online + '\nPlayers: ' + playerCount,
        color=discord.Color.dark_green()
    )
    embed.set_thumbnail(
        url="https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1")

    await ctx.send(embed=embed)


# Inspect users message for prefix manipulation
@client.event
async def on_message(message):

    # Avoid bot to respond to itself
    if message.author == client.user:
        return

    # Prefix manipulation
    try:

        if message.mentions[0] == client.user:

            with open("prefixes.json", "r") as read:
                prefixes = json.load(read)

            pre = prefixes[str(message.guild.id)]

            await message.channel.send(f"My prefix for {message.guild.name} is now {pre}.")

    except:
        pass

    await client.process_commands(message)


# Greetings
@client.listen('on_message')
async def greets(message):
    message.content = message.content.lower()

    # Avoid bot to respond to itself
    if message.author == client.user:
        return

    # Bot interaction (greetings)
    greetings = ["hello", "hi", "hey", "henlo", "hai", "sup"]

    for greets in greetings:
        # Bot greets back

        if re.search(rf'(\s|^){greets}(\b|$)', message.content):
            mention = message.author.mention
            greets = greets.capitalize()

            # If sender is creator
            if str(message.author) == "Vandyck#7726":
                await message.channel.send(f"All hail master, {mention}.  \U0001F647")

            # If sender is core member
            elif "core" in [y.name.lower() for y in message.author.roles]:

                await message.channel.send(f"{greets} administrator {mention} .\nI am ready at your service. \U0001F935")

            else:
                await message.channel.send(f"{greets}, {mention}!")


# Remove vulgar comment
@client.listen('on_message')
async def remove_vulgar(message):
    message.content = message.content.lower()

    # Avoid bot to respond to itself
    if message.author == client.user:
        return

    # Exception of rude message / Message auto clearing
    rude_words = ["fuck", "sohai", "cibai",
                  "diu", "dick", "boobs", "tits", "ass"]

    for rude_word in rude_words:
        # Delete inappropriate message
        if re.search(rf'(\s|^){rude_word}(\b|$)', message.content):
            await message.channel.purge(limit=1)


# Command to create modmail channel
@client.command()
async def mod_mail(ctx):
    guild = ctx.guild
    admin_role = discord.utils.get(
        guild.roles, name="Core")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    await ctx.guild.create_text_channel("\U0001F4E7-mod-mail", overwrites=overwrites)


# Mod mail
@client.listen('on_message')
async def mail_message(message):

    # Avoid bot to respond to itself
    if message.author == client.user:
        return

    empty_array = []
    modmail_channel = discord.utils.get(
        client.get_all_channels(), name="\U0001F4E7-mod-mail")
    if str(message.channel.type) == "private":

        # Check is it an attachment
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send(f"[{message.author.display_name}]")

            for file in files:
                await modmail_channel.send(file.url)
        else:
            await modmail_channel.send("[" + message.author.display_name + "]" + message.content)

    elif str(message.channel) == 'mod-mail' and message.content.startswith("<@"):
        member_object = message.mention[0]
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send(f"[{message.author.display_name}]")

            for file in files:
                await modmail_channel.send(file.url)
        else:
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]

            await member_object.send(f"[{message.author.display_name}] {mod_message}")


# Client command command
@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="KY Gor Gor commands",
        description="Here are all the command syntax available:",
        color=discord.Color.dark_gold()
    )
    embed.add_field(
        name="Prefix", value="\n```~```\nDefault prefix (can be modified)", inline=False)
    embed.add_field(
        name="Basic", value="\n```server```\nDisplay server information\n```settings```\nChange prefix for server.\n```help```\nDisplay bot commands", inline=False)
    embed.add_field(
        name="Mod Mail", value="\n```mod_mail```\nCreate a channel for moderator's mail", inline=False)
    await ctx.send(embed=embed)


# Client Server dashboard command
@ client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    id = str(ctx.guild.id)
    icon = str(ctx.guild.icon_url)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.dark_gold()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="ServerID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)


# Music Player
# Join voice channel
@client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.mention))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()


# Leave voice channel
@client.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


# Pause music
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing in the meantime.")


# Pause music
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


# Pause music
@client.command(name='Remove music', help='To make the bot remove playlist and stop in the voice channel')
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The music is playing.")


# Play music
@client.command()
async def play(ctx, url: str):
    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")

    voice_channel = ctx.message.author.voice.channel
    await voice_channel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))


client.run('ODIxMzc3MjI4Nzk3MTE2NDM2.YFC1Jw._Q8vI0Z_wkHpJsP_x60jHM954Fk')

# Run multiple dif bot in one script
# loop = asyncio.get_event_loop()


# async def create_bots():
#     await client.start('token')
#     await commander.start('token')

# loop.run_until_complete(create_bots())
