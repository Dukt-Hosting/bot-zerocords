import voxelbotutils as utils
import discord
import random
from discord.ext import commands, menus
import asyncio

class InfractionSource(menus.ListPageSource):

    def format_page(self, menu:menus.Menu, entries:list) -> utils.Embed:
        """
        Format the infraction entries into an embed.
        """

        with utils.Embed(use_random_colour=True) as embed:
            for row in entries:
                # TODO add timestamp
                embed.add_field(f"**Name:** {row['name']}", f"\n**Environment:** {row['environment']}\n\n**Climate:** {row['climate']}\n\n**Time:** {row['maptime']}\n\n**Image URL:** {row['imageurl']}\n\n\n", inline=False)
            embed.set_footer(f"Page {menu.current_page + 1}/{self.get_max_pages()}")
        return embed

class Duels (utils.Cog):

    @utils.Cog.listener()
    async def on_command_error(self, ctx, exception):
        if isinstance(exception, asyncio.TimeoutError):
            await ctx.send("Command timeout reached! Re-run the command if you would like to restart!")


    @utils.command()
    async def startGame(self, ctx, user):
        """
        Starts a new duels match
        """
        users = [ctx.author, user]
        
        async with self.bot.database() as db:
            maps = await db('SELECT * FROM availableMaps')

        threeMaps = random.sample(maps, 3)


    @utils.group()
    async def map(self, ctx):
        """
        Map command group
        """

        if ctx.invoked_subcommand is not None:
            return


    @map.command()
    async def add(self, ctx:utils.Context, mapname):
        """
        Interactive prompt for adding a map to the game
        """

        async with self.bot.database() as db:
            mapsWithName = await db('SELECT * FROM availableMaps WHERE name=$1 AND guild_id=$2', mapname, ctx.guild.id)
            if len(mapsWithName) > 0:
                return await ctx.send("There is already a map with this name!")

        content, embed = ctx.get_context_message('What is the environment for this map?')
        botMsg = await ctx.send(content, embed=embed)
        environment = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)

        content, embed = ctx.get_context_message('What is the climate for this map?')
        await botMsg.edit(content=content, embed=embed)
        climate = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)

        content, embed = ctx.get_context_message('What is the time for this map?')
        await botMsg.edit(content=content, embed=embed)
        time = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)

        content, embed = ctx.get_context_message('What image do you want for this map?')
        await botMsg.edit(content=content, embed=embed)
        imageMsg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)

        if len(imageMsg.attachments) > 0:
            imageUrl = imageMsg.attachments[0].url
        else:
            imageUrl = imageMsg.content

        with utils.Embed() as embed:
            embed.title = "Does this look right?"
            embed.description = f"**Map name**: {mapname}\n\n**Environment**: {environment.content}\n\n**Climate**: {climate.content}\n\n**Time**: {time.content}\n\n**Image**:"
            embed.set_image(imageUrl)
            await botMsg.edit(embed=embed)

        await botMsg.add_reaction('\U00002705')
        await botMsg.add_reaction('\U0000274c')

        reaction, user = await self.bot.wait_for('reaction_add', check=lambda x, y: y == ctx.author)
        
        if reaction.emoji == '✅':
            async with self.bot.database() as db:
                await db('INSERT INTO availableMaps VALUES ($1, $2, $3, $4, $5, $6)', ctx.guild.id, mapname, environment.content, climate.content, time.content, imageUrl)

            return await ctx.message.reply("Map added!")

        if reaction.emoji == '❌':
            return await ctx.message.reply('Map adding canceled!')


    @map.command(aliases=['ls'])
    async def list(self, ctx):
        async with self.bot.database() as db:
            maps = await db('SELECT * FROM availableMaps')

        pages = menus.MenuPages(source=InfractionSource(maps, per_page=3), clear_reactions_after=True, delete_message_after=True)
        await pages.start(ctx)  


    @map.command(aliases=['remove', 'rm', 'del'])
    async def delete(self, ctx, mapname):
        async with self.bot.database() as db:
            maps = await db('SELECT * FROM availableMaps WHERE name=$1 AND guild_id=$2', mapname, ctx.guild.id)

        if not len(maps) > 0:
            return await ctx.send('There are no maps with this name.')

        content, embed = ctx.get_context_message('Are you sure you want to delete this map?')
        message = await ctx.send(content=content, embed=embed)

        await message.add_reaction('\U00002705')
        await message.add_reaction('\U0000274c')

        reaction, user = await self.bot.wait_for('reaction_add', check=lambda x, y: y == ctx.author)

        if reaction.emoji == '✅':
            async with self.bot.database() as db:
                await db('DELETE FROM availableMaps WHERE guild_id=$1 AND name=$2', ctx.guild.id, mapname)
            
            content, embed = ctx.get_context_message('Map deleted!')
            return await message.edit(content=content, embed=embed)

        if reaction.emoji == '❌':
            content, embed = ctx.get_context_message('Map deletion canceled.')
            return await message.edit(content=content, embed=embed)
            
        


def setup(bot: utils.Bot): 
    x = Duels(bot)
    bot.add_cog(x)