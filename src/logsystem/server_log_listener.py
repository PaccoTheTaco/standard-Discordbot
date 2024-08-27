import discord
from discord.ext import commands

class ServerLogListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        for emoji in after:
            if emoji not in before:
                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_create):
                    creator = entry.user
                    embed = discord.Embed(
                        title="Emoji added",
                        description=f"Added Emoji: {emoji}\nAdded by: {creator.mention if creator else 'Unknown'}",
                        color=discord.Color.blue()
                    )
                    await self.log_server_activity(guild, embed)

        for emoji in before:
            if emoji not in after:
                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_delete):
                    remover = entry.user
                    embed = discord.Embed(
                        title="Emoji removed",
                        description=f"Removed Emoji: {emoji}\nRemoved by: {remover.mention if remover else 'Unknown'}",
                        color=discord.Color.blue()
                    )
                    await self.log_server_activity(guild, embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.premium_subscription_count != after.premium_subscription_count:
            embed = discord.Embed(
                title="Boost count updated",
                description=f"Boost count: {after.premium_subscription_count} Boosts",
                color=discord.Color.blue()
            )
            await self.log_server_activity(after, embed)

    async def log_server_activity(self, guild, embed):
        log_channel = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")
        if log_channel:
            await log_channel.send(embed=embed)

