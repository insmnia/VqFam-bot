from aiogram import types
from misc import dp,bot
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from json import load, dump

@dp.message_handler(commands=['start'])
async def starting_message(message: types.Message):
    username = message.from_user.username
    with open("users.json",'r') as db:
        db_users = load(db)

    if username not in db_users:
        db_users[username] = {}
        db_users[username]['user_id'] = message.from_user.id
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

@dp.message_handler(commands=['help'])
async def show_help(message: types.Message):
    help_msg = '''
    Здесь представлен список всех команд:
    1)Заполнить информацию о себе(/setinfo)[см./sethelp для подробностей].
    2)Посмотреть информацию о пользователе(/getinfo @username).Посмотреть информацию о себе(/getinfo).
    '''

    await bot.send_message(message.chat.id,help_msg)

@dp.message_handler(commands=['sethelp'])
async def show_sethelp(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Перейти к чату',url ='https://web.telegram.org/#/im?p=@VQfamBY_bot'))
    sethelp_msg = '''
    Хэй, у меня есть для тебя пару вопросов!
    Напиши мне в личное сообщение /setinfo для заполнения информации.
    <i>PS можно и тут, но будет удобнее в ЛС</i>.
    '''
    await bot.send_message(message.chat.id,sethelp_msg,parse_mode=ParseMode.HTML,reply_markup=kb)


@dp.message_handler(commands=['getinfo'])
async def get_user_info(message: types.Message):
    try:
        if len(message.text)>10:
            username = message.text.split()[1].replace('@','')
            with open("users.json",'r') as db:
                db_users = load(db)

            name = db_users[username]['name'].replace('b','').replace("'",'')
            user_info = f'<b>Никнейм пользователя</b> - {username}\n'\
                        f"<b>Имя пользователя</b> - {name}\n"\
                        f"<b>Дата рождения</b> - {db_users[username]['bd']}\n"\
                        f"<b>Автомобиль</b> - {db_users[username]['car']}\n"\
                        f"<b>Номер автомобиля</b> - {db_users[username]['car_number']}"
            
            await bot.send_message(message.chat.id,user_info,parse_mode=ParseMode.HTML)
        else:

            username = message.from_user.username

            with open("users.json",'r') as db:
                db_users = load(db)

            name = db_users[username]['name'].replace('b','').replace("'",'')

            
            user_info = f'<b>Никнейм пользователя</b> - {username}\n'\
                        f"<b>Имя пользователя</b> - {name}\n"\
                        f"<b>Дата рождения</b> - {db_users[username]['bd']}\n"\
                        f"<b>Автомобиль</b> - {db_users[username]['car']}\n"\
                        f"<b>Номер автомобиля</b> - {db_users[username]['car_number']}"
            
            await bot.send_message(message.chat.id,user_info,parse_mode=ParseMode.HTML)
    except:
        await message.reply('Проверьте правильность введенной комады. Возможно, пользователя нет в базе.')

@dp.message_handler(commands=['clear'])
async def clear_chat(message: types.Message):
    try:
        with open('users.json','r') as db:
            db_users = load(db)
        
        if db_users[message.from_user.username]['admin']==1:
            users = []
            for user in db_users:
                ChatMember = await bot.get_chat_member(chat_id=message.chat.id,user_id = db_users[user]['user_id'])
                if ChatMember.status == 'left':
                    del db_users[user]
    except:
        pass