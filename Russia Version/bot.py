from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher.filters import Text
import config as cfg
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
import logging

storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)
bot = Bot(token=cfg.TOKEN)


kb =  types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
kb2 = types.KeyboardButton('🧑‍💻 Мои команды 🧑‍💻:')
kb3 = types.KeyboardButton('🧑‍💻 Главное меню 🧑‍💻')
kb4 = types.KeyboardButton('🧑‍💻 Основатель 🧑‍💻')
kb.add(kb2,kb3,kb4)


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS) #greeting new users
async def new_chat_member_handler(message: types.Message):
    for member in message.new_chat_members:
        await message.reply(f"Welcome, {member.full_name} (@{member.username})!")

@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER) #farewell to departed users
async def left_chat_member_handler(message: types.Message):
    member = message.left_chat_member
    await message.reply(f"До свидания, {member.full_name} (@{member.username})!")
    

@dp.message_handler(commands=['start'])
async def startbot(message: types.Message):
   await message.answer(f'Hello {message.from_user.first_name},выбери одну из кнопок ниже для продолжения', reply_markup=kb)    

@dp.message_handler(Text(equals="🧑‍💻 Мои команды 🧑‍💻:"))
async def kommenu(message: types.Message):
      await message.reply(f"{message.from_user.first_name}, специально для вас я покажу свои команды \n Мои команды: /start, \n /ban (для администрации)")

@dp.message_handler(Text(equals="🧑‍💻 Главное меню 🧑‍💻"))
async def kommenu2(message: types.Message):   
   await message.reply(f"{message.from_user.first_name}, <b>главное меню</b> по вашей просьбе", reply_markup=kb, parse_mode=types.ParseMode.HTML)

@dp.message_handler(Text(equals="🧑‍💻 Основатель 🧑‍💻"))
async def kommenu3(message: types.Message):   
   await message.reply(f"{message.from_user.first_name}, <b>Данный бот был сделан разработчиком <a href='https://t.me/Bogdan_Mirosh'>WEBBOGDAN</a></b>, чтобы поддержать нашего с вами любимца) подпишитесь на его <a href='https://github.com/BOGDANMIROSHNICHENKO'><b>GITHUB</b></a>", reply_markup=kb, parse_mode=types.ParseMode.HTML)


logging.basicConfig(level=logging.INFO)


@dp.message_handler(Command("ban"))
async def ban_user(message: types.Message, state: FSMContext):
    if message.from_user.id in cfg.admins:  
        if message.reply_to_message:  
            user_id = message.reply_to_message.from_user.id  
            try:
                await bot.kick_chat_member(message.chat.id, user_id)  
                await message.reply(f"Пользователь {user_id} был забанен.")  
            except Exception as e:
                await message.reply("Произошла ошибка при бане пользователя.")
                logging.error(f"Ошибка бана пользователя: {e}")
        else:
            await message.reply("Ответьте на сообщение пользователя, которого хотите забанить.")
    else:
        await message.reply("Вы не являетесь администратором группы.")

@dp.message_handler()
async def mess_handler(message: types.Message):     
    text = message.text.lower()
    text2 = message.text.lower().replace(' ', '')
    for word in cfg.WORDS:
        if word in text:
            await message.delete()
            await message.answer( 'Ругаться плохо') 
        if word in text2:
            await message.delete()
            await message.answer( 'Ругаться плохо')
    if message.reply_to_message:
        for respmes in cfg.RESPECT:
            if respmes in text:
                await message.reply(f'Уважание оказано пользователем @{message.from_user.username}')

executor.start_polling(dp, skip_updates=True)