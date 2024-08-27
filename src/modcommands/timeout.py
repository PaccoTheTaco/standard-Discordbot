import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class TimeoutCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mute", description="Mute a user for a specified duration.")
    async def mute(self, interaction: discord.Interaction, user: discord.Member, duration: int = None, reason: str = None):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        duration_seconds = duration * 60 if duration else None
        await user.timeout(timedelta(seconds=duration_seconds) if duration_seconds else None, reason=reason)
        await interaction.response.send_message(f"{user.name} has been muted. Duration: {duration if duration else 'indefinitely'} minutes. Reason: {reason if reason else 'No reason provided.'}")

async def setup(bot):
    await bot.add_cog(TimeoutCommand(bot))
