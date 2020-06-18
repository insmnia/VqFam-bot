import re
from json import load, dump
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from misc import dp
from misc import bot

class Register(StatesGroup):
    
    name = State()
    date = State()
    car = State()
    car_number = State()

with open("users.json",'r') as db:
    db_users = load(db)

@dp.message_handler(commands=['setinfo'], state='*')
async def register(message: types.Message):

    await message.reply('Готовы к регистрации? Тогда начнем!\n <b>Введите имя:</b>',parse_mode=ParseMode.HTML)
    await Register.name.set()

@dp.message_handler(commands=['cancel'], state='*')
async def register(message: types.Message,state: FSMContext):

    try:
        await state.finish()
        await message.reply('Процесс регистрации остановлен')

    except:
        pass

@dp.message_handler(state=Register.name,content_types=types.ContentTypes.TEXT)
async def getname(message: types.Message,state: FSMContext):

    await state.update_data(name=message.text)
    await Register.next()
    await message.answer('Теперь введите дату рождения\n<b>Дата рождения:</b>',parse_mode=ParseMode.HTML)

@dp.message_handler(state=Register.date,content_types=types.ContentTypes.TEXT)
async def getdb(message: types.Message,state: FSMContext):

    await state.update_data(date=message.text)
    await Register.next()
    await message.answer('Теперь введите марку машины\n<b>Марка:</b>',parse_mode=ParseMode.HTML)

@dp.message_handler(state=Register.car,content_types=types.ContentTypes.TEXT)
async def getcar(message: types.Message,state: FSMContext):

    await state.update_data(car=message.text)
    await Register.next()
    await message.answer('Остался только номер машины\n<b>Номер:</b>',parse_mode=ParseMode.HTML)

@dp.message_handler(state=Register.car_number,content_types=types.ContentTypes.TEXT)
async def getcarnumber(message: types.Message,state: FSMContext):
    global db_users

    username = message.from_user.username
    await state.update_data(car_number=message.text)

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Да',callback_data='yes'))
    kb.add(InlineKeyboardButton(text='Нет',callback_data='no'))

    user_data = await state.get_data()
    final_register_message = f"<b>Ваше имя:</b> {user_data['name']}\n"\
                             f"<b>Ваша дата рождения:</b> {user_data['date']}\n"\
                             f"<b>Ваша машина:</b> {user_data['car']}\n"\
                             f"<b>Ваш номер машины:</b> {message.text}\n"

    db_users[username]['name'] = user_data['name']
    db_users[username]['bd'] = user_data['date']
    db_users[username]['car'] = user_data['car']
    db_users[username]['car_number'] = message.text

    await state.finish()
    await message.answer(final_register_message,parse_mode=ParseMode.HTML,reply_markup=kb)
    
@dp.callback_query_handler(lambda x: x.data=='yes')
async def save_user_data(callback_query: types.CallbackQuery):

    with open('users.json','w') as db:
        dump(db_users,db)

    await bot.answer_callback_query(callback_query.id, text='Информация была сохранена, введите /getinfo для получения данных')

@dp.callback_query_handler(lambda x: x.data=='no')
async def clear_user_data(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id,text='Информация удалена')