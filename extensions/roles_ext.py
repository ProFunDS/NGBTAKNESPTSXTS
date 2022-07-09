from asyncio import TimeoutError, sleep

from config.utils import language_roles

from hikari import (ComponentInteraction, ComponentType, Embed,
                    InteractionCreateEvent)
                    
from lightbulb import (Plugin, SlashCommand, SlashContext, add_checks, command,
                       guild_only, implements, option)


role_issuer = Plugin('Role System')

@role_issuer.command
@add_checks(guild_only)
@option('category', 'Choosing a role category',
        choices=['languages'])
@command('roles', 'Take or give a role', auto_defer=True)
@implements(SlashCommand)
async def raffle_axie_command(ctx: SlashContext):
    author_id = ctx.author.id
    guild = ctx.get_guild()
    member = guild.get_member(author_id)

    row = ctx.bot.rest.build_action_row()
    select_menu = row.add_select_menu('Role select')
    select_menu.set_placeholder('Choose a role')

    match ctx.options.category:
        case 'languages':
            roles = language_roles

    for label, pair in roles.items():
        option = select_menu.add_option(label, pair.id)
        option.set_emoji(pair.emoji)
        option.add_to_menu()
    
    select_menu.add_to_container()

    respond = await ctx.respond(component=row)
    message = await respond.message()
    
    try:
        event = await ctx.bot.wait_for(
            InteractionCreateEvent,
            60,
            lambda e: isinstance(inter := e.interaction, ComponentInteraction)
            and inter.user.id == author_id
            and inter.message.id == message.id
            and inter.component_type == ComponentType.SELECT_MENU
        )
    except TimeoutError:
        return await message.edit('The menu timed outs', components=[])
    else:
        role_id = int(event.interaction.values[0])
        role_mention = guild.get_role(role_id).mention
        if role_id in member.role_ids:
            await member.remove_role(role_id)
            await message.edit(Embed(description=f'You gave away the {role_mention} role'), components=[])
        else:
            await member.add_role(role_id)
            await message.edit(Embed(description=f'You took the {role_mention} role'), components=[])
            channel = ctx.get_channel()

def load(bot):
    bot.add_plugin(role_issuer)

def unload(bot):
    bot.remove_plugin(role_issuer)
