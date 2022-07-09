#!python3.10.2
from os import name

from hikari import Activity, ActivityType, Status

from config import __version__
from discord import bot
    
if __name__ == '__main__':
    bot.load_extensions_from('extensions')
    if name != 'nt':
        import uvloop
        uvloop.install()

    bot.run(activity=Activity(name=f'V.{__version__}',
            type=ActivityType.WATCHING),
            status=Status.DO_NOT_DISTURB)
