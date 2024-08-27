import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def get_github_repo_info(repo_name):
    url = f'https://api.github.com/repos/{repo_name}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_embed(repo_info):
    embed = discord.Embed(title=repo_info['full_name'], url=repo_info['html_url'], description=repo_info['description'], color=0x7289da)
    embed.add_field(name='Stars', value=repo_info['stargazers_count'], inline=True)
    embed.add_field(name='Forks', value=repo_info['forks_count'], inline=True)
    embed.add_field(name='Open Issues', value=repo_info['open_issues_count'], inline=True)
    embed.add_field(name='Language', value=repo_info['language'], inline=True)
    embed.set_footer(text=f"Owner: {repo_info['owner']['login']}")

    return embed

def setup_github_commands(bot):
    @bot.tree.command(name="github", description="Fetch information about a GitHub repository")
    async def github(interaction: discord.Interaction, owner: str, name: str):
        repo_name = f"{owner}/{name}"
        repo_info = get_github_repo_info(repo_name)
        
        if repo_info:
            await interaction.response.send_message(embed=create_embed(repo_info))
        else:
            await interaction.response.send_message('Repository nicht gefunden oder ein Fehler ist aufgetreten.')
