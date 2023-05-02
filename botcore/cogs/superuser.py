
from typing import Optional

import discord
from config import config
from discord import app_commands
from discord.ext import commands
from botcore import utils

class Superuser(commands.Cog, command_attrs=dict(hidden=True)):
    """\📛 Admin Commands
    """
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Do admin stuff on startup."""
        pass

    @commands.command(
        name="echo",
        aliases=config.ALIAS_ECHO,
        description=config.HELP_ECHO_LONG,
        help=config.HELP_ECHO_SHORT
    )
    @commands.is_owner()
    async def _echo(self, ctx:commands.Context, channel: discord.TextChannel, *, message: Optional[str]):
        """Make the bot say stuff."""
        channel = channel is not None and channel or ctx
        await channel.send(message)
        await ctx.send(f"\n Said in {channel}: {message}")

    @commands.command(
        name="leaveguild",
        aliases=config.ALIAS_LEAVE_GUILD,
        description=config.HELP_LEAVE_GUILD_LONG,
        help=config.HELP_LEAVE_GUILD_SHORT
    )
    @commands.is_owner()
    async def _leaveserver(self, ctx:commands.Context, *, server: str = None):
        try:
            server = int(server)
        except ValueError:
            pass
        else:
            utils.dprint(config.UI_LEAVE_GUILD_SUCCESS_FMT.format(self.bot.get_guild(int(server)), server))
            await ctx.send(config.UI_LEAVE_GUILD_SUCCESS_FMT.format(self.bot.get_guild(int(server)), server))
            await self.bot.get_guild(int(server)).leave()
            return

        guild = discord.utils.get(self.bot.guilds, name=server) # Get the guild by name
        if guild is None:
            utils.dprint(config.UI_LEAVE_GUILD_FAILED_FMT.format(server))
            await ctx.send(config.UI_LEAVE_GUILD_FAILED_FMT.format(server))
            return
        utils.dprint(config.UI_LEAVE_GUILD_SUCCESS_FMT.format(f"{guild.name} | Id: {guild.id}"))
        await ctx.send(config.UI_LEAVE_GUILD_SUCCESS_FMT.format(f"{guild.name} | Id: {guild.id}"))
        await guild.leave() # Guild found


    @commands.command(
        name="reloadcog",
        aliases=config.ALIAS_RELOAD_COG,
        description=config.HELP_RELOAD_COG_LONG,
        help=config.HELP_RELOAD_COG_SHORT
    )
    @commands.is_owner()
    async def _reload_cog(self, ctx: commands.Context, *, cog_str: str = None):
        cog = [cog_str]
        try:
            if cog is not None:
                await utils.cogs_manager(self.bot, "reload", cogs=cog)
                await ctx.send(config.UI_RELOAD_COG_SUCCESS_FMT.format(cog_str))
        except Exception as e:
            return await ctx.send(config.UI_RELOAD_COG_FAILED_FMT.format(cog_str, e))


    @commands.command(
        name="shutdown",
        aliases=config.ALIAS_SHUTDOWN,
        description=config.HELP_SHUTDOWN_LONG,
        help=config.HELP_SHUTDOWN_SHORT
    )
    @commands.is_owner()
    async def _master_shutdown(self, ctx: commands.Context):
        utils.dprint(config.UI_SHUTDOWN_FMT)
        await ctx.send(config.UI_SHUTDOWN_FMT)
        await self.bot.Mastershutdown()


async def setup(bot:commands.Bot):
    await bot.add_cog(Superuser(bot))
