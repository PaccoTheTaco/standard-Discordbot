import discord
from discord import app_commands
from discord.ext import commands

class KickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a user from the server.")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await user.kick(reason=reason)
        await interaction.response.send_message(f"{user.name} has been kicked. Reason: {reason if reason else 'No reason provided.'}")

async def setup(bot):
    await bot.add_cog(KickCommand(bot))
