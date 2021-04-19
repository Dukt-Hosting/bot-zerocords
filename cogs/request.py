import voxelbotutils as utils
from discord.ext import menus
from discord.ext import commands
import json
from datetime import datetime

now = datetime.now()

class InfractionSource(menus.ListPageSource):

    def format_page(self, menu:menus.Menu, entries:list) -> utils.Embed:
        """
        Format the infraction entries into an embed.
        """

        with utils.Embed(use_random_colour=True) as embed:
            for row in entries:
                # TODO add timestamp
                embed.add_field(f"#{row['request_id']} : {row['request_title']}", inline=False)
            embed.set_footer(f"Page {menu.current_page + 1}/{self.get_max_pages()}")
        return embed

class BugReports(utils.Cog):

    @utils.command()
    async def submit(self, ctx:utils.Context, *, content:str):
        """
        Submits a request to the Admins of the server. 

        The first line of the request is the title.
        """

        # Get the next open ID then slap it all into the database
        async with self.bot.database() as db:
            allbugs = len(await db("SELECT * FROM current_bugs"))
            await db("INSERT INTO current_bugs VALUES ($1, $2, $3, $4, $5, $6)", allbugs + 1, content.split('\n')[0], hastecontent, False, ctx.author.id, f"https://hastebin.com/{key}")

        # Make an embed and send it to discord!
        with utils.Embed(use_random_colour=True) as e:
            e.title = "Bug Reported!"
            await ctx.send(embed = e)

    @utils.command()
    async def allbugs(self, ctx:utils.Context, accepted:bool=False):
        """
        Lists all requests in the database with a bool query (Default is unfinished)
        """
        # Check if the user has permissions
        if ctx.author.id not in self.bot.config['bug_perms']:
            return await ctx.send("You don't have perms to run this command!")

        # Get the bugs that fit the bool query
        async with self.bot.database() as db:
            rows = await db('SELECT * FROM current_bugs WHERE completed=$1', completed)

        # If there is more than 1 row, start the menu. Else, send that there is no bugs
        if len(rows) > 0:
            pages = menus.MenuPages(source=InfractionSource(rows, per_page=5), clear_reactions_after=True, delete_message_after=True)
            await pages.start(ctx)
        else:
            await ctx.send("No Open Bugs! Woo Hoo!")

    @utils.command()
    async def setpriority(self, ctx:utils.Context, bug_id:int, priority:str):
        """
        Sets the priority of a bug (low, medium, or high)
        """
        # Check if the user has permissions
        if ctx.author.id not in self.bot.config['bug_perms']:
            return await ctx.send("You don't have perms to run this command!")

        # Set the valid prioritys
        prioritys = ['low', 'medium', 'high']

        # If the given priority is not in the list, return a big bad error message
        if priority not in prioritys:
            return await ctx.send("Not a valid priority!")

        # Get the bug associated with the ID
        async with self.bot.database() as db:
            rows = await db("SELECT * FROM current_bugs WHERE bug_id = $1", bug_id)

        # If there is no bug, then the ID is not correct
        if len(rows) == 0:
            return await ctx.send("No bugs found!")

        # Update the bug priority
        async with self.bot.database() as db:
            await db("UPDATE current_bugs SET priority = $2 WHERE bug_id = $1", bug_id, priority)

        # Send the cool message that it was done 
        await ctx.send("Successfully completed that action!")

    @utils.command()
    async def setbugstate(self, ctx, bug_id:int, state:bool):
        """
        Sets the completed state of a bug (True or False)
        """
        # Check if the user has permissions
        if ctx.author.id not in self.bot.config['bug_perms']:
            return await ctx.send("You don't have perms to run this command!")

        # Get the bug associated with the ID
        async with self.bot.database() as db:
            rows = await db("SELECT * FROM current_bugs WHERE bug_id = $1", bug_id)

        # If there is no bug, then the ID is not correct
        if len(rows) == 0:
            return await ctx.send("No bugs found!")

        # Update the bug with the ID
        async with self.bot.database() as db:
            await db("UPDATE current_bugs SET completed = $2 WHERE bug_id = $1", bug_id, state)

        await ctx.send("Successfully completed that action!")

    @utils.command()
    async def getbug(self, ctx:utils.Context, bug_id:int):
        """
        Gets the content of a bug
        """
        # Check if the user has permissions
        if ctx.author.id not in self.bot.config['bug_perms']:
            return await ctx.send("You don't have perms to run this command!")
        
        # Get the bug associated with the ID
        async with self.bot.database() as db:
            rows = await db("SELECT * FROM current_bugs WHERE bug_id = $1", bug_id)

        # If there is no bug, then the ID is not correct
        if len(rows) == 0:
            return await ctx.send("No bugs found!")

        # Get the single row
        row = rows[0]

        # Make the embed and send it
        with utils.Embed(use_random_colour=True) as e:
            e.title = f"#{row['bug_id']} : {row['bug_title']}"
            e.description = row['hastebin_link'] + "\n\n" + row['bug_desc']
            await ctx.send(embed = e)

def setup(bot:utils.Bot):
    x = BugReports(bot)
    bot.add_cog(x)
