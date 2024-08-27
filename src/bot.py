import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from welcomeandleave.welcome import setup as setup_welcome
from welcomeandleave.leave import setup as setup_leave
from github import setup_github_commands

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await setup_welcome(bot)
    await setup_leave(bot)
    setup_github_commands(bot)

async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)

import asyncio
asyncio.run(main())
