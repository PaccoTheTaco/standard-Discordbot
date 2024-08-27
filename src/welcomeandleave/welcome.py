import discord
from discord.ext import commands
import random
from datetime import datetime

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if channel:
            welcome_messages = [
                f"Welcome to the server, {member.mention}! We're excited to have you here!",
                f"Hey {member.mention}, glad you joined us! Make yourself at home.",
                f"Hello {member.mention}! Welcome aboard! We're glad to have you here.",
                f"Hi {member.mention}, welcome to our community! Let's make great memories together.",
                f"Cheers {member.mention}, welcome! We hope you have a fantastic time here."
            ]

            welcome_message = random.choice(welcome_messages)

            embed = discord.Embed(
                title="Welcome!",
                description=welcome_message,
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=member.avatar.url)

            embed.set_footer(text="We're happy to see you here!")

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
