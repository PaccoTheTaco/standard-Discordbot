import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from welcomeandleave.welcome import setup as setup_welcome
from welcomeandleave.leave import setup as setup_leave
from tickets.ticket_system import setup as setup_ticket_system
from github import setup_github_commands

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await setup_welcome(bot)
    await setup_leave(bot)
    await setup_ticket_system(bot) 
    setup_github_commands(bot)
    await bot.tree.sync() 
    print(f'Logged in as {bot.user}')

async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)

import asyncio
asyncio.run(main())
