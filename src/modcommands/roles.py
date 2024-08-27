import discord
from discord import app_commands
from discord.ext import commands

class RoleManagementCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addrole", description="Add a role to a user.")
    async def addrole(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        try:
            await user.add_roles(role)
            await interaction.response.send_message(f"{role.name} has been added to {user.name}.")
        except discord.Forbidden:
            await interaction.response.send_message("Error: The bot does not have sufficient permissions to add this role.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="removerole", description="Remove a role from a user.")
    async def removerole(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        try:
            await user.remove_roles(role)
            await interaction.response.send_message(f"{role.name} has been removed from {user.name}.")
        except discord.Forbidden:
            await interaction.response.send_message("Error: The bot does not have sufficient permissions to remove this role.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RoleManagementCommand(bot))
