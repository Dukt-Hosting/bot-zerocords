import voxelbotutils as utils

import discord
from discord.ext import commands

import random
from random import seed, randint

class BaseCords(utils.Cog):
        
    AUDIT_CHANNEL = 762455404625133598
    WORLD_NEWS_CHANNEL = 762451686098206730
    SPACE_NEWS_CHANNEL = 762453453842415617
    DEBUG_CHANNEL = 743724517108744212

    @utils.command(aliases=['ccc'])
    @commands.has_any_role(762460134307528764)
    async def createcountrychannels(self, ctx:utils.Context, user:discord.Member, categoryname:str, countryprefix:str):
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
        with utils.Embed(use_random_colour=True) as e:
            channel = self.bot.get_channel(self.AUDIT_CHANNEL)
            e.title = f'Command Ran: ccc'
            e.description= f'Category was created for {categoryname}!'
            e.set_author_to_user(ctx.author)
            await channel.send(embed = e)

    @utils.command(aliases=['rcc'])
    @commands.has_any_role(762460134307528764)
    async def removecountrychannels(self, ctx:utils.Context, categoryid:int):
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
        with utils.Embed(use_random_colour=True) as e:
            channel = self.bot.get_channel(self.AUDIT_CHANNEL)
            e.title = f'Command Ran: rcc'
            e.description= f'Category with the name of: {cachename} removed!'
            e.set_author_to_user(ctx.author)
            await channel.send(embed = e)

    @utils.command(aliases=['wn'])
    @commands.has_any_role(762460134307528764, 762460123629092874)
    async def worldnews(self, ctx:utils.Context, country, *, info):
        with utils.Embed(use_random_colour=True) as e:
            if len(ctx.message.attachments) > 0:
                e.set_image(url=ctx.message.attachments[0].url)
            channel = self.bot.get_channel(self.WORLD_NEWS_CHANNEL)
            e.title=country.upper()
            e.description=info
            e.set_author_to_user(ctx.author)
            await channel.send('<@&762451734190227466>')
            await channel.send(embed = e)
        
    @utils.command(aliases=['sn'])
    @commands.has_any_role(762460134307528764, 762460123629092874)
    async def spacenews(self, ctx:utils.Context, country, *, info):
        with utils.Embed(use_random_colour=True) as e:
            if len(ctx.message.attachments) > 0:
                e.set_image(url=ctx.message.attachments[0].url)
            channel = self.bot.get_channel(self.SPACE_NEWS_CHANNEL)
            e.title=country
            e.description=info
            e.set_author_to_user(ctx.author)
            await channel.send('<@&762451734190227466>')
            await channel.send(embed = e)

    @utils.command()
    @commands.has_any_role(762460134307528764)
    async def setcountry(self, ctx:utils.Context, member : discord.Member, role : discord.Role):
        '''Adds user to a country and adds them to the database'''
        await member.add_roles(role)
        embedvar = discord.Embed(title = f'Succesfully Added The Role!', description = f'Succesfully Added {role.mention} To {member.mention}!', color=0x059fff)
        await ctx.send(embed = embedvar)
        
    @utils.command()
    @commands.has_any_role(762460134307528764)
    async def removecountry(self, ctx:utils.Context, member : discord.Member, roletoremove : discord.Role):
        await member.remove_roles(roletoremove)
        embedvar = discord.Embed(title = f'Succesfully Removed The Role!', description = f'Succesfully Removed {roletoremove.mention} From {member.mention}!', color=0x059fff)
        await ctx.send(embed = embedvar)
        
    @utils.command()
    async def roll(self, ctx:utils.Context, sides):
        '''Roll A Dice And Go!'''
        await ctx.send(f'Grabbing The D{sides}')
        for _ in range(1):
            roll = randint(1, int(sides))
            
            
        sembed = discord.Embed(title = f'I Rolled Your D{sides}', description = f'***These Results Are Purely Random***', color = 0x059fff)
        sembed.add_field(name='Roll: ', value=roll, inline=True)
        sembed.add_field(name='Dice: ', value=f'D{sides}', inline=True)
        await ctx.send(embed = sembed)
        
    @utils.command()
    async def guidelines(self, ctx:utils.Context, choice=None):
        if choice != None:
            if choice == 'combat':
                sembed = discord.Embed(title = f'Combat Guidelines / Regulations', description = f'***The Guidelines And Rules For Combat***', color = 0x059fff)
                sembed.add_field(name=f'Combat:', value=f'1. In this server you use dice to decide the outcome of actions. \n 2. To Roll A Dice Use "n!roll 20" \n 3. The higher you roll the higher the attack/defence is. \n 4. There will be a game master in every war/battle. Ping a staff member for a gamemaster. \n ***Base your rolls on 1-20 with 1 being the worst and 20 the best.***', inline=True)
                await ctx.send(embed = sembed)
        if choice == None:
            sembed = discord.Embed(title = f'Roleplay Guidlines / Regulations', description = f'***Available Categorys:***', color = 0x059fff)
            sembed.add_field(name=f'`combat`', value=f'General Combat Guidelines', inline=True)
            await ctx.send(embed = sembed)

    @utils.command(aliases=['wnr'])
    async def worldnewsrole(self, ctx:utils.Context):
        await ctx.author.add_roles(ctx.guild.get_role(762451734190227466))
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
