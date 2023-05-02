from .credentials import *

BOT_PREFIX = "%"

###############################################################################
TASK_REFRESH_RATE = 30 # seconds or None to disable automatic refresh

#42eb1c -- Green
#f3cA28 -- Gold
#C51CEB -- Purple
#1CA9EB -- L Blue
#EB5E1C -- Orange
#FA1E4E -- Pinkish Red
EMBED_COLOR = int("FA1E4E", 16)
STARTUP_MESSAGE = "[Startup] Starting Bot..."
STARTUP_COMPLETE_MESSAGE = "[Startup] Startup Complete!"


## UI stuff
UI_EMBED_TIMEOUT_DESC = "This message will be deleted after {}."
UI_NOVALUE = "None"
UI_SAVED_CHANGES = "\✅ Changes committed!"
UI_CANCELED_CHANGES = "\❌ Canceled Changes"

ERROR_CHANNEL_ID_NOTFOUND = "Couldn't find channel"
ERROR_UNEXPECTED_MESSAGE = "Something Went Wrong!"
ERROR_WRONG_DATA_TYPE = "Wrong Data Type!"
ERROR_UNEXPECTED_QUOTE = "Put a [\\] before a quote[\"]"
ERROR_MISSING_PERMISSION = "You are not worthy"

HELP_COMMAND_COG_SPACING = 3
HELP_COMMAND_COLOR_NOCOG = int("55ff9e", 16)
HELP_COMMAND_COLOR_PASS = int("42eb1c", 16)
HELP_COMMAND_COLOR_WARNING = int("f57800", 16)
HELP_COMMAND_COLOR_ERROR = int("ff1100", 16)
##


# General
ALIAS_SETTING = ["settings", "sett"]
ALIAS_GIFALENDAR_SETTING = ["gifalendarsettings", "gcs"]
ALIAS_UPTIME = ["ut"]
ALIAS_PREFIX = []
#
HELP_SETTINGS_SHORT = "Configure the bot."
HELP_SETTINGS_LONG = "View and configure the bot's inner clockwork (You have to be an Administrator or higher to access this)."
HELP_SETTINGS_TITLE = "Bot Setting for {}"
HELP_SETTINGS_DESC = "`Configure general settings!`"
HELP_SETTINGS_IDX_TITLE = "{}:"
HELP_SETTINGS_IDX_DESC = "`{}`"
HELP_SETTINGS_USAGE = "Usage: %ssettings <setting> <value>" % BOT_PREFIX

HELP_GIFALENDAR_SETTINGS_SHORT = "Configure Gifalendar."
HELP_GIFALENDAR_SETTINGS_LONG = "Configure Gifalendar."
HELP_GIFALENDAR_SETTINGS_TITLE = "Gifalendar Setting for {}"
HELP_GIFALENDAR_SETTINGS_DESC = "`Configure how I should annoy your friends!`"
HELP_GIFALENDAR_SETTINGS_USAGE = "Usage: %sgifalendar <setting> <value> (This can take up to %s seconds to register)" % (BOT_PREFIX, TASK_REFRESH_RATE)

UI_UPTIME_FMT = "I've been alive for: `{}`"
HELP_UPTIME_SHORT = "View bot uptime"
HELP_UPTIME_LONG = "View bot uptime"

UI_PREFIX_FMT = "My prefix here is: `{}`"
HELP_PREFIX_SHORT = "View bot prefix in this server"
HELP_PREFIX_LONG = "View bot prefix in this server"


# Superuser
ALIAS_ECHO = ["say"]
#
HELP_ECHO_LONG = "Make the bot say stuff"
HELP_ECHO_SHORT = "Make the bot say stuff"

ALIAS_LEAVE_GUILD = ["leaveserver"]
UI_LEAVE_GUILD_SUCCESS_FMT = "Left Server: {} | Id: {}"
UI_LEAVE_GUILD_FAILED_FMT = "Couldn't leave server: {} | >Couldn't find server or server doesn't exist"
HELP_LEAVE_GUILD_LONG = "Leave specified server"
HELP_LEAVE_GUILD_SHORT = "Leave specified server"

ALIAS_RELOAD_COG = ["rc"]
UI_RELOAD_COG_SUCCESS_FMT = "Reloaded Cog: {}"
UI_RELOAD_COG_FAILED_FMT = "Couldn't Reload Cog: {} {}"
HELP_RELOAD_COG_LONG = "Reload Cog"
HELP_RELOAD_COG_SHORT = "Reload Cog"

ALIAS_SHUTDOWN = []
UI_SHUTDOWN_FMT = "Shutting down..."
HELP_SHUTDOWN_LONG = "Shutdown the bot"
HELP_SHUTDOWN_SHORT = "Shutdown the bot"

# Gifalendar
ALIAS_GC_STOP_TASKS = ["gcst"]
UI_GC_STOP_TASKS_SUCCESS = "Stopping all tasks..."
HELP_GC_STOP_TASKS_LONG = "Stop all running tasks"
HELP_GC_STOP_TASKS_SHORT = "Stop all running tasks"

ALIAS_GC_RESTART_TASKS = ["gcrst"]
UI_GC_RESTART_TASKS_SUCCESS = "Restarting tasks..."
HELP_GC_RESTART_TASKS_LONG = "Restart tasks"
HELP_GC_RESTART_TASKS_SHORT = "Restart tasks"

ALIAS_GC_RELOAD_DB = ["gcrldb"]
UI_GC_RELOAD_DB_SUCCESS = "Reloading db..."
HELP_GC_RELOAD_DB_LONG = "Reload db"
HELP_GC_RELOAD_DB_SHORT = "Reload db"

ALIAS_GC_INFO = ["gci"]
UI_GC_INFO_EMBED_TITLE = "GIFalendar Info for {}"
UI_GC_INFO_EMBED_SEND_AT_TITLE = "`Send Message At:`"
UI_GC_INFO_EMBED_SEND_AT_DESC = "**{}**"
UI_GC_INFO_EMBED_NEXT_MESSAGE_TITLE = "`Time before next message:`"
UI_GC_INFO_EMBED_NEXT_MESSAGE_DESC = "**{}**"
HELP_GC_INFO_LONG = "View some information about the server's GIFalendar"
HELP_GC_INFO_SHORT = "View some information about the server's GIFalendar"