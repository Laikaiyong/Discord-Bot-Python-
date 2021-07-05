import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import requests

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="~",
                      intents=intents, help_command=None, activity=discord.Activity(type=discord.ActivityType.competing, name="Vandyck#7726 兄ちゃん戦争"))


@client.command()
async def welcome(ctx):
    guild = client.get_guild(852085478659457035)
    channel = guild.get_channel(852085478659457042)
    member_count = guild.member_count

    img = Image.open("Pynata Cover.png")
    img = img.copy()

    member = "<@>"
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

client.run('ODIxMzc3MjI4Nzk3MTE2NDM2.YFC1Jw.xYz2WfFeHNblG0X1b3Cu5xjYrz4')
