import voxelbotutils as utils

import discord
from discord.ext import commands

class PingCommand(utils.Cog):

    @utils.command()
    async def ping(self, ctx:utils.Context):
        """
        A sexy lil ping command for the bot.
        """

        with utils.Embed(use_random_colour=True) as e:
            e.title = "Pong!"
            e.add_field('Latency', self.bot.latency)
            return await ctx.send(embed = e)


def setup(bot:utils.Bot):
    x = PingCommand(bot)
    bot.add_cog(x)
