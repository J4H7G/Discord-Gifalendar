import os
from dotenv import load_dotenv
load_dotenv()
def get_env(key, default=None):
    return os.getenv(key, default)
# online | offline | idle | dnd | invisible
VALID_STATUS = ["online", "offline", "idle", "dnd", "invisible"]
# unknown | playing | streaming | listening | watching | custom | competing
VALID_ACTIVITY = ["unknown", "playing", "streaming", "listening", "watching", "custom", "competing"]

BOT_TOKEN:      str = get_env("BOT_TOKEN")
BOT_VERSION:    str = get_env("BOT_VERSION", "0.0.0")
BOT_STATUS:     str  = get_env("BOT_STATUS", "online").lower() if get_env("BOT_STATUS").lower() in VALID_STATUS else "online"
BOT_ACTIVITY:   str  = get_env("BOT_ACTIVITY", "watching").lower() if get_env("BOT_ACTIVITY").lower() in VALID_ACTIVITY else "unknown"
BOT_FLAIR:      str  = get_env("BOT_FLAIR", "screaming rats")