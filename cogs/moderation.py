import voxelbotutils as utils
import discord
from discord.ext import commands


class Moderation(utils.Cog):

    AUDIT_CHANNEL = 743724517108744212
    WORLD_NEWS_CHANNEL = 743724517108744212
    SPACE_NEWS_CHANNEL = 762453453842415617

    @utils.command()
    @commands.has_any_role(762460134307528764)
    async def kick(self, ctx:utils.Context, user:discord.Member, *, reason:str='<No reason provided>'):
        """
        Kicks a user from the server.
        """

        # Add mod check to target user

        # DM the user
        dm_reason = f"You have been kicked from **{ctx.guild.name}** with the reason `{reason}`."
        try:
            await user.send(dm_reason)
        except discord.Forbidden:
            pass  # Can't DM the user? Oh well
        except discord.HTTPException:
            pass  # Can't DM the user? Oh well

        # Kick the user
        manage_reason = f"{ctx.author!s}: {reason}"
        try:
            await user.kick(reason=manage_reason)
        except discord.Forbidden:
            return await ctx.send(f"I was unable to kick {user.mention}.")
        except discord.NotFound:
            return await ctx.send("To me it looks like that user doesn't exist :/")

        # Throw the reason into the database
        self.bot.dispatch("moderation_action", moderator=ctx.author, user=user, reason=reason, action="Kick")

        # Output to chat
        return await ctx.send(f"{user.mention} has been kicked by {ctx.author.mention} with reason `{reason}`.")

    
    @utils.command(aliases=['purge', 'clear', 'delete'])
    @commands.has_any_role(762460134307528764)
    async def _purgemsg(self, ctx:utils.Context, amount:int):
        ctx.channel.purge(limit=amount+1)
        with utils.Embed(use_random_colour=True) as e:
            e.title = f'Cleared Messages!'
            e.description= f'Cleared {amount} messages in this channel!'
            await ctx.send(embed = e)
        with utils.Embed(use_random_colour=True) as e:
            channel = self.bot.get_channel(self.AUDIT_CHANNEL)
            e.title = f'Command Ran: purge'
            e.description= f'Cleared {amount} messages in {ctx.channel}'
            e.set_author_to_user(ctx.author)
            await channel.send(embed = e)



def setup(bot:utils.Bot):
    x = Moderation(bot)
    bot.add_cog(x)