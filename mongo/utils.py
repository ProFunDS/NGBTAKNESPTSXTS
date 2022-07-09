from datetime import datetime as dt

from mongo import users


def create_pack(m_id, exp = 0, im = 0, 
            time = None, refer_id = None) -> dict:
    time = time or dt.now()
    return {'_id': m_id, 'exp': exp, 'im': im,
         'time': time,
         'refer_id': refer_id,
         'telegram_id': None,
         'voice_time': time}

async def delete_entry(m_id) -> None:
    user = await users.find_one({'_id': m_id})
    if user:
        await users.delete_one({'_id': m_id})
        if user['refer_id']:
            refer = await users.find_one({'_id': user['refer_id']})
            if refer:
                await users.update_one(
                    {'_id': refer['_id']},
                    {'$set': {'im': refer['im']-1}})