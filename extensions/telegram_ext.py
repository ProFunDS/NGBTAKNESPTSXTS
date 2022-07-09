from mongo import tg_keys, users
from mongo.utils import create_pack

from lightbulb import (Plugin, SlashCommand, SlashContext, add_checks, command,
                       implements, option)
from lightbulb.checks import guild_only


telegram = Plugin('Telegram System')

@telegram.command
@add_checks(guild_only)
@option('secret_key', 'The secret key that you received in the NAME telegram bot')
@command('connect_telegram_account',
    'Link telegram and discord profiles',
    auto_defer=True)
@implements(SlashCommand)
async def connect_tg_account_command(ctx: SlashContext):
    secret_key = ctx.options.secret_key.strip()
    m_id = ctx.author.id

    key = await tg_keys.find_one({'key': secret_key})
    if key is None:
        return await ctx.respond(
            'Invalid secret key.\nPlease call the `/my_secret_key` command in the NAME telegram bot')

    user = await users.find_one({'_id': m_id})
    if user is None:
        t = 'For some reason you are not in our database.\nNow I will create...'
        await ctx.respond(t)
        return await users.insert_one(create_pack(m_id))

    await tg_keys.delete_one({'key': secret_key})

    if user['telegram_id']:
        return await ctx.respond(
            'You have already linked your telegram account.\nPlease do not generate secret keys!')

    await users.update_one(
        {'_id': m_id},
        {'$set': {'telegram_id': key['_id']}})

    t = 'Now you can get experience for chatting in our Telegram group, and also use the `/my_statistics` command in Telegram'
    await ctx.respond(f'Successfully `✅`\n{t}')


def load(bot):
    bot.add_plugin(telegram)

def unload(bot):
    bot.remove_plugin(telegram)
