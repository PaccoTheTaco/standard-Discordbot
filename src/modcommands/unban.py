import discord
from discord import app_commands
from discord.ext import commands

class UnbanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unban", description="Unban a user from the server.")
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild = interaction.guild
        await guild.unban(user, reason=reason)
        await interaction.response.send_message(f"{user.name} has been unbanned. Reason: {reason if reason else 'No reason provided.'}")

async def setup(bot):
    await bot.add_cog(UnbanCommand(bot))
