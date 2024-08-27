import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from welcomeandleave.welcome import setup as setup_welcome
from welcomeandleave.leave import setup as setup_leave
from tickets.ticket_system import setup as setup_ticket_system
from github import setup_github_commands
from modcommands.kick import setup as setup_kick
from modcommands.ban import setup as setup_ban
from modcommands.unban import setup as setup_unban
from modcommands.timeout import setup as setup_timeout
from modcommands.untimeout import setup as setup_untimeout
from modcommands.lock_unlock import setup as setup_lock_unlock
from modcommands.softban import setup as setup_softban
from modcommands.roles import setup as setup_roles
from games.tictactoe import setup as setup_tictactoe
from reactionroles.reaction_roles_listener import ReactionRolesListener
from reactionroles.data_manager import DataManager
from reminder import setup as setup_reminder
from umfrage import setup as setup_umfrage
from logsystem import VoiceLogListener, RoleLogListener, MessageLogListener, ServerLogListener

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def setup_reaction_roles(bot):
    try:
        data_manager = DataManager()
        print("DataManager initialized successfully.")
        await bot.add_cog(ReactionRolesListener(bot, data_manager))
        print("ReactionRolesListener cog added successfully.")
    except Exception as e:
        print(f"Error in setup_reaction_roles: {e}")


@bot.event
async def on_ready():
    try:
        await setup_reaction_roles(bot)
        await setup_welcome(bot)
        await setup_leave(bot)
        await setup_ticket_system(bot) 
        setup_github_commands(bot)
        await setup_kick(bot)
        await setup_ban(bot)
        await setup_unban(bot)
        await setup_timeout(bot)
        await setup_untimeout(bot)
        await setup_lock_unlock(bot)
        await setup_softban(bot)
        await setup_roles(bot)
        await setup_tictactoe(bot)
        await setup_umfrage(bot)
        await setup_reaction_roles(bot)
        await setup_reminder(bot)
        await bot.add_cog(VoiceLogListener(bot))
        await bot.add_cog(RoleLogListener(bot))
        await bot.add_cog(MessageLogListener(bot))
        await bot.add_cog(ServerLogListener(bot))
        await bot.tree.sync() 
        print(f'Logged in as {bot.user}')
    except Exception as e:
        print(f"Error in logging in: {e}")

async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)

import asyncio
asyncio.run(main())
