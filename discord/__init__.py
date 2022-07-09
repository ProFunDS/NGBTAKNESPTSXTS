from config import GUILD_ID, OWNERS_ID
from config.tokens import TOKEN

from hikari import Intents

from lightbulb import BotApp


bot = BotApp(TOKEN, ignore_bots=True,
         default_enabled_guilds=(GUILD_ID,),
         owner_ids=OWNERS_ID,
         logs='ERROR',
         banner=None,
         intents=Intents.ALL)
