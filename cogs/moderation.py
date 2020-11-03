import voxelbotutils as utils
import discord
from discord.ext import commands


class Moderation(utils.Cog):

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


def setup(bot:utils.Bot):
    x = Moderation(bot)
    bot.add_cog(x)