from config import GUILD_MEMBER_ROLE_ID, WELCOME_CHANNEL_ID, __version__
from config.rating_settings import EFL, EPIM, IMR, LR, LR_IMR

from hikari import Embed

from lightbulb import Plugin, SlashCommand, SlashContext, command, implements


helper = Plugin('Help System')

TEXT = f'''**About the guild**:

Have you read the <#{WELCOME_CHANNEL_ID}> channel yet?
...and <#123456789987654321>?
...and <#123456789987654321>?


**About the guild member role**:

In order to obtain the <@&{GUILD_MEMBER_ROLE_ID}> role you must: 
```py
1. have an Axie Infinity account```
..or...
```py
2. reach activity level {LR} here by communicating in different channels and threads```
..or...
```py
3. invite {IMR} new members here and gain activity level {LR_IMR}.```
If an invitee places you as their invitee with `/specify_my_referrer`, they will receive **{EFL}** activity experience and you will receive **{EPIM}** activity experience.

If you have an Axie Infinity account, you need to send the address of your account to the administrator in a private message.
If you fulfill 2 or 3 of these points, the role of guild member will be given to you automatically. You can track your progress with the command `/show_statistics`.
If you surrender your account, but remain in the role of guild member, when you receive rewards from the project, the conditions of fulfilling 2 or 3 points will be considered.


**About the bot**:

*Only slash-command bot.
Current version: {__version__}*
'''

@helper.command
@command('help', 'Get information about the guild and NAME-Bot')
@implements(SlashCommand)
async def help_command(ctx: SlashContext):
    await ctx.respond(embed=Embed(description=TEXT))

def load(bot):
    bot.add_plugin(helper)

def unload(bot):
    bot.remove_plugin(helper)
