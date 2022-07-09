from datetime import datetime as dt

from config import GUILD_MEMBER_ROLE_ID, USER_ROLE_ID
from config.rating_settings import EFL, EPIM, IMR, LR, LR_IMR, PPM, WT

from mongo import users
from mongo.utils import DESCENDING, create_pack

from hikari import CommandChoice, Embed, ForbiddenError, Member
from hikari.events.message_events import GuildMessageCreateEvent

from lightbulb import (Plugin, SlashCommand, SlashContext, add_checks, command,
                       implements, option)
from lightbulb.checks import guild_only


rating = Plugin('Rating System')

async def check_user(e, m: Member, im: int, exp: int) -> None:
    check = (im >= IMR) and (exp >= LR_IMR*EFL)
    if check or exp >= LR*EFL:
        await m.add_role(GUILD_MEMBER_ROLE_ID)
        await m.remove_role(USER_ROLE_ID)
        try:
            await m.edit(nickname=f'NAME | {m.username}',)
        except ForbiddenError:
            pass
        t = f'{m.mention}**, сongratulations! You get the role of a guild member for your activity!**'
        ch = e.get_channel()
        await ch.send(t)

@rating.listener(GuildMessageCreateEvent)
async def on_message(e: GuildMessageCreateEvent):
    if e.is_bot or e.is_webhook:
        return

    m_id = e.author_id

    user = await users.find_one({'_id': m_id})
    if user is None:
        return await users.insert_one(create_pack(m_id))

    now = dt.now()
    if (now - user['time']).seconds > WT:
        exp = user['exp'] + PPM
        await users.update_one({'_id': m_id},
            {'$set': {'exp': exp, 'time': now}})

        m = e.get_member()
        if GUILD_MEMBER_ROLE_ID not in m.role_ids:
            await check_user(e, m, user['im'], exp)

@rating.command
@add_checks(guild_only)
@option('member',
    'The member who will me recorded as a referrer',
    Member)
@command('specify_my_referrer',
    'Specify the referrer who invited me to the guild',
    auto_defer=True)
@implements(SlashCommand)
async def specify_referrer_command(ctx: SlashContext):
    if ctx.options.member.is_bot:
        return await ctx.respond("It's a bot!")
        
    author_id = ctx.author.id
    referrer_id = ctx.options.member.id
    
    if author_id == referrer_id:
        return await ctx.respond("Don't try to identify yourself as a referrer.")

    author_entry = await users.find_one({'_id': author_id})
    referrer_entry = await users.find_one({'_id': referrer_id})

    if author_entry is None:
        await users.insert_one(author_entry := create_pack(author_id))
    elif author_entry['refer_id']:
        return await ctx.respond('You have already entered your referrer.')

    if referrer_entry is None:
        await users.insert_one(referrer_entry := create_pack(referrer_id))

    await users.update_one({'_id': author_id},
        {'$set': {'refer_id': referrer_id, 'exp': author_entry['exp']+EFL}})
    await users.update_one({'_id': referrer_id},
        {'$set': {'im': referrer_entry['im']+1, 'exp': referrer_entry['exp']+EPIM}})

    t = f'You get {EFL} exp and your referrer gets {EPIM} exp.'
    await ctx.respond(f'Successfully `✅`\n{t}\n`/show_statistics`')

@rating.command
@add_checks(guild_only)
@option('member',
    'The member whose statistics will displayed (optional)',
    Member,
    default=None)
@command('show_statistics', "Get information about my or someone else's profile", auto_defer=True)
@implements(SlashCommand)
async def profile_command(ctx: SlashContext):
    m = ctx.options.member or ctx.author
    if m.is_bot:
        return await ctx.respond("It's a bot.")

    guild = ctx.get_guild()
    m_name = guild.get_member(m.id).display_name

    user = await users.find_one({'_id': m.id})
    if user is None:
        await users.insert_one(user := create_pack(m.id))
        
    level, exp = user['exp']//EFL, user['exp']%EFL

    embed = Embed(
        title=f'{m_name} stats',
        timestamp=dt.now()
        )
    embed.set_thumbnail(m.avatar_url)
    
    embed.add_field(
        'Experience',
        f'Level: **{level}**\n **{exp}/{EFL}** | **{round(exp/EFL*100, 1)}**%'
        )
        
    embed.add_field('Invited members', f'Score: **{user["im"]}**')
    
    embed.add_field(
        'Telegram',
        '✅' if user['telegram_id'] else '❌'
        )
    
    if user['refer_id']:
        refer = guild.get_member(user['refer_id'])
        refer = refer.mention if refer else 'Refer not in guild'
        embed.add_field('Referrer', refer)

    embed.set_footer('NAME', icon=guild.icon_url)
    
    await ctx.respond(embed=embed)

@rating.command
@option('size',
    'Choose the dimension of the leaderboard',
    choices=['Only my position', '3', '5', '10', '15'],
    default=5)
@option('sort', 'By experience or by score of invited members',
    choices=[
        CommandChoice(name='by level', value='exp'),
        CommandChoice(name='by score of invited members', value='im')
    ],
    default='exp')
@command('leaderboard', 'Show the leaderboard', auto_defer=True)
@implements(SlashCommand)
async def leaderboard_command(ctx: SlashContext):
    o = ctx.options
    guild = ctx.get_guild()

    count = await users.count_documents({})
    all_users = users.find().sort(o.sort, DESCENDING)
    all_users = await all_users.to_list(count)

    if o.size == 'Only my position':
        user = await users.find_one({'_id': ctx.author.id})
        return await ctx.respond(f'Your position: {all_users.index(user)+1}')
    
    embed = Embed(title='Leaderboard')
    
    for user in all_users[:int(o.size)]:
        match o.sort:
            case 'exp':
                field_name = f"{user['exp']//EFL} level"
            case _:
                field_name = f"{user['im']} invited members"
            
        embed.add_field(
            '🌿 ' + field_name,
            guild.get_member(user['_id']).mention)
            
    # don't refactor this block!
    embed.edit_field(0, embed.fields[0].name.replace('🌿', '🏆'))
    embed.edit_field(1, embed.fields[1].name.replace('🌿', '🥈'))
    embed.edit_field(2, embed.fields[2].name.replace('🌿', '🥉'))
    embed.set_footer('NAME', icon=guild.icon_url)
    
    await ctx.respond(embed=embed)

def load(bot):
    bot.add_plugin(rating)

def unload(bot):
    bot.remove_plugin(rating)
