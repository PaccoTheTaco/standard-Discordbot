import discord
from discord.ext import commands

class CloseTicketButton(discord.ui.Button):
    def __init__(self, user: discord.User):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.danger)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator or interaction.user == self.user:
            guild = interaction.guild
            closed_category = discord.utils.get(guild.categories, name="Closed Tickets")
            if closed_category is None:
                closed_category = await guild.create_category("Closed Tickets")

            await interaction.channel.set_permissions(self.user, overwrite=None)
            await interaction.channel.edit(category=closed_category)
            await interaction.response.send_message("The ticket has been closed and moved to the Closed Tickets category.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)

class CloseTicketView(discord.ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=None)
        self.add_item(CloseTicketButton(user))

class CloseTicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_close_ticket_view(self, user: discord.User):
        return CloseTicketView(user)

async def setup(bot):
    await bot.add_cog(CloseTicketSystem(bot))
