from asyncio import sleep

from random import choice

from mongo import users

from config import DEV_CHANNEL_ID, EVENT_MANAGER_ROLE_ID, GUILD_MEMBER_ROLE_ID
from config.rating_settings import EFL, IMR, LR, LR_IMR
from config.utils import colors

from hikari import Embed
from lightbulb import (Plugin, SlashCommand, SlashContext, add_checks, command,
                       has_roles, implements, option)


events = Plugin('Events System')

@events.command
@add_checks(has_roles(EVENT_MANAGER_ROLE_ID))
@option('inline', 'Enable inline mode?', bool, default=True)
@option('delay', 'Delay between selection', int, default=6)
@option('number_of_winners', 'The number of winners to be selected', int)
@command('raffle', 'Random drawing between Guild Members', auto_defer=True)
@implements(SlashCommand)
async def raffle_command(ctx: SlashContext):
    o = ctx.options
    
    members = await ctx.app.rest.fetch_members(ctx.guild_id)
    members = [m for m in members if GUILD_MEMBER_ROLE_ID in m.role_ids]
    
    embed = Embed(title='Raffle!', color=colors['lightblue'])
    embed.set_image('https://media0.giphy.com/media/vCUjNFrZOW7kjl9fEO/giphy.gif?cid=ecf05e47pfq8xy8hdz34wt527kpdv3xuvdprr4fy4lo6eo6s&rid=giphy.gif&ct=s')
    
    msg = await ctx.respond(embed=embed)

    for _ in range(1, o.number_of_winners+1):
        await sleep(o.delay)

        winner = choice(members)
        members.remove(winner)
        
        winner_entry = await users.find_one({'_id': winner.id})
    
        text = 'Need to check Ronin'

        if winner_entry:
            level, im = winner_entry['exp']//EFL, winner_entry['im']
            if (level >= LR) or (im >= IMR and level >= LR_IMR):
                text = f'{level} level and {im} invited members'

        embed.title = f'Choice #{_}'
        embed.add_field(f'🥇 {text}', winner.display_name, inline=o.inline)
        await msg.edit(embed=embed)
        
    await sleep(2)
    embed.title = f'Winners! Congratulations!'
    embed.set_image()
    await msg.edit(embed=embed)

@events.command
@add_checks(has_roles(EVENT_MANAGER_ROLE_ID))
@option('inline', 'Enable inline mode?', bool, default=True)
@option('delay', 'Delay between selection', int, default=6)
@option('number_of_winners', 'The number of winners to be selected', int)
@command('raffle_axie', 'Random drawing between Guild Members', auto_defer=True)
@implements(SlashCommand)
async def raffle_axie_command(ctx: SlashContext):
    o = ctx.options
    
    members = await ctx.app.rest.fetch_members(ctx.guild_id)
    members = [m for m in members if GUILD_MEMBER_ROLE_ID in m.role_ids]
    
    embed = Embed(title='Raffle!', color=colors['lightblue'])
    embed.set_image('https://media0.giphy.com/media/sGBejL5i7iS9RTMnKx/giphy.gif?cid=ecf05e47nqwz8iep04yjcqvbxz6ghowog2mafs9n4oawowlm&rid=giphy.gif&ct=s')
    
    msg = await ctx.respond(embed=embed)
    
    # refactor this
    axies = [8657599, 3665669, 10953634, 3574308, 5831197, 1169842, 608726, 1800835, 525894]
    if len(axies) == 0:
        return await ctx.respond('Please fill in the list')

    for _ in range(1, o.number_of_winners+1):
        await sleep(o.delay)

        winner = choice(members)
        members.remove(winner)

        axie = axies[_-1]
        text = f'[won Axie#{axie}!](https://marketplace.axieinfinity.com/axie/{axie}/)'

        embed.title = f'Choice #{_}'
        embed.add_field(f'🏆 #{_}', f'{winner.display_name}\n{text}', inline=o.inline)
        await msg.edit(embed=embed)
        
    await sleep(2)
    embed.title = f'Winners! Congratulations!'
    embed.set_image()
    await msg.edit(embed=embed)

    await sleep(5)
    dev_channel = await ctx.app.rest.fetch_channel(DEV_CHANNEL_ID)
    await dev_channel.send(embed=embed)


def load(bot):
    bot.add_plugin(events)

def unload(bot):
    bot.remove_plugin(events)
