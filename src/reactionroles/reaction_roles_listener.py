import discord
from discord.ext import commands
from .reaction_role import ReactionRole
from discord import app_commands

class ReactionRolesListener(commands.Cog):
    def __init__(self, bot, data_manager):
        self.bot = bot
        self.data_manager = data_manager

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        roles = self.data_manager.get_reaction_roles(str(payload.message_id))
        for role in roles:
            if role.get_emoji() == str(payload.emoji):
                guild = self.bot.get_guild(payload.guild_id)
                role_to_add = guild.get_role(int(role.get_role_id()))
                await payload.member.add_roles(role_to_add)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member.bot:
            return

        roles = self.data_manager.get_reaction_roles(str(payload.message_id))
        for role in roles:
            if role.get_emoji() == str(payload.emoji):
                role_to_remove = guild.get_role(int(role.get_role_id()))
                await member.remove_roles(role_to_remove)

    @app_commands.command(name="reactionrole")
    async def reactionrole(self, interaction: discord.Interaction, role: discord.Role, message_id: str, emoji: str):
        """Adds a reaction role to a message."""
        try:
            guild_id = str(interaction.guild.id)
            role_id = str(role.id)

            print(f"Guild ID: {guild_id}, Message ID: {message_id}, Role ID: {role_id}, Emoji: {emoji}")

            reaction_role = ReactionRole(guild_id, message_id, role_id, emoji)

            self.data_manager.add_reaction_role(reaction_role)

            channel = interaction.channel
            message = await channel.fetch_message(message_id)

            if not message:
                await interaction.response.send_message(f"Message with ID {message_id} not found in this channel.", ephemeral=True)
                return

            await message.add_reaction(emoji)

            await interaction.response.send_message(f"Reaction role for {role.name} added to message {message_id} with emoji {emoji}.", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message(f"Message with ID {message_id} not found.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"I do not have permission to add roles or reactions in this server.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"HTTP error occurred: {str(e)}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {str(e)}", ephemeral=True)
