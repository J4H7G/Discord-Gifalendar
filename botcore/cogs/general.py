
from time import time
from config import config
from discord.ext import commands
from botcore import utils

class General(commands.Cog):
    """ General commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name='uptime',
        aliases=config.ALIAS_UPTIME,
        description=config.HELP_UPTIME_LONG,
        help=config.HELP_UPTIME_SHORT
    )
    async def _uptime(self, ctx:commands.Context):
        await ctx.send(config.UI_UPTIME_FMT.format(utils.get_uptime(self.bot,format=True,current_time=time())))

    @commands.hybrid_command(
        name='prefix',
        aliases=config.ALIAS_PREFIX,
        description=config.HELP_PREFIX_LONG,
        help=config.HELP_PREFIX_SHORT
    )
    async def _prefix(self, ctx:commands.Context):
        await ctx.send(config.UI_PREFIX_FMT.format(self.bot.guild_settings[ctx.guild].get('bot_prefix')))

    @commands.command(
        name="setting",
        aliases=config.ALIAS_SETTING,
        description=config.HELP_SETTINGS_LONG,
        help=config.HELP_SETTINGS_SHORT
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def _settings(self, ctx:commands.Context, *args):
        sett = self.bot.guild_settings[ctx.guild]

        if len(args) == 0:
            await ctx.send(embed=await sett.format())
            return

        args_list = list(args)
        args_list.remove(args[0])

        response = await sett.write(args[0], " ".join(args_list), ctx)

        if response:
            await ctx.send(config.UI_SAVED_CHANGES)
        else:
            await ctx.send(config.UI_CANCELED_CHANGES)
    
    @_settings.error
    async def _settings_error(self, ctx:commands.Context, error):
        if isinstance(error, commands.UnexpectedQuoteError):
            return await ctx.send(config.ERROR_UNEXPECTED_QUOTE)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(config.ERROR_MISSING_PERMISSION)


    @commands.command(
        name="gifalendarsetting",
        aliases=config.ALIAS_GIFALENDAR_SETTING,
        description=config.HELP_GIFALENDAR_SETTINGS_LONG,
        help=config.HELP_GIFALENDAR_SETTINGS_SHORT
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def _gifalendarsettings(self, ctx:commands.Context, *args):
        guildsetting = self.bot.gifalendar_settings[ctx.guild]

        if len(args) == 0:
            await ctx.send(embed = await guildsetting.format())
            return

        args_list = list(args)
        args_list.remove(args[0])

        response = await guildsetting.write(args[0], " ".join(args_list), ctx)

        if response:
            await ctx.send(config.UI_SAVED_CHANGES)
        else:
            await ctx.send(config.UI_CANCELED_CHANGES)
    
    @_gifalendarsettings.error
    async def _gifalendarsettings_error(self, ctx:commands.Context, error):
        if isinstance(error, commands.UnexpectedQuoteError):
            return await ctx.send(config.ERROR_UNEXPECTED_QUOTE)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(config.ERROR_MISSING_PERMISSION)


async def setup(bot:commands.Bot):
    await bot.add_cog(General(bot))