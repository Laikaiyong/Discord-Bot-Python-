import discord
from discord.ext import commands
import json
import requests
import re
import youtube_dl
import os
import random as rd
from PIL import Image, ImageFont, ImageDraw
from pymongo import MongoClient


# Prefix set up
def get_prefix(client, message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=get_prefix,
                      intents=intents, help_command=None, activity=discord.Activity(type=discord.ActivityType.competing, name="Vandyck#7726 兄ちゃん戦争"))


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


# Welcome Card
@client.event
async def on_member_join(member):
    guild = client.get_guild(852085478659457035)
    channel = guild.get_channel(852085478659457042)
    member_count = guild.member_count

    img = Image.open("Pynata Cover.png")
    img = img.copy()

    member_im = Image.open(requests.get(member.avatar_url, stream=True).raw)
    member_im = member_im.resize((310, 300), Image.LANCZOS)

    img.paste(member_im, (int(1150/3)+25, int(669/4)))
    msg = "Welcome " + member.name + " (Member " + str(member_count) + ")"
    draw = ImageDraw.Draw(img)
    chunk_five = ImageFont.truetype("Chunk Five Print.otf", 60)
    w, h = draw.textsize(msg, font=chunk_five)
    draw.text(((1150-w)/2, (669-h)/8*7), msg, fill="black", font=chunk_five)
    img.save("new.png", "PNG")

    await channel.send(f"Welcome to the server {member.mention}! :partying_face:\n:one: Check out <#{852088286922801193}> to redeem membership :white_check_mark:\n:two: Stay updated on events in <#{856440780164169738}> :fireworks:\n:three: Customize your unique role in <#{852111666716213258}> :scroll:\n:four: Get useful resources in <#{852101645836091472}> on your developing journey :person_climbing:\n", file=discord.File("new.png"))

    for channel in member.guild.channels:
        if channel.name.startswith('Peep'):
            await channel.edit(name=f'Peep: {sum(client.user)}')
            break


# Reaction Role
@client.command(aliases=['rr'])
async def reactrole(ctx, message: discord.Message, emoji, role: discord.Role):
    if message != None and emoji != None and role != None:
        await message.add_reaction(emoji)

        with open('reactrole.json') as f:
            data = json.load(f)

        new = dict()
        new['emoji'] = emoji.name
        new['role'] = role

        data.append(new)

        with open('reactrole.json', 'w') as f:
            json.dump(data, f)

    else:
        await ctx.send("Invalid argument. (e.g. ~reactrole message_id :emoji: @role")


@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    elif int(payload.message_id) in [860046847519621180, 860140723131252786, 860140829100343306, 856834763545378836]:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        with open("reactrole.json") as f:
            data = json.load(f)

            for info in data:
                if info["emoji"] == payload.emoji.name:
                    role = discord.utils.get(guild.roles, name=info["role"])
                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    if int(payload.message_id) in [860046847519621180, 860140723131252786, 860140829100343306, 856834763545378836]:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        with open("reactrole.json") as f:
            data = json.load(f)
            for info in data:
                if info["emoji"] == payload.emoji.name:
                    role = discord.utils.get(guild.roles, name=info["role"])
                    await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


# Minecraft API Thingy
@ client.command()
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
@ client.event
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


# Remove vulgar and Respond Greetings
@ client.listen('on_message')
async def vulgar(message):
    message.content = message.content.lower()

    # Avoid bot to respond to itself
    if message.author == client.user:
        return

    # Exception of rude message / Message auto clearing
    rude_words = ["fuck", "sohai", "cibai",
                  "diu", "dick", "boobs", "tits", "ass"]

    # Delete inappropriate message
    for rude_word in rude_words:
        if re.search(rf'(\s|^){rude_word}(\b|$)', message.content):
            await message.delete()
        break


# Greets
@ client.listen('on_message')
async def vulgar(message):

    # Bot interaction (greetings)
    greetings = ["hello", "hi", "hey", "henlo", "hai", "sup"]

    message.content = message.content.lower()

    # Avoid bot to respond to itself
    if message.author == client.user:
        return

    for greets in greetings:
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


