import os
import discord
from discord.ext import commands
from .utils.dataIO import fileIO
import operator

class WhoPlays:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def whoplays(self, ctx, *, game:str):
        """Shows a list of all the members"""

        if len(game) <= 2:
            await self.bot.say("You need at least 3 characters.")
            return 
              
        server = ctx.message.server
        members = server.members

        playing_game = ""
        for member in members:
            if member.game is not None:
                if game.lower() in member.game.name.lower():
                    playing_game += "+ {} ({})\n".format(member.name, member.game.name)              

        if not playing_game:
            await self.bot.say("No one is playing that game.")
        else:
            msg = "```python\n"
            msg += "These are the people who are playing {}: \n".format(game)
            msg += playing_game
            msg += "```"           
            await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    async def cgames(self, ctx):
        """Shows the currently most played games"""
        server = ctx.message.server
        members = server.members

        freq_list = {}
        for member in members:
            if member.game is not None:
                if member.game.name not in freq_list:
                    freq_list[member.game.name] = 0
                freq_list[member.game.name]+=1

        sorted_list = sorted(freq_list.items(), key=operator.itemgetter(1))    

        if not freq_list:
            await self.bot.say("Surprisingly, no one is playing anything.")
        else:            
            # create display
            msg = "```These are the server's most played games at the moment: \n\n"
            msg += "{:<25s}{:>25s}\n".format("Game:", "# Playing:")
            count = 0
            for game in freq_list.keys():
                if count < 10:
                    if len(game) > 25:
                        trunc_game = game [0:21] + "..."
                        msg+= "{:<25s}{:>25d}\n".format(trunc_game, freq_list[game])
                    else:
                        msg+= "{:<25s}{:>25d}\n".format(game, freq_list[game])
                count += 1
            msg += "```" 
            await self.bot.say(msg)         


def setup(bot):
    n = WhoPlays(bot)
    bot.add_cog(n)