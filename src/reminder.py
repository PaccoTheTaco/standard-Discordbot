from discord.ext import commands
from discord import app_commands
import asyncio

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="remind", description="Set a reminder.")
    @app_commands.describe(time="Time format: s=seconds, m=minutes, h=hours, d=days")
    async def remind(self, ctx, time: str, *, reminder: str = "Reminder!"):
        try:
            seconds = self.convert_time_to_seconds(time)
            if seconds is None:
                await ctx.send("Invalid time format! Please use `s` for seconds, `m` for minutes, `h` for hours, or `d` for days.", ephemeral=True)
                return

            await ctx.send(f"Reminder set for {time} from now!", ephemeral=True)
            await asyncio.sleep(seconds)
            await ctx.author.send(f"Reminder: {reminder}")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}", ephemeral=True)

    def convert_time_to_seconds(self, time: str) -> int:
        time_mapping = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400
        }
        try:
            return int(time[:-1]) * time_mapping[time[-1]]
        except (ValueError, KeyError):
            return None

async def setup(bot):
    await bot.add_cog(Reminder(bot))
