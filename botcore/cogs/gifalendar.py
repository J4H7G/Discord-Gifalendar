import os
import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
from datetime import timezone, timedelta
import secrets
from botcore import utils
from pathlib import Path
from botcore.embed import BasicEmbed
from config import config

dir_path = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()
default_images_path = '{}/resources/gc_'.format(dir_path)
class Gifalendar(commands.Cog):
    """ Annoy your friends every day! With a gif or something
    """
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self._tasks = []
        self.refresh_tasks.start()

    def cog_unload(self):
        self.init_tasks.cancel()
        self._tasks = [t.cancel() for t in self._tasks]
        self._tasks.clear()

######################################################

    @tasks.loop(seconds=config.TASK_REFRESH_RATE)
    async def refresh_tasks(self):
        self.cog_unload()
        await self.init_tasks.start()

    @refresh_tasks.before_loop
    async def refresh_tasks_before_loop(self):
        await self.bot.wait_until_ready()

    @tasks.loop(count=1)
    async def init_tasks(self):
        for guild in self.bot.guilds:
            GuildGCS = self.bot.gifalendar_settings[guild]
            tz = utils.get_timezone_name(hours=GuildGCS.get('gifalendar_timezone_offset'))
            loop_interval = utils.str_time_to_seconds(GuildGCS.get('gifalendar_loop_interval'))
            sendAt = GuildGCS.get('gifalendar_send_at')
            sendAt_hour, sendAt_minute, sendAt_second = 0, 0, 0
            if sendAt:
                sendAt_timestamp = utils.split_timestamp(sendAt)
                sendAt_hour = int(sendAt_timestamp[0]) or 0
                sendAt_minute = int(sendAt_timestamp[1]) or 0
                sendAt_second = int(sendAt_timestamp[2]) or 0
 
            await self.gifalendar_task_generator(guild=guild, interval=loop_interval, hour=sendAt_hour, minute=sendAt_minute, second=sendAt_second, timezone=tz)

    @init_tasks.before_loop
    async def init_tasks_before_loop(self):
        await self.bot.wait_until_ready()

######################################################

    async def gifalendar_task(self, guild):
        GuildGCS = self.bot.gifalendar_settings[guild]
        channel = self.bot.get_channel(GuildGCS.get('gifalendar_channel_id'))
        if not channel: return

        tz = timezone(timedelta(hours=GuildGCS.get('gifalendar_timezone_offset')))
        currentWeekday = utils.get_weekday(timezone=tz)
        MediaList = GuildGCS.get(currentWeekday)
        if not MediaList:
            Media = f'''{default_images_path}{currentWeekday}/{secrets.choice(os.listdir(f"{default_images_path}{currentWeekday}"))}'''
            await channel.send(file=discord.File(Media))
        else:
            Media = secrets.choice(GuildGCS.get(currentWeekday))
            await channel.send(Media)

    def gifalendar_before_task(self, hour:int=0, minute:int=0, second:int=0, timezone=None):
        async def wrapper():
            await self.bot.wait_until_ready()
            await asyncio.sleep(utils.gifalendar_seconds_until(hour, minute, second, timezone))
        return wrapper

    async def gifalendar_task_generator(self, guild=None, interval=86400, hour:int=0, minute:int=0, second:int=0, timezone=None):
        task = tasks.loop(seconds=interval)(self.gifalendar_task)
        task.before_loop(self.gifalendar_before_task(hour, minute, second, timezone))
        task.start(guild=guild)
        self._tasks.append(task)
        return task

######################################################

    async def _start_tasks_helper(self, ctx:commands.Context, send_message:bool=False):
        await self.init_tasks()
        if send_message: await ctx.send("Started tasks")

    # @commands.hybrid_command(name='starttasks')
    # @commands.is_owner()
    # async def _start_tasks(self, ctx:commands.Context):
    #     await self._start_tasks_helper(ctx=ctx, send_message=True)


    async def _stop_tasks_helper(self, ctx:commands.Context, send_message:bool=False):
        self.cog_unload()
        if send_message: await ctx.send(config.UI_GC_STOP_TASKS_SUCCESS)

    @commands.hybrid_command(
        name='gifalendarstoptasks',
        aliases=config.ALIAS_GC_STOP_TASKS,
        description=config.HELP_GC_STOP_TASKS_LONG,
        help=config.HELP_GC_STOP_TASKS_SHORT,
        hidden=True
    )
    @commands.is_owner()
    async def _gifalendar_stop_tasks(self, ctx:commands.Context):
        await self._stop_tasks_helper(ctx=ctx, send_message=True)


    async def _restart_tasks_helper(self, ctx:commands.Context, send_message:bool=False):
        await self._stop_tasks_helper(ctx)
        await self._start_tasks_helper(ctx)
        if send_message: await ctx.send(config.UI_GC_RESTART_TASKS_SUCCESS)


    @commands.hybrid_command(
        name='gifalendarrestarttasks',
        aliases=config.ALIAS_GC_RESTART_TASKS,
        description=config.HELP_GC_RESTART_TASKS_LONG,
        help=config.HELP_GC_RESTART_TASKS_SHORT,
        hidden=True
    )
    @commands.is_owner()
    async def _gifalendar_restart_tasks(self, ctx:commands.Context):
        await self._restart_tasks_helper(ctx)


    @commands.hybrid_command(
        name='gifalendarreloaddb',
        aliases=config.ALIAS_GC_RELOAD_DB,
        description=config.HELP_GC_RELOAD_DB_LONG,
        help=config.HELP_GC_RELOAD_DB_SHORT,
        hidden=True
    )
    @commands.is_owner()
    async def _gifalendar_reload_db(self, ctx:commands.Context):
        GuildGCS = self.bot.gifalendar_settings[ctx.guild]
        GuildGCS.reload()
        await ctx.send(config.UI_GC_RELOAD_DB_SUCCESS)


    @commands.hybrid_command(
        name='gifalendarinfo',
        aliases=config.ALIAS_GC_INFO,
        description=config.HELP_GC_INFO_LONG,
        help=config.HELP_GC_INFO_SHORT
    )
    @commands.is_owner()
    async def _gifalendar_detail(self, ctx:commands.Context):
        GuildGCS = self.bot.gifalendar_settings[ctx.guild]
        
        embed = await BasicEmbed(title=config.UI_GC_INFO_EMBED_TITLE.format(ctx.guild.name), skip_send=True)
        hours, minutes, seconds = utils.extract_time_from_string(time_str=GuildGCS.get("gifalendar_send_at"))
        embed.add_field(
            name=config.UI_GC_INFO_EMBED_SEND_AT_TITLE,
            value=config.UI_GC_INFO_EMBED_SEND_AT_DESC.format(GuildGCS.get("gifalendar_send_at")),
            inline=True
        )
        embed.add_field(
            name=config.UI_GC_INFO_EMBED_NEXT_MESSAGE_TITLE,
            value=config.UI_GC_INFO_EMBED_NEXT_MESSAGE_DESC.format(utils.format_time_seconds(
                utils.gifalendar_seconds_until(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds,
                    timezone=utils.get_timezone_name(hours=GuildGCS.get('gifalendar_timezone_offset'))
                )
            )),
            inline=True
        )

        return await ctx.send(embed=embed)


async def setup(bot:commands.Bot):
    await bot.add_cog(Gifalendar(bot))