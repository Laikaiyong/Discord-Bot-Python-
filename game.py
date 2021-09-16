import discord
from discord.ext import commands
import random as rd

# Tic Tac Toe
player_one = ""
player_two = ""
turn = ""
game_over = True
board = []

winning_condition = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


class Game(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tictactoe(self, ctx, p1: discord.Member, p2: discord.Member):
        global count
        global player_one
        global player_two
        global turn
        global game_over

        if game_over:
            global board
            board = [
                "\U00002B1C" * i for i in range(0, 9)]
            turn = ""
            game_over = False
            count = 0

            player_one = p1
            player_two = p2

            line = ""
            for index in range(len(board)):
                if index in [2, 5, 8]:
                    line += " " + board[index]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[index]

            num = rd.randint(1, 2)
            if num == 1:
                turn = player_one
                await ctx.send(f"It is {player_one.mention}'s turn.")
            elif num == 2:
                turn = player_two
                await ctx.send(f"It is {player_two.mention}'s turn.")
        else:
            await ctx.send("A game is already in progress. Finish it before starting anew one. \U0001F3AE")

    @commands.command()
    async def place(self, message, pos: int):
        global turn
        global player_one
        global player_two
        global board
        global count
        global game_over

        if not game_over:
            mark = ""
            if turn == player_one and message.author == player_one:
                mark = "\U0001F1FD"
            elif turn == player_two and message.author == player_two:
                mark = "\U0001F17E"
            if 0 < pos < 10 and board[pos-1] == "\U00002B1C":
                board[pos-1] = mark
                count += 1

                line = ""
                for index in range(len(board)):
                    if index in (2, 5, 8):
                        line += " " + board[index]
                        await message.channel.send(line)
                        line = ""
                    else:
                        line += " " + board[index]

                def check_winner(self, winning_condition, mark):
                    global game_over
                    for condition in winning_condition:
                        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                            game_over = True

                check_winner(winning_condition, mark)
                if game_over:
                    if mark == "\U0001F1FD":
                        await message.channel.send(player_one.mention + " wins! :trophy:")
                    else:
                        await message.channel.send(player_two.mention + " wins! :trophy:")
                elif count >= 9:
                    await message.channel.send("It's a tie.")

                if turn == player_one:
                    turn = player_two
                else:
                    turn = player_one

            else:
                await message.channel.send("It is not your turn.")

        else:
            await message.channel.send("Please start a new game. \U0001F3B2")

    @ tictactoe.error
    async def tictactoe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Plase mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Please make sure to mention / ping players (ie. {ctx.message.author.mention})")

    @ place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Plase enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")


def setup(client):
    client.add_cog(Game(client))
