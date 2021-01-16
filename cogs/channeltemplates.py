import voxelbotutils as utils

import discord
from discord.ext import commands

from treelib import Tree
    
class ChannelTemplate(utils.Cog):

    @utils.command()
    async def storetemplate(self, ctx:utils.Context, name:str, id:discord.CategoryChannel):
        async with self.bot.database() as db:
            data = await db("SELECT * FROM channel_templates WHERE guild_id=$1", ctx.guild.id)
        duplicatecounter = [i for i in data if i["name"] == name]
        if len(duplicatecounter) >= 1:
            return await ctx.send("There is already a template with this name!")
        subchannels = id.channels # replace with method to get all channels in a category
        data = {
            "categorychannel": id.name,
            "subchannels": [{"type":i.type, "name":i.name} for i in subchannels]
        }
        # INSERT INTO channel_templates VALUES (ctx.guild.id, str(data));
        async with self.bot.database() as db:
            await db("INSERT INTO channel_templates VALUES ($1, $2);", ctx.guild.id, str(data))

        tree = Tree()
        tree.create_node(id.name, id.name)
        for i in subchannels:
            if i.type == "voice":
                tree.create_node("🔊" + i.name, i.name, id.name)
            if i.type == "text":
                tree.create_node("#" + i.name, i.name, id.name)

        with utils.Embed(use_random_colour=True) as embed:
            embed.title = "Saved template!"
            embed.description = f"```\n{tree}\n```"

    @utils.command()
    async def createchannelwithtemplate (self, ctx:utils.Context, name:str, user:discord.Member, countryprefix, *, countryname):
        async with self.bot.database() as db:
            templates = await db("SELECT * FROM channel_templates WHERE guild_id=$1")
        templatedata = [i for i in templates if i["name"] == name]
        templatedata = templatedata[0]
        category = await ctx.guild.create_category(templatedata['categorychannel'].replace("{}", countryprefix))
        for i in templatedata["subchannels"]:
            if i["type"] == "voice":
                channel = await ctx.guild.create_voice_channel(
                    i["name"].replace("{}", countryprefix),
                    reason=f"Company ({countryprefix}) channels created, command ran by {ctx.author.name}({ctx.author.id})",
                    category=category,
                )
            if i["type"] == "text":
                channel = await ctx.guild.create_voice_channel(
                    i["name"].replace("{}", countryprefix),
                    reason=f"Company ({countryprefix}) channels created, command ran by {ctx.author.name}({ctx.author.id})",
                    category=category,
                )
        role = await ctx.guild.create_role(reason=f'ZeroCords - Auto made a company role{ctx.author.name}({ctx.author.id})', hoist=True, name=countryname)

def setup(bot:utils.Bot):
    x = ChannelTemplate(bot)
    bot.add_cog(x)
