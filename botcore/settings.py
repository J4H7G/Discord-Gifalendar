import os
import json
import discord
from config import config

dir_path = os.path.dirname(os.path.realpath(__file__))

"""
HOW TO ADD SETTINGS VARS:
    1. add var dict@self.settings_template
    2. add def under "########### Setting methods ###########" apply settings by using | self.config[setting] = value
    3. add def under dict@switcher
"""


class Settings():

    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        self.json_data = None
        self.config = None
        self.path = '{}/generated/settings.json'.format(dir_path)

        self.settings_template = {
            "id": 0,
            "guild_name": "",
            "bot_prefix": "!",
        }

        self.reload()
        self.upgrade()

    async def write(self, setting, value, ctx):
        response = await self.process_setting(setting, value, ctx)

        with open(self.path, 'w') as source:
            json.dump(self.json_data, source, indent=4)
        self.reload()
        return response

    def updateDB(self, config):
        with open(self.path, 'w') as source:
            json.dump(config, source, indent=4)
        self.reload()

    def reload(self):
        source = open(self.path, 'r')
        self.json_data = json.load(source)

        target = None

        for server in self.json_data:
            server = self.json_data[server]

            if server['id'] == self.guild.id:
                target = server

        if target is None:
            self.create()
            return

        self.config = target

    def upgrade(self, force_refresh:bool=False):
        refresh = force_refresh and force_refresh or False
        # Update on startup
        dynamic_update = {
            'guild_name': self.guild.name,
        }
        for key in self.settings_template.keys():
            if not key in self.config:
                self.config[key] = self.settings_template.get(key)
                refresh = True
                
            for dyn in dynamic_update.keys():
                if not dyn in self.config or key != dynamic_update.get(dyn):
                    self.config[dyn] = dynamic_update.get(dyn)
                    refresh = True

        if refresh:
            self.updateDB(self.json_data)
            self.reload()

    def create(self):

        self.json_data[self.guild.id] = self.settings_template
        self.json_data[self.guild.id]['id'] = self.guild.id
        self.json_data[self.guild.id]['guild_name'] = self.guild.name
        
        self.updateDB(self.json_data)

    def get(self, setting):
        return self.config[setting]

    async def format(self):
        embed = discord.Embed(
            title=config.HELP_SETTINGS_TITLE.format(self.guild.name), description=config.HELP_SETTINGS_DESC, color=config.EMBED_COLOR)

        embed.set_thumbnail(url=self.guild.icon)
        embed.set_footer(text=config.HELP_SETTINGS_USAGE)

        exclusion_keys = ['id', 'guild_name']

        for key in self.config.keys():
            if key in exclusion_keys:
                continue

            if self.config.get(key) == "" or self.config.get(key) is None:

                embed.add_field(name=config.HELP_SETTINGS_IDX_TITLE.format(key), value=config.HELP_SETTINGS_IDX_DESC.format(config.UI_NOVALUE))
                continue
            
            embed.add_field(name=config.HELP_SETTINGS_IDX_TITLE.format(key), value=config.HELP_SETTINGS_IDX_DESC.format(self.config.get(key)))

        return embed

    async def process_setting(self, setting, value, ctx):

        switcher = {
            'bot_prefix': lambda: self.bot_prefix(setting, value, ctx),
        }
        get_setting = switcher.get(setting)

        if get_setting is None:
            return None
        else:
            cb = await get_setting()
            if cb is None:
                return True
            else:
                return cb

    # ########### Setting methods ###########

    async def bot_prefix(self, setting, value, ctx):
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

        self.config[setting] = value
