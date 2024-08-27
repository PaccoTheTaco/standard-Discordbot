import discord
from discord.ext import commands

class MessageLogListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_contents = {}
        self.message_authors = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        self.message_contents[message.id] = message.content
        self.message_authors[message.id] = message.author

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        guild = before.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")

        if not log_channel:
            return

        embed = discord.Embed(title="Message Edited", color=discord.Color.orange())
        embed.add_field(name="Author", value=before.author.mention, inline=False)
        embed.add_field(name="Before", value=self.message_contents.get(before.id, "Unknown"), inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=before.author.display_name)
        embed.set_thumbnail(url=before.author.avatar.url)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        guild = message.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")

        if not log_channel:
            return

        embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
        embed.add_field(name="Author", value=self.message_authors.get(message.id, "Unknown"), inline=False)
        embed.add_field(name="Message", value=self.message_contents.get(message.id, "Unknown"), inline=False)
        embed.set_footer(text=message.author.display_name)
        embed.set_thumbnail(url=message.author.avatar.url)
        await log_channel.send(embed=embed)
