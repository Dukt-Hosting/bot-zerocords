from discord.ext import commands
import voxelbotutils as utils


class BotSettings(utils.Cog):

    @utils.group()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, add_reactions=True, manage_messages=True)
    @commands.guild_only()
    async def setup(self, ctx:utils.Context):
        """Talks the bot through a setup"""

        if ctx.invoked_subcommand is not None:
            return
        
        settings_mention = utils.SettingsMenuOption.get_guild_settings_mention
        
        menu = utils.SettingsMenu()
        menu.add_multiple_options(
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'Moderation Settings',
                callback=self.bot.get_command('setup mod'),
            ),
            
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'Modlog Settings',
                callback=self.bot.get_command('setup modlog'),
            ),
            
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'GeoPolitical Roleplay Settings',
                callback=self.bot.get_command('setup georp'),
            ),
        )
        
        try:
            await menu.start(ctx)
            await ctx.send("Done setting up!")
        except utils.errors.InvokedMetaCommand:
            pass
    
    @setup.command()
    @utils.checks.meta_command()
    async def mod(self, ctx:utils.Context):
        """Run the bot setup"""

        # Make sure it's only run as its own command, not a parent
        if ctx.invoked_subcommand is not None:
            return

        # Create settings menu
        menu = utils.SettingsMenu()
        settings_mention = utils.SettingsMenuOption.get_guild_settings_mention
        
        menu.add_multiple_options(
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'Set moderator role (currently {0})'.format(settings_mention(x, 'guild_moderator_role_id')),
                converter_args=(
                    utils.SettingsMenuConverter(
                        prompt='What do you want to set the moderator role to?',
                        asking_for='moderator role',
                        converter=commands.RoleConverter,
                    ),
                ),
                callback=utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'guild_moderator_role_id')
            ),
            
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'Set mute role (currently {0})'.format(settings_mention(x, 'muted_role_id')),
                converter_args=(
                    utils.SettingsMenuConverter(
                        prompt='What do you want to set the mute role to?',
                        asking_for='mute role',
                        converter=commands.RoleConverter,
                    ),
                ),
                callback=utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'muted_role_id')
            ),
        )

        try:
            await menu.start(ctx)
        except utils.errors.InvokedMetaCommand:
            pass

    @setup.command()
    @utils.checks.meta_command()
    async def modlog(self, ctx:utils.Context):
        """Talks the bot through a setup"""

        menu = utils.SettingsMenu()
        settings_mention = utils.SettingsMenuOption.get_guild_settings_mention
        
        menu.add_multiple_options(
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'hi there'.format(settings_mention(x, 'column')),
                converter_args=(
                    utils.SettingsMenuConverter(
                        prompt='What do you want to set X to?',
                        asking_for='X',
                        converter=commands.xconverter,
                    ),
                ),
                callback=x
            ),
            
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'hi there'.format(settings_mention(x, 'column')),
                converter_args=(
                    utils.SettingsMenuConverter(
                        prompt='What do you want to set X to?',
                        asking_for='X',
                        converter=commands.xconverter,
                    ),
                ),
                callback=x
            ),
            
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'hi there'.format(settings_mention(x, 'column')),
                converter_args=(
                    utils.SettingsMenuConverter(
                        prompt='What do you want to set X to?',
                        asking_for='X',
                        converter=commands.xconverter,
                    ),
                ),
                callback=x
            ),
        )
        
        menu.bulk_add_options(
            ctx,
            {
                'display': lambda c: "Set kick archive channel (currently {0})".format(settings_mention(c, 'kick_modlog_channel_id')),
                'converter_args': [("What channel do you want kicks to go to?", "modmail archive", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'kick_modlog_channel_id'),
            },
            {
                'display': lambda c: "Set ban archive channel (currently {0})".format(settings_mention(c, 'ban_modlog_channel_id')),
                'converter_args': [("What channel do you want bans to go to?", "modmail archive", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'ban_modlog_channel_id'),
            },
            {
                'display': lambda c: "Set mute archive channel (currently {0})".format(settings_mention(c, 'mute_modlog_channel_id')),
                'converter_args': [("What channel do you want mutes to go to?", "modmail archive", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'mute_modlog_channel_id'),
            },
            {
                'display': lambda c: "Set warn archive channel (currently {0})".format(settings_mention(c, 'warn_modlog_channel_id')),
                'converter_args': [("What channel do you want warns to go to?", "modmail archive", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'warn_modlog_channel_id'),
            },
            {
                'display': lambda c: "Set edited message archive channel (currently {0})".format(settings_mention(c, 'edited_message_modlog_channel_id')),
                'converter_args': [("What channel do you want edited message logs to go to?", "modmail archive", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'edited_message_modlog_channel_id'),
            },
            {
                'display': lambda c: "Set deleted message archive channel (currently {0})".format(settings_mention(c, 'deleted_message_modlog_channel_id')),
                'converter_args': [("What channel do you want deleted message logs to go to?", "modmail archive", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'deleted_message_modlog_channel_id'),
            },
            {
                'display': lambda c: "Set voice update log channel (currently {0})".format(settings_mention(c, 'voice_update_modlog_channel_id')),
                'converter_args': [("What channel do you want deleted message logs to go to?", "VC update archive", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'voice_update_modlog_channel_id'),
            },
            {
                'display': lambda c: "Guild update log channel (currently {0})".format(settings_mention(c, 'guild_update_channel_id')),
                'converter_args': [("Where do you want guild updates to go??", "Guild Update Channel", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'guild_update_channel_id'),
            },
            {
                'display': lambda c: "Roleplay Audit Log Channel (currently {0})".format(settings_mention(c, 'audit_channel')),
                'converter_args': [("What do you want to set the Audit Log channel to?", "Audit Log Channel", commands.TextChannelConverter)],
                'callback': utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'audit_channel'),
            },
        )
        try:
            # await menu.start(ctx)
            await ctx.send('Modlogs are currently being revamped.')
            await ctx.ack()
        except utils.errors.InvokedMetaCommand:
            pass
    
    @setup.command()
    @utils.checks.meta_command()
    async def georp(self, ctx:utils.Context):
        """Run the bot setup"""

        # Make sure it's only run as its own command, not a parent
        if ctx.invoked_subcommand is not None:
            return

        # Create settings menu
        menu = utils.SettingsMenu()
        settings_mention = utils.SettingsMenuOption.get_guild_settings_mention
        
        menu.add_multiple_options(
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'Set Worldnews channel (currently {0})'.format(settings_mention(x, 'worldnews_channel')),
                converter_args=(
                    utils.SettingsMenuConverter(
                        prompt='What do you want to set the Worldnews channel to?',
                        asking_for='Worldnews Channel',
                        converter=commands.TextChannelConverter,
                    ),
                ),
                callback=utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'worldnews_channel')
            ),
            
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'Set Spacenews channel (currently {0})'.format(settings_mention(x, 'spacenews_channel')),
                converter_args=(
                    utils.SettingsMenuConverter(
                        prompt='What do you want to set the Spacenews channel to?',
                        asking_for='Spacenews Channel',
                        converter=commands.TextChannelConverter,
                    ),
                ),
                callback=utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'spacenews_channel')
            ),
            
            utils.SettingsMenuOption(
                ctx=ctx,
                display=lambda x: 'Set News Role channel (currently {0})'.format(settings_mention(x, 'news_role')),
                converter_args=(
                    utils.SettingsMenuConverter(
                        prompt='What do you want to set News Role to?',
                        asking_for='News Role',
                        converter=commands.RoleConverter,
                    ),
                ),
                callback=utils.SettingsMenuOption.get_set_guild_settings_callback('guild_settings', 'news_role')
            ),
        )
        try:
            await menu.start(ctx)
        except utils.errors.InvokedMetaCommand:
            pass

def setup(bot:utils.Bot):
    x = BotSettings(bot)
    bot.add_cog(x)
