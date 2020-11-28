from discord.ext import commands
import discord
import voxelbotutils as utils
from datetime import datetime as dt, timedelta


class GuildUpdateHandler(utils.Cog):

    @utils.Cog.listener()
    async def on_guild_channel_create(self, channel:discord.TextChannel):
        create_time = dt.utcnow()
        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create, limit=1):
            if entry.user.bot == True:
                break
            if entry.target.id != channel.id:
                break
            if entry.user == self.bot.user:
                break
            with utils.Embed(use_random_colour=True) as embed:
                embed.title = "Channel Created"
                embed.add_field(name="User", value=f'{entry.user.mention}\n(`{entry.user.id}`)')
                embed.add_field(name="Channel", value=f'{channel.mention}\n(`{channel.id}`)')
                embed.set_author_to_user(entry.user)
                embed.timestamp = create_time
        channel_id = self.bot.guild_settings[channel.guild.id].get("guild_update_channel_id")
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        # Send log
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
    
    @utils.Cog.listener()
    async def on_guild_channel_delete(self, channel:discord.TextChannel):
        create_time = dt.utcnow()
        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1):
            if entry.user.bot == True:
                break
            if entry.target.id != channel.id:
                break
            if entry.user == self.bot.user:
                break
            with utils.Embed(use_random_colour=True) as embed:
                embed.title = "Channel Deleted"
                embed.add_field(name="User", value=f'{entry.user.mention}\n(`{entry.user.id}`)')
                embed.add_field(name="Channel", value=f'**#{channel.name}**\n(`{channel.id}`)')
                embed.set_author_to_user(entry.user)
                embed.timestamp = create_time
        channel_id = self.bot.guild_settings[channel.guild.id].get("guild_update_channel_id")
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        # Send log
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
    
    @utils.Cog.listener()
    async def on_guild_channel_update(self, before:discord.TextChannel, after:discord.TextChannel):
        async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1):
            if entry.user.bot == True:
                break
            with utils.Embed(use_random_colour=True) as embed:
                embed.title = "Channel Updated!"
                embed.description = f"**#{before.name} was updated!**"
                embed.set_author_to_user(entry.user)
                if before.name != after.name:
                    embed.add_field(name="Name", value=f"**{before.name} => {after.name}**")
                if before.category != after.category:
                    embed.add_field(name="Category", value=f"**{before.category.name} => {after.category.name}**")
                if before.topic != after.topic:
                    before_topic = before.topic
                    if not before.topic:
                        before_topic = "None"
                    if len(before_topic) > 50:
                        before_topic= before.topic[:50] + '...'
                    after_topic = after.topic
                    if not after.topic:
                        after_topic = "None"

                    if len(after_topic) > 50:
                        after_topic = after.topic[:50] + '...'
                    embed.add_field(name="Topic", value=f"**{before_topic} => {after_topic}**")
                if before.position != after.position:
                    embed.add_field(name="Position", value=f"**{before.position} => {after.position}**")
                if before.slowmode_delay != after.slowmode_delay:
                    embed.add_field(name="Slowmode Delay", value=f"**{before.slowmode_delay} => {after.slowmode_delay}  **")

        channel_id = self.bot.guild_settings[before.guild.id].get("guild_update_channel_id")
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
    
    @utils.Cog.listener()
    async def on_member_ban(self, guild:discord.Guild, user:discord.Member):
        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):
            if entry.user.bot == True:
                break
            if user.id != entry.target.id:
                break
            if guild.id != entry.user.guild.id:
                break
            await self.bot.dispatch('moderation_action', moderator=entry.user, user=entry.target, reason=entry.reason, action="ban")
    
    @utils.Cog.listener()
    async def on_member_unban(self, guild:discord.Guild, user:discord.Member):
        async for entry in guild.audit_logs(action=discord.AuditLogAction.unban, limit=1):
            if entry.user.bot == True:
                break
            if user.id != entry.target.id:
                break
            if guild.id != entry.user.guild.id:
                break
            await self.bot.dispatch('moderation_action', moderator=entry.user, user=user, reason=entry.reason, action="ban")
        

def setup(bot:utils.Bot):
    x = GuildUpdateHandler(bot)
    bot.add_cog(x)