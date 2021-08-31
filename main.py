import discord
from discord.ext import commands
import json
import requests
import re
import random as rd
from PIL import Image, ImageFont, ImageDraw


class Main(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Prefix set up
    def get_prefix(self, message):

        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]

    @commands.command(aliases=["set"])
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)

        await ctx.send(f"The prefix was changed to {prefix}.")

    # Inspect users message for prefix manipulation
    @commands.Cog.listener("on_message")
    async def check_prefix(self, message):

        # Avoid bot to respond to itself
        if message.author == self.client.user:
            return

        # Prefix manipulation
        try:

            if message.mentions[0] == self.client.user:

                with open("prefixes.json", "r") as read:
                    prefixes = json.load(read)

                pre = prefixes[str(message.guild.id)]

                await message.channel.send(f"My prefix for {message.guild.name} is now {pre}.")

        except:
            pass

    # # Join a new server and set prefix
    # @commands.Cog.listener("on_guild_join")
    # async def set_prefix(guild):

    #     with open("prefixes.json", "r") as f:
    #         prefixes = json.load(f)

    #     prefixes[str(guild.id)] = "~"

    #     with open("prefixes.json", "w") as f:
    #         json.dump(prefixes, f)

    @commands.command(aliases=["set"])
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)

        await ctx.send(f"The prefix was changed to {prefix}.")

    # Inspect users message for prefix manipulation
    @commands.Cog.listener("on_message")
    async def send_prefix(self, message):

        # Avoid bot to respond to itself
        if message.author == self.client.user:
            return

        # Prefix manipulation
        try:

            if message.mentions[0] == self.client.user:

                with open("prefixes.json", "r") as read:
                    prefixes = json.load(read)

                pre = prefixes[str(message.guild.id)]

                await message.channel.send(f"My prefix for {message.guild.name} is now {pre}.")

        except:
            pass

    # Welcome Card
    @commands.Cog.listener("on_member_join")
    async def welcome(self, member):
        guild = self.client.get_guild(852085478659457035)
        channel = guild.get_channel(852085478659457042)
        member_count = guild.member_count

        img = Image.open("Pynata Cover.png")
        img = img.copy()

        member_im = Image.open(requests.get(
            member.avatar_url, stream=True).raw)
        member_im = member_im.resize((310, 300), Image.LANCZOS)

        img.paste(member_im, (int(1150/3)+25, int(669/4)))
        msg = "Welcome " + member.name + " (Member " + str(member_count) + ")"
        draw = ImageDraw.Draw(img)
        chunk_five = ImageFont.truetype("Chunk Five Print.otf", 60)
        w, h = draw.textsize(msg, font=chunk_five)
        draw.text(((1150-w)/2, (669-h)/8*7), msg,
                  fill="black", font=chunk_five)
        img.save("new.png", "PNG")

        await channel.send(f"Welcome to the server {member.mention}! :partying_face:\n:one: Check out <#{852088286922801193}> to redeem membership :white_check_mark:\n:two: Stay updated on events in <#{856440780164169738}> :fireworks:\n:three: Customize your unique role in <#{852111666716213258}> :scroll:\n:four: Get useful resources in <#{852101645836091472}> on your developing journey :person_climbing:\n", file=discord.File("new.png"))

        for channel in member.guild.channels:
            if channel.name.startswith('Peep'):
                await channel.edit(name=f'Peep: {str(member.guild.member_count)}')
                break

    # Recount member count
    @commands.Cog.listener("on_member_leave")
    async def recount(self, member):
        channel = self.client.get_channel('channel id here')
        for channel in member.guild.channels:
            if channel.name.startswith('Peep'):
                await channel.edit(name=f'Peep: {str(member.guild.member_count)}')
                break

    # Client help command
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="KY Gor Gor commands",
            description="Here are all the command syntax available:",
            color=discord.Color.dark_gold()
        )
        embed.add_field(
            name="Prefix", value="\n`~`\nDefault prefix (can be modified)", inline=True)
        embed.add_field(
            name="Basic", value="\n`server`\nDisplay server information\n`settings`\nChange prefix for server.\n`help`\nDisplay bot commands\n`quote`\nSend Random Quote", inline=True)
        embed.add_field(
            name="Mod Mail", value="\n`mod_mail`\nCreate a channel for moderator's mail", inline=True)
        await ctx.send(embed=embed)

    # Quote

    @commands.command()
    async def quote(self, ctx):
        data = requests.get("https://zenquotes.io/api/random")
        data = data.json()
        quote = f"**{data[0]['q']}** -  *{data[0]['a']}*"
        await ctx.send(quote)

    # Check ping latency
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    # Kick users who are not obey the rules
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Kick",
                description=f"**{member}** was kicked.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Reason", value=f"{reason}")
            await ctx.send(embed=embed)

    # Ban users who are not obey the rules
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Ban",
                description=f"**{member}** was banned.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Reason", value=f"{reason}")
            await ctx.send(embed=embed)

    # Add bundles react
    @commands.command(aliases=['ab'])
    async def add_bundles_react(self, ctx, message: discord.Message, *emoji):
        if message != None and emoji != None:
            for emote in emoji:
                await message.add_reaction(emote)

        else:
            await ctx.send("Invalid argument.")

    # React role
    @commands.Cog.listener("on_raw_reaction_add")
    async def add_role(self, payload):
        if int(payload.message_id) in self.react_messages:
            guild_id = payload.guild_id
            guild = discord.utils.find(
                lambda g: g.id == guild_id, self.client.guilds)

            with open("reactrole.json") as f:
                data = json.load(f)

                for info in data:
                    if info["emoji"] == payload.emoji.name:
                        role = discord.utils.get(
                            guild.roles, name=info["role"])
                        await payload.member.add_roles(role)

    @commands.Cog.listener("on_raw_reaction_remove")
    async def remove_role(self, payload):
        if int(payload.message_id) in self.react_messages:
            guild_id = payload.guild_id
            guild = discord.utils.find(
                lambda g: g.id == guild_id, self.client.guilds)

            with open("reactrole.json") as f:
                data = json.load(f)
                for info in data:
                    if info["emoji"] == payload.emoji.name:
                        role = discord.utils.get(
                            guild.roles, name=info["role"])
                        await self.client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

    # # Minecraft API Thingy
    # @commands.command()
    # async def minecraft(self, ctx, arg):
    #     r = requests.get('https://api.minehut.com/server/' + arg + '?byName=true')
    #     json_data = r.json()

    #     description = json_data["server"]["motd"]
    #     online = str(json_data["server"]["online"])
    #     playerCount = str(json_data["server"]["playerCount"])

    #     embed = discord.Embed(
    #         title=arg.capitalize() + " Server Info",
    #         description='Description: ' + description +
    #         '\nOnline: ' + online + '\nPlayers: ' + playerCount,
    #         color=discord.Color.dark_green()
    #     )
    #     embed.set_thumbnail(
    #         url="https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1")

    #     await ctx.send(embed=embed)

    # Remove vulgar and Respond Greetings
    @commands.Cog.listener('on_message')
    async def vulgar(self, message):
        message.content = message.content.lower()

        # Avoid bot to respond to itself
        if message.author == self.client.user:
            return

        # Exception of rude message / Message auto clearing
        rude_words = ["fuck", "sohai", "cibai",
                      "diu", "dick", "boobs", "tits", "ass", "booty"]

        if not message.author.bot:
            for rude_word in rude_words:
                if re.search(rf'(\s|^){rude_word}(\b|$)', message.content):
                    await message.delete()
                break

    # Greets
    @commands.Cog.listener('on_message')
    async def greets(self, message):

        # Bot interaction (greetings)
        greetings = ["hello", "hi", "hey", "henlo", "hai", "sup"]

        message.content = message.content.lower()

        # Avoid bot to respond to itself
        if message.author == self.client.user:
            return

        if not message.author.bot:
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
    @commands.Cog.listener('on_message')
    async def emote_react(self, message):
        nice_words = ['nice', 'noice', 'nais', 'nices', 'nicess']

        for word in nice_words:
            if re.search(rf'(\s|^){word}(\b|$)', message.content):
                await message.add_reaction("<:noice:859666087216676884>")

    # Nominate command
    @commands.command(aliases=['nom'])
    async def nominate(self, message):
        users = [
            member for member in message.channel.members if "bots" not in [y.name.lower() for y in member.roles] and member != str(message.author)]
        users.remove(str(message.author))
        user = rd.choice(users)
        await message.channel.send(user.mention + " had been nominated.")

    # Client Server dashboard command

    @commands.command()
    async def server(self, ctx):
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


def setup(client):
    client.add_cog(Main(client))
