from datetime import datetime as dt

from config import WRITER_ROLE_ID
from config.utils import colors

from hikari import Embed, OptionType

from lightbulb import (Plugin, SlashCommand, SlashContext, add_checks, command,
                       implements, option)
from lightbulb.checks import has_roles


publisher = Plugin('Publisher System')

@publisher.command
@add_checks(has_roles(WRITER_ROLE_ID))
@option('text', 'Write a text with \\n (<2000 characters)')
@option('image_url', 'Picture url from Internet', required=False)
@option('set_timestamp', 'Should the timestamp be credited?', bool)
@option('set_author', 'Should the author be credited?', bool)
@option('color', 'Choose a color', choices=colors.keys())
@option('channel', 'Choose channel', OptionType.CHANNEL)
@command('write', 'Write post to any channel', auto_defer=True)
@implements(SlashCommand)
async def write_command(ctx: SlashContext):
    o = ctx.options
    guild = ctx.get_guild()
    channel = guild.get_channel(o.channel.id)
    author = guild.get_member(ctx.author.id)

    embed = Embed(
            description=o.text.replace('\\n', '\n').replace('/n', '\n'),
            color=colors[o.color])
    if o.set_author: # bottom embed
        embed.set_footer(
            text=author.display_name,
            icon=author.display_avatar_url)
    if o.set_timestamp:
        embed.timestamp = dt.now()
    embed.set_author(name=guild.name, icon=guild.icon_url)
    if o.image_url:
        await channel.send(o.image_url)

    await channel.send(embed=embed)

    await ctx.respond('Successfully `✅`')

def load(bot):
    bot.add_plugin(publisher)

def unload(bot):
    bot.remove_plugin(publisher)
