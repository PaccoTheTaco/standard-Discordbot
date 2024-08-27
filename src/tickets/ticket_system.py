import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from .close_ticket import CloseTicketSystem

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.close_ticket_system = CloseTicketSystem(bot)

    @app_commands.command(name="ticketembed", description="Send an embed with a ticket dropdown")
    async def ticket_embed(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Ticket System",
            description="Please select one of the options below to create a ticket.",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Support", value="Click here if you have a question.", inline=False)
        embed.add_field(name="Report", value="Click here if you want to report someone.", inline=False)
        embed.add_field(name="Application", value="Click here if you want to apply for a position.", inline=False)

        view = TicketDropdownView(self.bot, self.close_ticket_system)
        await interaction.response.send_message(embed=embed, view=view)

    @ticket_embed.error
    async def ticket_embed_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

class TicketDropdown(discord.ui.Select):
    def __init__(self, bot, close_ticket_system):
        self.bot = bot
        self.close_ticket_system = close_ticket_system
        options = [
            discord.SelectOption(label="Support", description="Click here if you have a question.", value="support"),
            discord.SelectOption(label="Report", description="Click here if you want to report someone.", value="report"),
            discord.SelectOption(label="Application", description="Click here if you want to apply for a position.", value="application"),
        ]
        super().__init__(placeholder="Make a selection", options=options)

    async def callback(self, interaction: discord.Interaction):
        await self.create_ticket_channel(interaction, self.values[0])

    async def create_ticket_channel(self, interaction: discord.Interaction, ticket_type: str):
        try:
            guild = interaction.guild
            category = discord.utils.get(guild.categories, name="Tickets")
            if category is None:
                category = await guild.create_category("Tickets")

            channel_name = f"{ticket_type}-{interaction.user.id}"
            ticket_channel = await guild.create_text_channel(name=channel_name, category=category)

            await ticket_channel.set_permissions(guild.default_role, read_messages=False)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            await ticket_channel.set_permissions(guild.me, read_messages=True, send_messages=True)

            embed = discord.Embed(
                title=f"{ticket_type.capitalize()} Ticket",
                description="This ticket has been created.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Created by", value=f"{interaction.user.name}#{interaction.user.discriminator}", inline=False)
            embed.add_field(name="Ticket Type", value=ticket_type.capitalize(), inline=False)
            embed.add_field(name="Creation Time", value=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), inline=False)

            close_button_view = self.close_ticket_system.get_close_ticket_view(interaction.user)

            await ticket_channel.send(embed=embed, view=close_button_view)

            await interaction.response.send_message(f"Your {ticket_type.capitalize()} ticket has been created: {ticket_channel.mention}", ephemeral=True)

        except Exception as e:
            print(f"An error occurred: {e}")
            await interaction.response.send_message("An error occurred while creating the ticket. Please try again later.", ephemeral=True)

class TicketDropdownView(discord.ui.View):
    def __init__(self, bot, close_ticket_system):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown(bot, close_ticket_system))

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
