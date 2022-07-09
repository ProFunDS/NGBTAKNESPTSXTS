from datetime import datetime

from mongo import users
from mongo.utils import DuplicateKeyError, create_pack, delete_entry

from discord import bot

from hikari import CommandChoice, Member

from lightbulb import (Plugin, SlashCommandGroup, SlashContext,
                       SlashSubCommand, add_checks, command, implements,
                       option)
from lightbulb.checks import owner_only


moderation = Plugin('Moderation System')


@moderation.command
@add_checks(owner_only)
@command('moderation', '[Only for admins]')
@implements(SlashCommandGroup)
async def moder(ctx: SlashContext):
    await ctx.respond(f'Choose subcommand: {moder.subcommands}')

@moder.child
@add_checks(owner_only)
@option('id', 'Insert the ID')
@command('get_date', 'Get date by id')
@implements(SlashSubCommand)
async def get_date_by_id(ctx: SlashContext):
    _id = int(ctx.options.id)
    date = datetime.fromtimestamp((_id/4194304+1420070400000)/1000)  # magic
    text = date.strftime('Дата: %d.%m.%Y\nВремя: %H:%M:%S (МСК)')
    await ctx.respond(text)

@moder.child
@add_checks(owner_only)
@option('extension', 'Module to be reloaded',
    choices=bot.extensions)
@command('reload_extension', 'Reload module')
@implements(SlashSubCommand)
async def reload_command(ctx: SlashContext):
    ctx.bot.reload_extensions(ctx.options.extension)
    await ctx.respond('Successfully `✅`')

@moder.child
@add_checks(owner_only)
@option('extension', 'Module to be loaded | Example: module_ext')
@command('load_extension', 'Load module')
@implements(SlashSubCommand)
async def load_command(ctx: SlashContext):
    ctx.bot.load_extensions(f'extensions.{ctx.options.extension}')
    await ctx.respond('Successfully `✅`')

@moder.child
@add_checks(owner_only)
@option('extension', 'Module to be unloaded',
    choices=bot.extensions)
@command('unload_extension', 'Unload module')
@implements(SlashSubCommand)
async def unload_command(ctx: SlashContext):
    ctx.bot.unload_extensions(ctx.options.extension)
    await ctx.respond('Successfully `✅`')

@moder.child
@add_checks(owner_only)
@option('amount', 'Amount of points to add or remove from a member', int)
@option('choice', 'Experience or score of invited members',
    choices=[
        CommandChoice(name='Experience', value='exp'),
        CommandChoice(name='Score of invited members', value='im')
    ])
@option('member', 'Member whose stats will be updated', Member)
@command('update_member_stats', 'Update member statistics')
@implements(SlashSubCommand)
async def update_entry_command(ctx: SlashContext):
    opts = ctx.options
    m = opts.member

    if m.is_bot:
        return await ctx.respond("It'a bot! `❌`")
        
    user = await users.find_one({'_id': m.id})

    if user is None:
        await users.insert_one(user := create_pack(m.id))

    await users.update_one({'_id': m.id},
        {'$set': {opts.choice: user[opts.choice]+opts.amount}})
    await ctx.respond('Successfully `✅`')
    
@moder.child
@add_checks(owner_only)
@option('member',
    'The member for whom the record will be created in the database',
    Member)
@command('add_member_to_db',
    'Create an entry in the database for the member')
@implements(SlashSubCommand)
async def create_entry_command(ctx: SlashContext):
    if ctx.options.member.is_bot:
        return await ctx.respond("It'a bot! `❌`")
    try:
        await users.insert_one(create_pack(ctx.options.member.id))
        await ctx.respond('Successfully `✅`')
    except DuplicateKeyError:
        await ctx.respond('The member is already in the database! `❌`')

@moder.child
@add_checks(owner_only)
@option('member',
    'The member whose record is being removed from the database',
    Member)
@command('remove_member_from_db',
    'Delete member entry from database')
@implements(SlashSubCommand)
async def delete_entry_command(ctx: SlashContext):
    await delete_entry(ctx.options.member.id)
    await ctx.respond('Successfully `✅`')

@moder.child
@add_checks(owner_only)
@option('check', 'A you seriously?', bool)
@command('turn_off_the_bot', 'Turn off the bot')
@implements(SlashSubCommand)
async def turn_off_command(ctx: SlashContext):
    if ctx.options.check:
        await ctx.respond('See you soon!')
        await ctx.bot.close()
    else:
        await ctx.respond('Okey.')

def load(bot):
    bot.add_plugin(moderation)

def unload(bot):
    bot.remove_plugin(moderation)
