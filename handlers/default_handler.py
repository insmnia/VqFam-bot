from aiogram import types
from misc import dp
from aiogram.types import ParseMode
from json import load, dump

@dp.message_handler(content_types=['new_chat_members'])
async def starting_message(message: types.Message):
    username = message.new_chat_members[0]['username']

    with open("users.json",'r') as db:
        db_users = load(db)

    if username not in db_users:
        db_users[username] = {}
        db_users[username]['user_id'] = message.new_chat_members[0]['id']
        db_users[username]['name'] = ''
        db_users[username]['bd'] = ''
        db_users[username]['car'] = ''
        db_users[username]['car_number'] = ''
    

    start_msg = f"""
    Добро пожаловать в семью <b>VQfamBY</b>, {username}!
    Для просмотра команд напиши /help.
    """
    
    with open('users.json','w') as db:
        dump(db_users,db)

    await bot.send_message(message.chat.id,start_msg,parse_mode=ParseMode.HTML)