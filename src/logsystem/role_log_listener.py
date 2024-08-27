import discord
from discord.ext import commands

class RoleLogListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild = role.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")

        if not log_channel:
            return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            creator = entry.user

        embed = discord.Embed(title="Role created", color=discord.Color.green())
        embed.add_field(name="Rolename", value=role.mention, inline=False)
        embed.add_field(name="Created by", value=creator.mention if creator else "Unknown", inline=False)
        embed.add_field(name="Permissions", value=str(role.permissions), inline=False)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")

        if not log_channel:
            return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            deleter = entry.user

        embed = discord.Embed(title="Role deleted", color=discord.Color.red())
        embed.add_field(name="Rolename", value=role.name, inline=False)
        embed.add_field(name="Deleted by", value=deleter.mention if deleter else "Unknown", inline=False)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        guild = before.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")

        if not log_channel:
            return

        embed = discord.Embed(title="Role updated", color=discord.Color.yellow())
        embed.add_field(name="Role", value=after.mention, inline=False)
        if before.name != after.name:
            embed.add_field(name="Old Name", value=before.name, inline=False)
            embed.add_field(name="New Name", value=after.name, inline=False)
        if before.color != after.color:
            embed.add_field(name="Old Color", value=str(before.color), inline=False)
            embed.add_field(name="New Color", value=str(after.color), inline=False)
        if before.permissions != after.permissions:
            added = [perm for perm in after.permissions if perm not in before.permissions]
            removed = [perm for perm in before.permissions if perm not in after.permissions]
            embed.add_field(name="Added Permissions", value=", ".join(str(perm) for perm in added), inline=False)
            embed.add_field(name="Removed Permissions", value=", ".join(str(perm) for perm in removed), inline=False)

        await log_channel.send(embed=embed)
