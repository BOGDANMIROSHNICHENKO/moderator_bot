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


kb =  types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1) #button menu
kb2 = types.KeyboardButton('🧑‍💻 My commands 🧑‍💻:')
kb3 = types.KeyboardButton('🧑‍💻 Main menu 🧑‍💻')
kb4 = types.KeyboardButton('🧑‍💻 Owner 🧑‍💻')
kb.add(kb2,kb3,kb4)


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS) #greeting new users
async def new_chat_member_handler(message: types.Message):
    for member in message.new_chat_members:
        await message.reply(f"Welcome, {member.full_name} (@{member.username})!")

@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER) #farewell to departed users
async def left_chat_member_handler(message: types.Message):
    member = message.left_chat_member
    await message.reply(f"Goodbye, {member.full_name} (@{member.username})!")
    

@dp.message_handler(commands=['start']) #Button Handler
async def startbot(message: types.Message):
   await message.answer(f'Hello {message.from_user.first_name}, choose one of the buttons below to continue', reply_markup=kb)    

@dp.message_handler(Text(equals="🧑‍💻 My commands 🧑‍💻:"))
async def kommenu(message: types.Message):
      await message.reply(f"{message.from_user.first_name}, especially for you, I will show my commands \n My commands: /start, \n /ban (for administration)")

@dp.message_handler(Text(equals="🧑‍💻 Main menu 🧑‍💻"))
async def kommenu2(message: types.Message):   
   await message.reply(f"{message.from_user.first_name}, <b>main menu</b> at your request", reply_markup=kb, parse_mode=types.ParseMode.HTML)

@dp.message_handler(Text(equals="🧑‍💻 Owner 🧑‍💻"))
async def kommenu3(message: types.Message):   
   await message.reply(f"{message.from_user.first_name}, <b><b>This bot was made by the developer <a href='https://t.me/Bogdan_Mirosh'>WEBBOGDAN</a></b> to support our pet) subscribe to his <a href='https ://github.com/BOGDANMIROSHNICHENKO'><b>GITHUB</b></a>", reply_markup=kb, parse_mode=types.ParseMode.HTML)


logging.basicConfig(level=logging.INFO)


@dp.message_handler(Command("ban")) #command ban
async def ban_user(message: types.Message, state: FSMContext):
    if message.from_user.id in cfg.admins:  
        if message.reply_to_message:  
            user_id = message.reply_to_message.from_user.id  
            try:
                await bot.kick_chat_member(message.chat.id, user_id)  
                await message.reply(f"User {user_id} was banned.")  
            except Exception as e:
                await message.reply("An error occurred while banning a user.")
                logging.error(f"User ban error: {e}")
        else:
            await message.reply("Reply to the message of the user you want to ban.")
    else:
        await message.reply("You are not a group administrator.")

@dp.message_handler()
async def mess_handler(message: types.Message):    #filter bad words 
    text = message.text.lower()
    text2 = message.text.lower().replace(' ', '')
    for word in cfg.WORDS:
        if word in text:
            await message.delete()
            await message.answer( 'Swear badly') 
        if word in text2:
            await message.delete()
            await message.answer( 'Swear badly')
    if message.reply_to_message:
        for respmes in cfg.RESPECT:
            if respmes in text:
                await message.reply(f'Уважание оказано пользователем @{message.from_user.username}') #respect to user

executor.start_polling(dp, skip_updates=True)

