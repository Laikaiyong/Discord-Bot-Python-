import discord
from discord.ext import commands


class ModMail(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command to create modmail channel
    @commands.command()
    async def mod_mail(self, ctx):
        guild = ctx.guild
        admin_role = discord.utils.get(
            guild.roles, name="Core")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }
        await ctx.guild.create_text_channel("\U0001F4E7-mod-mail", overwrites=overwrites)

    # Mod mail

    @commands.Cog.listener('on_message')
    async def mail_message(self, message):

        # Avoid bot to respond to itself
        if message.author == self.client.user:
            return

        empty_array = []
        modmail_channel = discord.utils.get(
            self.client.get_all_channels(), name="\U0001F4E7-mod-mail")
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

                await member_object.send(f"[{message.author}] {mod_message}")


def setup(client):
    client.add_cog(ModMail(client))
