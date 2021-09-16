import discord
from discord.ext import commands
from discord.ext.commands.core import check
import youtube_dl


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

        # all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio',
            'noplaylist': 'True',
            'source_address': '0.0.0.0'
        }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        self.vc = ""

    def search_yt(self, item):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            first_url = self.music_queue[0][0]['source']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                first_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # try to connect to voice channel if you are not already connected
            # if self.vc == "" or not self.vc.is_connected() or self.vc == None:
            #     self.vc = await self.music_queue[0][1].connect()
            # else:
            #     await self.vc.move_to(self.music_queue[0][1])
            self.vc = discord.utils.get(self.client.voice_clients)
            print(self.music_queue)
            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # # Join voice channel
    # @commands.command(name='join', help='Tells the bot to join the voice channel')
    # async def join(self, ctx):
    #     if not ctx.message.author.voice:
    #         await ctx.send("{} is not connected to a voice channel :x: ".format(ctx.message.author.mention))
    #         return
    #     else:
    #         channel = ctx.message.author.voice.channel
    #         await channel.connect()

    # Leave voice channel
    @commands.command(aliases=['dc'])
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel. :x: ")

    # Play youtube video
    @commands.command(aliases=['p'])
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel == None:
            await ctx.send("{} is not connected to a voice channel :x:".format(ctx.message.author.mention))

        else:
            try:
                channel = ctx.message.author.voice.channel
                await channel.connect()
            except:
                pass
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Keyword might not be available :x:")
            else:
                await ctx.send("Added **{}** to queue :inbox_tray:".format(song['title']))
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await ctx.send("**Now playing:** {} :musical_note:".format(self.music_queue[0][0]['title']))
                    await self.play_music()

    @commands.command(name='remove')
    async def remove(self, ctx, number):

        try:
            removed_song = self.music_queue(int(number))
            await ctx.send('Removed **{}** :outbox_tray:'.format(removed_song[0]['title']))
            self.music_queue.pop(int(number)-1)

        except:
            await ctx.send('Your queue is either **empty** or the number is **out of range**')

    # Skip the song
    @ commands.command(aliases=['fs'])
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await ctx.send("**Now playing:** {} :musical_note:".format(self.music_queue[0][0]['title']))
            await self.play_music()

    # Stop the whole queue
    @ commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            self.music_queue = []
            await ctx.send("The playlist had been cleared :broom:")
        else:
            await ctx.send("Nothing is playing right now.:x:")

    # Resume music
    @ commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Nothing is playing right now.:x:")

    # Pause music
    @ commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Nothing is playing right now.:x:")

    # Queue music requested by user
    @ commands.command(aliases=['q'])
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            if len(self.music_queue) <= 5:
                page = discord.Embed(
                    title="Queue :arrows_clockwise:",
                    color=discord.Color.dark_gold()
                )
                for i in range(0, len(self.music_queue)):
                    page.add_field(
                        name="Song " + str(i+1),
                        value=self.music_queue[i][0]['title'],
                        inline=False
                    )
                page.set_footer(text="Page 1")
                await ctx.send(embed=page)
            else:
                embed_pages = []
                starting_num = 0
                remainder = 0
                if len(self.music_queue) % 5 != 0:
                    remainder = 1
                for page in range(int(len(self.music_queue)/5) + remainder):
                    page = discord.Embed(
                        title="Queue :arrows_clockwise:",
                        color=discord.Color.dark_gold()
                    )
                    if starting_num + 5 > len(self.music_queue):
                        for i in range(starting_num, len(self.music_queue)):
                            page.add_field(
                                name="Song " + str(i+1),
                                value=self.music_queue[i][0]['title'],
                                inline=False
                            )
                    else:
                        for i in range(starting_num, starting_num+5):
                            page.add_field(
                                name="Song " + str(i+1),
                                value=self.music_queue[i][0]['title'],
                                inline=False
                            )
                    page.set_footer(text="Page {}".format(
                        str(len(embed_pages)+1)))
                    starting_num += 5
                    embed_pages.append(page)
                message = await ctx.send(embed=embed_pages[0])
                for i in ["⬅️", "➡️"]:
                    await message.add_reaction(i)

                index = 0
                while True:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=None)
                    await message.remove_reaction(reaction.emoji, ctx.message.author)

                    if str(reaction) == "⬅️" and str(user) != self.client.user.id:
                        index -= 1
                        try:
                            page = embed_pages[index]
                        except IndexError:
                            page = embed_pages[len(embed_pages)-1]
                    elif str(reaction) == "➡️" and str(user) != self.client.user.id:
                        index += 1
                        try:
                            page = embed_pages[index]
                        except IndexError:
                            page = embed_pages[0]

                    await message.edit(embed=page)
        else:
            await ctx.send("No song requested.:x:")


def setup(client):
    client.add_cog(Music(client))
