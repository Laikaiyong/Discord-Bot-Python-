import discord
from discord.ext import commands
from pymongo import MongoClient

bot_channel = [856443290814906378, 856724336344825909,
               856443269143068682, 856442826958045194, 857435422673076254, 852085478659457040]
talk_channels = [856440780164169738, 852101645836091472, 856443069048946708, 856443305994616832, 856443325963304961, 856443348797751296, 856514679384178698, 856774483688161330, 856573661347184700, 856724886416654356, 856828838313721856, 856535262926077962, 856535212884492328, 856534826840227900, 856535666908987432, 856535124774748200, 856535388276523068, 856534767722037268, 856534713606340640,
                 856535065801785384, 856828969297641493, 856535453603594261, 856535038295146516, 856515778022735882, 856515915084201984, 857625195060789298, 856514588076671006, 856520871950286849, 856523750371229737, 856443792462839838, 856832125575626762, 852111379946143784, 852115164937584651, 852113512439349258, 852085478659457044, 852085478659457040, 852085478659457043, 856764193205780480, 852193472122847232]

level = ["Level 1", "Level 10", "Level 25",
         "Level 50", "Level 75", "Level 100", "Level 200+"]
level_num = [5, 10, 15]

cluster = MongoClient(
    "mongodb+srv://vandyck_lai1:<z1gawpIWnU0tFh9v>@kygorgorcluster.wwvha.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

levelling = cluster["KYGorGorCluster"]["levelling"]


class levelsys(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ready")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = levelling.find_one({"id": message.author.id})

            if not message.author.bot:
                if stats is None:
                    new_user = {"id": message.author.id, "xp": 10}
                    levelling.insert_one(new_user)
                else:
                    xp = stats["xp"] + 5
                    levelling.update_one({"id": message.author.id}, {
                                         "$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*(lvl-1))):
                            break
                        lvl += 1
                    xp -= ((50*(lvl**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"{message.author.mention} had reached **Level {lvl}**, keep up the momentum")
                        for i in range(len(level)):
                            if lvl == level_num[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=i))

                                embed = discord.Embed(
                                    description=f"{message.author.mention}, you earned **{i}** role!"
                                )
                                embed.set_thumbnail(
                                    url=message.author.avatar_url)
                                embed.set_footer(
                                    text='\u200b Behold, the wisdom of activeness')
                                await message.channel.send(embed=embed)

    @commands.command(aliases='r')
    async def rank(self, ctx):
        if ctx.channel.id in bot_channel:
            stats = levelling.find_one({"id": ctx.author.id})

            if stats is None:
                embed = discord.Embed(
                    description="You haven't send any messages, send 1 and try again \U0001F60F")

            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50*(lvl**2))+(50*(lvl-1))):
                        break
                    lvl += 1

                xp -= ((50*(lvl**2))+(50*(lvl-1)))

                boxes = int((xp/(200*((1/2) * lvl)))*20)
                rankings = levelling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break

                embed = discord.Embed(
                    title="{}'s level stats".format(ctx.author.name))
                embed.add_field(
                    name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(
                    name="XP", value=f"{xp}/{int(200 *((1/2) * lvl))}", inline=True)
                embed.add_field(
                    name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (
                    20 - boxes) * ":white_large_square:", inline=True)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)

    @commands.command(aliases='ldb')
    async def leaderboard(self, ctx):
        if ctx.channel.id in bot_channel:
            rankings = levelling.find().sort("xp", -1)
            i = 1
            embed = discord.Embed(title="Active Ranking:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    temp_xp = x["xp"]
                    embed.add_field(
                        name=f"{i}: {temp.name}", value=f"total xp: {temp_xp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(levelsys(client))
