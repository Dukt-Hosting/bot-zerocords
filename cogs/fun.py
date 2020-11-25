import voxelbotutils as utils

import discord
from discord.ext import commands

import random
from random import seed, randint

class BaseCords(utils.Cog):

    @utils.command()
    async def meme(self, ctx:utils.Context):
        """
        Gives you a fresh meme
        """
        url = "http://maps.googleapis.com/maps/api/geocode/json?address=googleplex&sensor=false"
        r = await self.bot.session.get('https://meme-api.herokuapp.com/gimme')
        data = await r.json()
        with utils.Embed(use_random_colour=True) as e:
            e.title = f'Meme: {data["title"]}.'
            e.url = data['postLink']
            e.set_image(url=data["url"])
            #e.author = "👍 " + str(data['ups']) + " | r/" + data['subreddit']
            e.set_author(name=f"👍 {data['ups']} | r/{data['subreddit']}")
            e.add_field("NSFW",data['nsfw'])
            e.add_field("Spoiler",data['spoiler'])
            e.add_field("Author",data['author'])
            await ctx.send(embed=e)

def setup(bot:utils.Bot):
    x = BaseCords(bot)
    bot.add_cog(x)
