from config import DEV_CHANNEL_ID

from hikari import Embed

from lightbulb import Plugin
from lightbulb.errors import (CommandInvocationError, CommandIsOnCooldown,
                              ExtensionAlreadyLoaded, ExtensionMissingLoad,
                              ExtensionMissingUnload, ExtensionNotFound,
                              ExtensionNotLoaded, NotOwner, OnlyInGuild,
                              MissingRequiredRole)
from lightbulb.events import CommandErrorEvent, SlashCommandErrorEvent


errors = Plugin('ErrorHandler System')

@errors.listener(CommandErrorEvent)
async def on_error(event: CommandErrorEvent) -> None:
    r = event.context.respond
    if isinstance(event.exception, CommandInvocationError):
        await r(f'`❌` Something went wrong during invocation of command `{event.context.command.name}`.')
        channel = event.context.get_channel()
        dev_channel = await event.app.rest.fetch_channel(DEV_CHANNEL_ID)
        embed = Embed(title='Error', description=f'`{event.exception.__cause__}`',
                    color='FF0000')
        embed.add_field('Channel', channel.mention)
        await dev_channel.send(embed=embed)
        return

    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, NotOwner):
        await r('`❌` This command is only available to owners.')
    elif isinstance(exception, MissingRequiredRole):
        await r(f'`❌` You do not have the required role.')
    elif isinstance(exception, OnlyInGuild):
        await r('`❌` This сommand is only available in the guild.')
    # elif isinstance(exception, CommandIsOnCooldown):
        # await r(f'`❌` This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.')
    elif isinstance(exception, ExtensionAlreadyLoaded):
        await r('`❌` Extension already loaded.')
    elif isinstance(exception, ExtensionMissingLoad):
        await r('`❌` The extension does not contain a load function.')
    elif isinstance(exception, ExtensionMissingUnload):
        await r('`❌` The extension does not contain a unload function.')
    elif isinstance(exception, ExtensionNotFound):
        await r('`❌` Extension not found.')
    elif isinstance(exception, ExtensionNotLoaded):
        await r('`❌` Extension not loaded.')
    else:
        await r('`❌` An unexpected error has occurred! Contact the administration.')

@errors.listener(SlashCommandErrorEvent)
async def on_slash_command_error(event: SlashCommandErrorEvent) -> None:
    channel = event.context.get_channel()
    name = event.context.command.name
    await channel.send(
        f'`❌` Something went wrong during invocation of command `{name}`.')
    
def load(bot):
    bot.add_plugin(errors)

def unload(bot):
    bot.remove_plugin(errors)