import voxelbotutils as utils

import discord
from discord.ext import commands

import random
from random import seed, randint

class BaseCords(utils.Cog):

    @utils.command(aliases=['suggest'])
    async def suggestion(self, ctx, *, suggestion:str):
        guild = self.bot.get_guild(750337633338654813)
        channel = guild.get_channel(781708362563584001)
        with utils.Embed(use_random_colour=True) as embed:
            embed.title = "Zerocords Suggestion"
            embed.description = f"Guild:\n```{ctx.guild.id}```\n\nUser:\n```({ctx.author.id}/{ctx.author.name}#{ctx.author.discriminator})```\n\nSuggestion:```\n{suggestion}```"
            await channel.send(embed=embed)

    @utils.command(aliases=['ccc'])
    @commands.has_permissions(manage_channels=True)
    async def createcountrychannels(self, ctx:utils.Context, user:discord.Member, categoryname:str, countryprefix:str):
        async with self.bot.database() as db:
            audit_channel = await db("SELECT audit_channel FROM guild_settings WHERE guild_id=$1", ctx.guild.id)
        channeltypes = ['culture', 'news', 'economy', 'general', 'military', 'relations', 'projects', 'wars']
        category = await ctx.guild.create_category(categoryname)
        for name in channeltypes:
            channel = await ctx.guild.create_text_channel(
                f"{countryprefix}-{name}",
                reason=f"Country ({countryprefix}) channels created, command ran by {ctx.author.name}",
                topic=f"{categoryname} - {name} ",
                category=category,
            )
        prichannel = await ctx.guild.create_text_channel(
            f"{countryprefix}-private",
            reason=f"Country ({countryprefix}) channels created, command ran by {ctx.author.name}",
            topic=f"{categoryname} - private",
            category=category,
        )
        role = await ctx.guild.create_role(reason='ZeroCords - Auto made a countrys role', hoist=True, name=categoryname)
        await prichannel.set_permissions(role, read_messages=True)
        await prichannel.set_permissions(ctx.guild.default_role, read_messages=False)
        await user.add_roles(role)
        await ctx.send(f'Channels made with the prefix of {countryprefix}!')
        if str(audit_channel[0]["audit_channel"]) == "None":
            return
        else:
            with utils.Embed(use_random_colour=True) as e:
                channel = self.bot.get_channel(audit_channel[0]["audit_channel"])
                e.title = f'Command Ran: ccc'
                e.description= f'Category was created for {categoryname}!'
                e.set_author_to_user(ctx.author)
                await channel.send(embed = e)
    
    @utils.command(aliases=['ccs'])
    @commands.has_permissions(manage_channels=True)
    async def createcompanychannels(self, ctx:utils.Context, user:discord.Member, categoryname:str, countryprefix:str):
        if ctx.guild is None:
            await ctx.send("Hey there! :wave:. You tried to run a command that can't be used outside servers!.")
        async with self.bot.database() as db:
            audit_channel = await db("SELECT audit_channel FROM guild_settings WHERE guild_id=$1", ctx.guild.id)
        channeltypes = ['info', 'worth', 'general', 'projects']
        category = await ctx.guild.create_category(categoryname)
        for name in channeltypes:
            channel = await ctx.guild.create_text_channel(
                f"{countryprefix}-{name}",
                reason=f"Country ({countryprefix}) channels created, command ran by {ctx.author.name}",
                topic=f"{categoryname} - {name} ",
                category=category,
            )
        prichannel = await ctx.guild.create_text_channel(
            f"{countryprefix}-private",
            reason=f"Country ({countryprefix}) channels created, command ran by {ctx.author.name}",
            topic=f"{categoryname} - private",
            category=category,
        )
        role = await ctx.guild.create_role(reason='ZeroCords - Auto made a countrys role', hoist=True, name=categoryname)
        await prichannel.set_permissions(role, read_messages=True)
        await prichannel.set_permissions(ctx.guild.default_role, read_messages=False)
        await user.add_roles(role)
        await ctx.send(f'Channels made with the prefix of {countryprefix}!')
        if audit_channel == None:
            return
        else:
            with utils.Embed(use_random_colour=True) as e:
                channel = self.bot.get_channel(audit_channel[0]["audit_channel"])
                e.title = f'Command Ran: ccc'
                e.description= f'Category was created for {categoryname}!'
                e.set_author_to_user(ctx.author)
                await channel.send(embed = e)

    @utils.command(aliases=['rcs'])
    @commands.has_permissions(manage_channels=True)
    async def removechannelsets(self, ctx:utils.Context, categoryid:int):
        async with self.bot.database() as db:
            audit_channel = await db("SELECT audit_channel FROM guild_settings WHERE guild_id=$1", ctx.guild.id)
        cat = self.bot.get_channel(categoryid)
        cachename = cat.name
        for role in ctx.guild.roles:
            if role.name == cachename:
                await role.delete()
        for channel in cat.text_channels:
            await channel.delete()
        for channel in cat.voice_channels:
            await channel.delete()
        await cat.delete()
        await ctx.send(f'Removed the channels from {cachename}')
        if audit_channel[0]["audit_channel"] is None:
            return
        else:
            with utils.Embed(use_random_colour=True) as e:
                channel = self.bot.get_channel(audit_channel[0]["audit_channel"])
                e.title = f'Command Ran: rcc'
                e.description= f'Category with the name of: {cachename} removed!'
                e.set_author_to_user(ctx.author)
                await channel.send(embed = e)

    @utils.command(aliases=['wn'])
    @commands.has_permissions(send_messages=True)
    async def worldnews(self, ctx:utils.Context, country, *, info):
        with utils.Embed(use_random_colour=True) as e:
            async with self.bot.database() as db:
                worldnews_channel = await db("SELECT worldnews_channel FROM guild_settings WHERE guild_id=$1", ctx.guild.id)
                news_role = await db('SELECT news_role FROM guild_settings WHERE guild_id=$1', ctx.guild.id)
            channel = self.bot.get_channel(worldnews_channel[0]["worldnews_channel"])
            if len(ctx.message.attachments) > 0:
                e.set_image(url=ctx.message.attachments[0].url)
            e.title=country.upper()
            e.description=info
            e.set_author_to_user(ctx.author)
            await channel.send(f'<@&{news_role[0]["news_role"]}>', embed = e)
        
    @utils.command(aliases=['sn'])
    @commands.has_permissions(send_messages=True)
    async def spacenews(self, ctx:utils.Context, country, *, info):
        with utils.Embed(use_random_colour=True) as e:
            async with self.bot.database() as db:
                spacenews_channel = await db("SELECT spacenews_channel FROM guild_settings WHERE guild_id=$1", ctx.guild.id)
                news_role = await db('SELECT news_role FROM guild_settings WHERE guild_id=$1', ctx.guild.id)
            channel = self.bot.get_channel(spacenews_channel[0]["spacenews_channel"])
            if len(ctx.message.attachments) > 0:
                e.set_image(url=ctx.message.attachments[0].url)
            e.title=country
            e.description=info
            e.set_author_to_user(ctx.author)
            await channel.send(f'<@&{news_role[0]["news_role"]}>', embed=e)

    @utils.command()
    @commands.has_permissions(manage_roles=True)
    async def setcountry(self, ctx:utils.Context, member : discord.Member, role : discord.Role):
        '''Adds user to a country and adds them to the database'''
        await member.add_roles(role)
        embedvar = discord.Embed(title = f'Succesfully Added The Role!', description = f'Succesfully Added {role.mention} To {member.mention}!', color=0x059fff)
        await ctx.send(embed = embedvar)
        
    @utils.command()
    @commands.has_permissions(manage_roles=True)
    async def removecountry(self, ctx:utils.Context, member : discord.Member, roletoremove : discord.Role):
        await member.remove_roles(roletoremove)
        embedvar = discord.Embed(title = f'Succesfully Removed The Role!', description = f'Succesfully Removed {roletoremove.mention} From {member.mention}!', color=0x059fff)
        await ctx.send(embed = embedvar)
        
    @utils.command()
    async def roll(self, ctx:utils.Context, sides:int):
        '''Roll A Dice And Go!'''
        await ctx.send(f'Grabbing The D{sides}')
        for _ in range(1):
            roll = randint(1, int(sides))
            
            
        sembed = discord.Embed(title = f'I Rolled Your D{sides}', description = f'***These Results Are Purely Random***', color = 0x059fff)
        sembed.add_field(name='Roll: ', value=roll, inline=True)
        sembed.add_field(name='Dice: ', value=f'D{sides}', inline=True)
        await ctx.send(embed = sembed)
        

    @utils.command(aliases=['wnr'])
    async def worldnewsrole(self, ctx:utils.Context):
        """Give you the worldnews role"""
        async with self.bot.database() as db:
            news_role_db = await db('SELECT news_role FROM guild_settings WHERE guild_id=$1', ctx.guild.id)
        news_role = news_role_db[0]["news_role"]
        if news_role is None:
            await ctx.send(f'Looks like this server has not setup a news role, ask a admin to do it with `{ctx.clean_prefix}setup`')
        else:
            await ctx.author.add_roles(ctx.guild.get_role(news_role))
            await ctx.send('Gave you the world news role.')
"""
    @utils.command()
    async def wiki(self, ctx:utils.Context, *, countryname):
        country = CountryInfo(countryname)
        wikiarticle = country.wiki()
        await ctx.send(wikiarticle)
        

    @utils.command()
    async def irlstats(self, ctx:utils.Context, *, countryname):
        country = CountryInfo(countryname)
        kmaera = country.area()
        popu = country.population()
        capital = country.capital()
        wikiarticle = country.wiki()
        embedVar = discord.Embed(title="Country info", description='country stats', color=0x00ff00)
        embedVar.add_field(name="Area (km)", value=kmaera, inline=True)
        embedVar.add_field(name="Capital", value=capital, inline=True)
        embedVar.add_field(name="Population", value=popu, inline=True)
        embedVar.add_field(name="Wikipedia", value=wikiarticle, inline=True)
        await ctx.send(embed=embedVar)
"""

def setup(bot:utils.Bot):
    x = BaseCords(bot)
    bot.add_cog(x)
