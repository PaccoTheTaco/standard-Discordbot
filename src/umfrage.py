import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Umfrage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {}

    @app_commands.command(name="umfrage", description="Starte eine Umfrage.")
    @app_commands.describe(question="Die Frage der Umfrage", option1="Option 1", option2="Option 2", duration="Dauer der Umfrage in Sekunden")
    @commands.has_permissions(administrator=True)
    async def umfrage(self, interaction: discord.Interaction, question: str, option1: str, option2: str, duration: int):
        embed = discord.Embed(title="📊 Umfrage", description=question, color=discord.Color.blue())
        embed.add_field(name="1️⃣", value=option1, inline=False)
        embed.add_field(name="2️⃣", value=option2, inline=False)
        embed.set_footer(text=f"Die Umfrage endet in {duration} Sekunden.")
        
        await interaction.response.send_message(embed=embed)
        poll_message = await interaction.original_response()

        await poll_message.add_reaction("1️⃣")
        await poll_message.add_reaction("2️⃣")

        self.active_polls[poll_message.id] = asyncio.create_task(self.end_poll(poll_message, duration))

    async def end_poll(self, message, duration):
        await asyncio.sleep(duration)
        
        poll_message = await message.channel.fetch_message(message.id)
        reactions = poll_message.reactions
        
        option1_count = 0
        option2_count = 0
        
        for reaction in reactions:
            if reaction.emoji == "1️⃣":
                option1_count = reaction.count - 1
            elif reaction.emoji == "2️⃣":
                option2_count = reaction.count - 1

        if option1_count > option2_count:
            winner = "1️⃣ " + poll_message.embeds[0].fields[0].value
        elif option2_count > option1_count:
            winner = "2️⃣ " + poll_message.embeds[0].fields[1].value
        else:
            winner = "Unentschieden"

        result_embed = poll_message.embeds[0].copy()
        result_embed.color = discord.Color.green()
        result_embed.set_footer(text="Die Umfrage ist beendet.")
        result_embed.add_field(name="Ergebnisse:", value=f"1️⃣ {option1_count} Stimmen\n2️⃣ {option2_count} Stimmen", inline=False)
        result_embed.add_field(name="Gewinner:", value=winner, inline=False)

        await poll_message.clear_reactions()
        await poll_message.edit(embed=result_embed)

        del self.active_polls[message.id]

async def setup(bot):
    await bot.add_cog(Umfrage(bot))
