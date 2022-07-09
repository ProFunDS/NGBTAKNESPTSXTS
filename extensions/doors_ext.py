from random import choice

from datetime import datetime as dt

from config import BOT_CHANNEL_ID, LOGO_EMOJI
from config.rating_settings import PPMV

from mongo import users
from mongo.utils import create_pack, delete_entry

from hikari.events.member_events import MemberCreateEvent, MemberDeleteEvent
from hikari.events.voice_events import VoiceStateUpdateEvent

from lightbulb import Plugin


doors = Plugin('Doors System')

@doors.listener(MemberCreateEvent)
async def member_join_event(e: MemberCreateEvent):
    if e.member.is_bot:
        return
    channel = e.get_guild().get_channel(BOT_CHANNEL_ID)
    emojis = await e.app.rest.fetch_guild_emojis(e.guild_id)
    t = f'{e.member.mention}, welcome to **NAME Guild**! {LOGO_EMOJI} {choice(emojis)}\
    \nIf you were invited here by another member, please specify it using the `/specify_my_referrer` command\
    \nGet information about the guild and NAME-Bot: `/help` command'
    await channel.send(t)

@doors.listener(MemberDeleteEvent)
async def member_left_event(event: MemberDeleteEvent):
    await delete_entry(event.user_id)

@doors.listener(VoiceStateUpdateEvent)
async def voice_state_update_event(event: VoiceStateUpdateEvent):
    state = event.state
    if state.member.is_bot:
        return

    old_state = event.old_state

    if old_state and state.channel_id:
        return
    
    m_id = state.user_id

    user = await users.find_one({'_id': m_id})
    if user is None:
        return await users.insert_one(create_pack(m_id))

    now = dt.now()

    set_dict = {'$set': {'voice_time': now}}
    
    if state.channel_id is None:
        new_exp = (now - user['voice_time']).seconds // 60 * PPMV
        set_dict['$set']['exp'] = user['exp'] + new_exp

    await users.update_one({'_id': m_id}, set_dict)

def load(bot):
    bot.add_plugin(doors)

def unload(bot):
    bot.remove_plugin(doors)