# React to specific message
@ client.listen('on_message')
async def emote_react(message):
    nice_words = ['nice', 'noice', 'nais', 'nices', 'nicess']

    for word in nice_words:
        if re.search(rf'(\s|^){word}(\b|$)', message.content):
            await message.add_reaction("<:noice:859666087216676884>")


# Nominate command
@ client.command(aliases=['nom'])
async def nominate(message):
    users = [
        member for member in message.channel.members if "bots" not in [y.name.lower() for y in member.roles] and member != str(message.author)]
    user = rd.choice(users)
    await message.channel.send(user.mention + " had been nominated.")


# Command to create modmail channel
@ client.command()
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
@ client.listen('on_message')
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
            await modmail_channel.send(f"[{message.author.name}]")

            for file in files:
                await modmail_channel.send(file.url)
        else:
            await modmail_channel.send("[" + message.author.name + "] " + message.content)

    elif str(message.channel) == 'mod-mail' and message.content.startswith("<@"):
        member_object = message.mention[0]
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send(f"[{message.author.name}]")

            for file in files:
                await modmail_channel.send(file.url)
        else:
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]

            await member_object.send(f"[{message.author.name}] {mod_message}")


# Client help command
@ client.command()
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
@ client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.mention))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()


# Leave voice channel
@ client.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


# Pause music
@ client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing in the meantime.")


# Pause music
@ client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


# Pause music
@ client.command(name='Remove music', help='To make the bot remove playlist and stop in the voice channel')
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The music is playing.")


# Play music
@ client.command(aliases=['p'])
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

# Tic Tac Toe
player_one = ""
player_two = ""
turn = ""
game_over = True
board = []

winning_condition = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@ client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player_one
    global player_two
    global turn
    global game_over

    if game_over:
        global board
        board = [
            "\U00002B1C", "\U00002B1C", "\U00002B1C", "\U00002B1C", "\U00002B1C", "\U00002B1C", "\U00002B1C", "\U00002B1C", "\U00002B1C"]
        turn = ""
        game_over = False
        count = 0

        player_one = p1
        player_two = p2

        line = ""
        for index in range(len(board)):
            if index in [2, 5, 8]:
                line += " " + board[index]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[index]

        num = rd.randint(1, 2)
        if num == 1:
            turn = player_one
            await ctx.send(f"It is {player_one.mention}'s turn.")
        elif num == 2:
            turn = player_two
            await ctx.send(f"It is {player_two.mention}'s turn.")
    else:
        await ctx.send("A game is already in progress. Finish it before starting anew one. \U0001F3AE")


@ client.command()
async def place(message, pos: int):
    global turn
    global player_one
    global player_two
    global board
    global count
    global game_over

    if not game_over:
        mark = ""
        if turn == player_one and message.author == player_one:
            mark = "\U0001F1FD"
        elif turn == player_two and message.author == player_two:
            mark = ":o2:"
        if 0 < pos < 10 and board[pos-1] == "\U00002B1C":
            board[pos-1] = mark
            count += 1

            line = ""
            for index in range(len(board)):
                if index in (2, 5, 8):
                    line += " " + board[index]
                    await message.channel.send(line)
                    line = ""
                else:
                    line += " " + board[index]

            check_winner(winning_condition, mark)
            if game_over:
                if mark == "\U0001F1FD":
                    await message.channel.send(player_one.mention + " wins! :trophy:")
                else:
                    await message.channel.send(player_two.mention + " wins! :trophy:")
            elif count >= 9:
                await message.channel.send("It's a tie.")

            if turn == player_one:
                turn = player_two
            else:
                turn = player_one

        else:
            await message.channel.send("It is not your turn.")

    else:
        await message.channel.send("Please start a new game. \U0001F3B2")


def check_winner(winning_condition, mark):
    global game_over
    for condition in winning_condition:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            game_over = True


@ tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Plase mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Please make sure to mention / ping players (ie. {ctx.message.author.mention})")


@ place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Plase enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


client.run(os.environ.get('TOKEN'))
