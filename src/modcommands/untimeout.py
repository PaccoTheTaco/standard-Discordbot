import discord
from discord import app_commands
from discord.ext import commands

class UntimeoutCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unmute", description="Unmute a user.")
    async def unmute(self, interaction: discord.Interaction, user: discord.Member):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await user.timeout(None)
        await interaction.response.send_message(f"{user.name} has been unmuted and can speak and send messages again.")

async def setup(bot):
    await bot.add_cog(UntimeoutCommand(bot))
