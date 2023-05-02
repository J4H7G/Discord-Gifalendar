
import os
from time import time


import discord
from discord.ext import commands

from config import config
from botcore import utils
from botcore.settings import Settings
from botcore.gifalendar_settings import GifalendarSettings

init_cogs = [
    f"botcore.cogs.{filename[:-3]}" for filename in os.listdir("botcore/cogs") if filename.endswith(".py")
    # 'botcore.cogs.general',
    # 'botcore.cogs.gifalendar',
    # 'botcore.cogs.superuser',
]
utils.dprint(f"Loaded {len(init_cogs)} cogs:", " | ".join([cog for cog in init_cogs]))

def init_bot_intents():
    bot_intents = discord.Intents.default()
    bot_intents.message_content = True
    return bot_intents

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=self.__get_prefix,
            # help_command=None,
            case_insensitive=True,
            intents=init_bot_intents(),
        )

    def __add_attribute(self, attr: str, attr_value: any):
        try:
            setattr(self, attr, attr_value)
            utils.dprint(f"[Startup] Inititalized <{attr}>")
        except:
            utils.dprint(f"[Startup] Failed to inititalize <{attr}>")

    async def init_botvars(self):
        self.__add_attribute(attr="up_time", attr_value=time())

    def __get_prefix(self, bot, message):
        guild_bot_prefix = self.guild_settings[message.guild].get('bot_prefix')
        if guild_bot_prefix != config.BOT_PREFIX:
            prefix = guild_bot_prefix
        else:
            prefix = config.BOT_PREFIX
        return commands.when_mentioned_or(prefix)(bot, message)


    async def register(self, guild):
        self.guild_settings[guild] = Settings(bot, guild)
        self.gifalendar_settings[guild] = GifalendarSettings(guild)
        return


    async def on_ready(self):
        utils.dprint(config.STARTUP_MESSAGE)
        await self.change_presence(status=discord.Status[config.BOT_STATUS], activity=discord.Activity(type=discord.ActivityType[config.BOT_ACTIVITY], name=config.BOT_FLAIR))

        for guild in self.guilds:
            await self.register(guild)
            utils.dprint("Joined {} | ID: {} | Prefix: {}".format(guild.name,guild.id,self.guild_settings[guild].get('bot_prefix')))

        await self.init_botvars()

        utils.dprint(config.STARTUP_COMPLETE_MESSAGE)


    async def setup_hook(self):
        """Initialize the db, prefixes & cogs."""
        try:
            await utils.cogs_manager(self, "load", init_cogs)
        except Exception as e:
            print(e)

        self.guild_settings = dict()
        self.gifalendar_settings = dict()

        self.loop.create_task(self.startup())


    async def on_guild_join(self, guild):
        await self.register(guild)
        await self.tree.sync()
        print("Joined New Group! {} | {}".format(guild.name,guild.id))

    async def on_guild_remove(self, guild):
        print("Left Group! {} | {}".format(guild.name,guild.id))


    async def on_message(self, message):
        if await self.is_owner(message.author):
            return await self.process_commands(message)

        if message.author.id == self.user.id:
            return

        await self.process_commands(message)


    async def startup(self):
        """Sync application commands"""
        await self.wait_until_ready()
        await self.tree.sync()


    async def Mastershutdown(self):
        await super().close()

if __name__ == '__main__':

    if config.BOT_TOKEN == "":
        utils.dprint("Error: No bot token!")
        exit(0)

    bot = Bot()
    bot.run(config.BOT_TOKEN, reconnect=True)
