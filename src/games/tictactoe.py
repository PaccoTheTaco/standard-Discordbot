import discord
from discord import app_commands
from discord.ext import commands

class TicTacToe:
    def __init__(self, player1: discord.User, player2: discord.User):
        self.board = [" " for _ in range(9)]
        self.current_player = player1
        self.players = {player1: "X", player2: "O"}

    def print_board(self):
        symbols = {"X": "❌", "O": "⭕", " ": "⬜"}
        board = [symbols[square] for square in self.board]
        return (
            f"{board[0]} {board[1]} {board[2]}\n"
            f"{board[3]} {board[4]} {board[5]}\n"
            f"{board[6]} {board[7]} {board[8]}"
        )

    def make_move(self, position, player):
        if self.board[position] == " ":
            self.board[position] = self.players[player]
            if self.check_winner():
                return f"Player {self.players[player]} ({'❌' if self.players[player] == 'X' else '⭕'}) wins! 🎉"
            elif " " not in self.board:
                return "It's a tie! 🤝"
            else:
                self.current_player = self.get_opponent(player)
                return None
        else:
            return "Invalid move! That spot is already taken. ❌"

    def get_opponent(self, player):
        return [p for p in self.players if p != player][0]

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]              
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != " ":
                return True
        return False

class TicTacToeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @app_commands.command(name="tictactoe", description="Challenge another player to a game of Tic-Tac-Toe.")
    async def start_game(self, interaction: discord.Interaction, player2: discord.User):
        player1 = interaction.user

        if player1.id in self.games or player2.id in self.games:
            await interaction.response.send_message("One of the players is already in a game!", ephemeral=True)
            return

        await interaction.response.defer()
        await interaction.followup.send(f"{player2.mention}, you have been challenged to a game of Tic-Tac-Toe by {player1.display_name}. Do you accept? (yes/no)")

        def check(m):
            return m.author == player2 and m.channel == interaction.channel and m.content.lower() in ["yes", "no"]

        try:
            response = await self.bot.wait_for('message', check=check, timeout=60.0)
            if response.content.lower() == "yes":
                game = TicTacToe(player1, player2)
                self.games[player1.id] = game
                self.games[player2.id] = game
                await interaction.followup.send(f"{player2.display_name} accepted the challenge! The game is starting now!")
                await interaction.followup.send(game.print_board())
                await interaction.followup.send(f"It's {game.current_player.display_name}'s turn ({'❌' if game.players[game.current_player] == 'X' else '⭕'}):")
            else:
                await interaction.followup.send(f"{player2.display_name} declined the game.")
        except asyncio.TimeoutError:
            await interaction.followup.send(f"{player2.display_name} did not respond in time. Challenge canceled.")

    @app_commands.command(name="move", description="Make a move in your Tic-Tac-Toe game.")
    @app_commands.describe(position="The position to place your mark (1-9)")
    async def make_move(self, interaction: discord.Interaction, position: int):
        player = interaction.user
        if player.id not in self.games:
            await interaction.response.send_message("You are not in a game!", ephemeral=True)
            return
        
        game = self.games[player.id]
        if game.current_player != player:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        position -= 1  
        if position < 0 or position > 8:
            await interaction.response.send_message("Invalid position! Choose a number between 1 and 9.", ephemeral=True)
            return

        result = game.make_move(position, player)
        await interaction.response.send_message(game.print_board())
        if result:
            await interaction.followup.send(result)
            del self.games[game.players[player].id]
            del self.games[game.get_opponent(player).id]
        else:
            await interaction.followup.send(f"It's {game.current_player.display_name}'s turn ({'❌' if game.players[game.current_player] == 'X' else '⭕'}):")

    @app_commands.command(name="endgame", description="End your current game of Tic-Tac-Toe.")
    async def end_game(self, interaction: discord.Interaction):
        player = interaction.user
        if player.id in self.games:
            game = self.games[player.id]
            opponent = game.get_opponent(player)
            del self.games[player.id]
            del self.games[opponent.id]
            await interaction.response.send_message("The game has been ended.")
        else:
            await interaction.response.send_message("You are not in a game!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicTacToeCog(bot))
