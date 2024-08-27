import discord
from discord.ext import commands

class ModLogListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target.id == user.id:
                embed = discord.Embed(
                    title="User Banned",
                    description=f"User: {user.mention}\nBanned by: {entry.user.mention}\nReason: {entry.reason if entry.reason else 'No reason provided'}",
                    color=discord.Color.red()
                )
                await self.log_mod_action(guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                embed = discord.Embed(
                    title="User Kicked",
                    description=f"User: {member.mention}\nKicked by: {entry.user.mention}\nReason: {entry.reason if entry.reason else 'No reason provided'}",
                    color=discord.Color.orange()
                )
                await self.log_mod_action(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.timed_out and not after.timed_out:
            async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                if entry.target.id == before.id and entry.before.get('communication_disabled_until') is not None:
                    embed = discord.Embed(
                        title="User Unmuted",
                        description=f"User: {before.mention}\nUnmuted by: {entry.user.mention}",
                        color=discord.Color.green()
                    )
                    await self.log_mod_action(before.guild, embed)
        elif not before.timed_out and after.timed_out:
            async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                if entry.target.id == before.id and entry.after.get('communication_disabled_until') is not None:
                    embed = discord.Embed(
                        title="User Muted",
                        description=f"User: {before.mention}\nMuted by: {entry.user.mention}\nUntil: {after.timed_out_until}",
                        color=discord.Color.purple()
                    )
                    await self.log_mod_action(before.guild, embed)

    async def log_mod_action(self, guild, embed):
        log_channel = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")
        if log_channel:
            await log_channel.send(embed=embed)

