import os
import json
import discord
from config import config
from botcore import utils

dir_path = os.path.dirname(os.path.realpath(__file__))

CmdConfigs = {
    "channel_id": "gifalendar_channel_id",
    "timezone_offset": "gifalendar_timezone_offset",
    "send_at": "gifalendar_send_at",
    "loop_interval": "gifalendar_loop_interval",
}

Weekdays = {
    "monday": "monday",
    "tuesday": "tuesday",
    "wednesday": "wednesday",
    "thursday": "thursday",
    "friday": "friday",
    "saturday": "saturday",
    "sunday": "sunday",
}

class GifalendarSettings():

    def __init__(self, guild):
        self.guild = guild
        self.json_data = None
        self.config = None
        self.path = '{}/generated/gifalendar_settings.json'.format(dir_path)

        self.settings_template = {
            "id": 0,
            CmdConfigs["channel_id"]: 0,
            CmdConfigs["timezone_offset"]: utils.get_timezone_offset(),
            CmdConfigs["send_at"]: "00:00:00",
            CmdConfigs["loop_interval"]: "24:00:00",

            Weekdays["monday"]: [],
            Weekdays["tuesday"]: [],
            Weekdays["wednesday"]: [],
            Weekdays["thursday"]: [],
            Weekdays["friday"]: [],
            Weekdays["saturday"]: [],
            Weekdays["sunday"]: [],
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
            "gifalendar_send_at": utils.refactor_time_seconds(self.get("gifalendar_send_at")),
            "gifalendar_loop_interval": utils.refactor_time_seconds(self.get("gifalendar_loop_interval"))
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
        
        self.updateDB(self.json_data)

    def get(self, setting):
        return self.config[setting]

    async def format(self):
        embed = discord.Embed(
            title=config.HELP_GIFALENDAR_SETTINGS_TITLE.format(self.guild.name), description=config.HELP_GIFALENDAR_SETTINGS_DESC, color=config.EMBED_COLOR)

        embed.set_thumbnail(url=self.guild.icon)
        embed.set_footer(text=config.HELP_GIFALENDAR_SETTINGS_USAGE)

        exclusion_keys = ['id']

        for key in self.config.keys():
            if key in exclusion_keys:
                continue

            if not self.config.get(key):

                embed.add_field(name=config.HELP_SETTINGS_IDX_TITLE.format(key), value=config.HELP_SETTINGS_IDX_DESC.format(config.UI_NOVALUE))
                continue
            
            embed.add_field(name=config.HELP_SETTINGS_IDX_TITLE.format(key), value=config.HELP_SETTINGS_IDX_DESC.format(self.config.get(key)))

        if embed.fields.__len__() % 3 != 0:
            embed.add_field(name="", value="")

        return embed

    async def process_setting(self, setting, value, ctx):

        switcher = {
            CmdConfigs['channel_id']: lambda: self.gifalendar_channel_id(setting, value, ctx),
            CmdConfigs['timezone_offset']: lambda: self.gifalendar_timezone_offset(setting, value, ctx),
            CmdConfigs['send_at']: lambda: self.gifalendar_send_at(setting, value, ctx),
            CmdConfigs['loop_interval']: lambda: self.gifalendar_loop_interval(setting, value, ctx),

            f'{Weekdays["monday"]}_add': lambda: self.gifalendar_monday_add(setting, value, ctx),
            f'{Weekdays["monday"]}_remove': lambda: self.gifalendar_monday_remove(setting, value, ctx),

            f'{Weekdays["tuesday"]}_add': lambda: self.gifalendar_tuesday_add(setting, value, ctx),
            f'{Weekdays["tuesday"]}_remove': lambda: self.gifalendar_tuesday_remove(setting, value, ctx),

            f'{Weekdays["wednesday"]}_add': lambda: self.gifalendar_wednesday_add(setting, value, ctx),
            f'{Weekdays["wednesday"]}_remove': lambda: self.gifalendar_wednesday_remove(setting, value, ctx),

            f'{Weekdays["thursday"]}_add': lambda: self.gifalendar_thursday_add(setting, value, ctx),
            f'{Weekdays["thursday"]}_remove': lambda: self.gifalendar_thursday_remove(setting, value, ctx),

            f'{Weekdays["friday"]}_add': lambda: self.gifalendar_friday_add(setting, value, ctx),
            f'{Weekdays["friday"]}_remove': lambda: self.gifalendar_friday_remove(setting, value, ctx),

            f'{Weekdays["saturday"]}_add': lambda: self.gifalendar_saturday_add(setting, value, ctx),
            f'{Weekdays["saturday"]}_remove': lambda: self.gifalendar_saturday_remove(setting, value, ctx),

            f'{Weekdays["sunday"]}_add': lambda: self.gifalendar_sunday_add(setting, value, ctx),
            f'{Weekdays["sunday"]}_remove': lambda: self.gifalendar_sunday_remove(setting, value, ctx),
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

    ############ Setting methods ###########

    async def gifalendar_channel_id(self, setting, value, ctx):

        if value.lower() in ("unset", "none", "false", 0):
            self.config[setting] = None
            return

        found = False
        for chan in self.guild.text_channels:
            if chan.id == int(value):
                self.config[setting] = chan.id
                found = True
        if found == False:
            await ctx.send(config.ERROR_CHANNEL_ID_NOTFOUND.format(value))
            return False

    async def gifalendar_timezone_offset(self, setting, value, ctx):
        try:
            value = int(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

        self.config[setting] = value

    async def gifalendar_send_at(self, setting, value, ctx):
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False
        value = utils.refactor_time_seconds(value)

        self.config[setting] = value

    async def gifalendar_loop_interval(self, setting, value, ctx):
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

        value = utils.refactor_time_seconds(value)
        self.config[setting] = value

####################################

    async def gifalendar_monday_add(self, setting, value, ctx) -> bool:
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False
        
        gc = self.config[Weekdays["monday"]]
        gc = gc.append(value)
        return True

    async def gifalendar_monday_remove(self, setting, value, ctx) -> bool:
        try:
            value = int(value)
        except:
            await ctx.send(config.ERROR_WRONG_DATA_TYPE)
            return False
        
        try:
            gc = self.config[Weekdays["monday"]]
            gc = gc.pop(value)
            return True
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

####################################

    async def gifalendar_tuesday_add(self, setting, value, ctx) -> bool:
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False
        
        gc = self.config[Weekdays["tuesday"]]
        gc = gc.append(value)
        return True

    async def gifalendar_tuesday_remove(self, setting, value, ctx) -> bool:
        try:
            value = int(value)
        except:
            await ctx.send(config.ERROR_WRONG_DATA_TYPE)
            return False
        
        try:
            gc = self.config[Weekdays["tuesday"]]
            gc = gc.pop(value)
            return True
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

####################################

    async def gifalendar_wednesday_add(self, setting, value, ctx) -> bool:
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False
        
        gc = self.config[Weekdays["wednesday"]]
        gc = gc.append(value)
        return True

    async def gifalendar_wednesday_remove(self, setting, value, ctx) -> bool:
        try:
            value = int(value)
        except:
            await ctx.send(config.ERROR_WRONG_DATA_TYPE)
            return False
        
        try:
            gc = self.config[Weekdays["wednesday"]]
            gc = gc.pop(value)
            return True
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

####################################

    async def gifalendar_thursday_add(self, setting, value, ctx) -> bool:
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False
        
        gc = self.config[Weekdays["thursday"]]
        gc = gc.append(value)
        return True

    async def gifalendar_thursday_remove(self, setting, value, ctx) -> bool:
        try:
            value = int(value)
        except:
            await ctx.send(config.ERROR_WRONG_DATA_TYPE)
            return False
        
        try:
            gc = self.config[Weekdays["thursday"]]
            gc = gc.pop(value)
            return True
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

####################################

    async def gifalendar_friday_add(self, setting, value, ctx) -> bool:
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False
        
        gc = self.config[Weekdays["friday"]]
        gc = gc.append(value)
        return True

    async def gifalendar_friday_remove(self, setting, value, ctx) -> bool:
        try:
            value = int(value)
        except:
            await ctx.send(config.ERROR_WRONG_DATA_TYPE)
            return False
        
        try:
            gc = self.config[Weekdays["friday"]]
            gc = gc.pop(value)
            return True
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

####################################

    async def gifalendar_saturday_add(self, setting, value, ctx) -> bool:
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False
        
        gc = self.config[Weekdays["saturday"]]
        gc = gc.append(value)
        return True

    async def gifalendar_saturday_remove(self, setting, value, ctx) -> bool:
        try:
            value = int(value)
        except:
            await ctx.send(config.ERROR_WRONG_DATA_TYPE)
            return False
        
        try:
            gc = self.config[Weekdays["saturday"]]
            gc = gc.pop(value)
            return True
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

####################################

    async def gifalendar_sunday_add(self, setting, value, ctx) -> bool:
        try:
            value = str(value)
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False
        
        gc = self.config[Weekdays["sunday"]]
        gc = gc.append(value)
        return True

    async def gifalendar_sunday_remove(self, setting, value, ctx) -> bool:
        try:
            value = int(value)
        except:
            await ctx.send(config.ERROR_WRONG_DATA_TYPE)
            return False
        
        try:
            gc = self.config[Weekdays["sunday"]]
            gc = gc.pop(value)
            return True
        except:
            await ctx.send(config.ERROR_UNEXPECTED_MESSAGE)
            return False

####################################
