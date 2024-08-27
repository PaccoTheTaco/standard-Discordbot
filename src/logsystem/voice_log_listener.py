import discord
from discord.ext import commands

class VoiceLogListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")

        if not log_channel:
            return

        embed = discord.Embed(color=discord.Color.blue(), footer={"text": member.display_name})

        if before.channel is None and after.channel is not None:
            embed.title = "Member joined Voice Channel"
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Channel", value=after.channel.name, inline=False)
        elif before.channel is not None and after.channel is None:
            embed.title = "Member left Voice Channel"
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Channel", value=before.channel.name, inline=False)
        elif before.channel is not None and after.channel is not None:
            embed.title = "Member switched Voice Channel"
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Before", value=before.channel.name, inline=False)
            embed.add_field(name="After", value=after.channel.name, inline=False)

        embed.set_thumbnail(url=member.avatar.url)
        await log_channel.send(embed=embed)
