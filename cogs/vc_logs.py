import discord
import voxelbotutils as utils

from datetime import datetime as dt, timedelta

class VCLogs(utils.Cog):

    @utils.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
        """
        Log users joining or leaving VCs.
        """
        if before.channel == after.channel:
            return
        update_log_id = self.bot.guild_settings[member.guild.id]['voice_update_modlog_channel_id']
        if not update_log_id:
            return
        channel = self.bot.get_channel(update_log_id)
        if not channel:
            return
        try:
            if before.channel is None:
                text = f"{member.mention} joined the **{after.channel.name}** VC."
            elif after.channel is None:
                text = f"{member.mention} left the **{before.channel.name}** VC."
            else:
                text = f"{member.mention} moved from the **{before.channel.name}** VC to the **{after.channel.name}** VC."
            if channel.permissions_for(channel.guild.me).embed_links:
                embed = utils.Embed(use_random_colour=True, description=text)
                embed.timestamp = dt.utcnow()
                data = {"embed": embed}
            else:
                data = {"content": text, "allowed_mentions": discord.AllowedMentions(users=False)}
            await channel.send(**data)
        except discord.Forbidden:
            pass


def setup(bot:utils.Bot):
    x = VCLogs(bot)
    bot.add_cog(x)