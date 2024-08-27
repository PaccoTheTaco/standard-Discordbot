import discord
from discord.ext import commands
import random
from datetime import datetime

class LeaveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="leave") or \
                  discord.utils.get(member.guild.text_channels, name="goodbye")
        if channel:
            leave_messages = [
                f"Sad to see you go, {member.mention}. We hope to see you again!",
                f"Goodbye {member.mention}. We hope you enjoyed your time here.",
                f"{member.mention} has left the server. We'll miss you!",
                f"{member.mention} decided to leave us. Farewell and take care!",
                f"Farewell {member.mention}! We wish you all the best."
            ]

            leave_message = random.choice(leave_messages)

            embed = discord.Embed(
                title="Goodbye!",
                description=leave_message,
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=member.avatar.url)

            embed.set_footer(text="We hope to see you again!")

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LeaveCog(bot))
