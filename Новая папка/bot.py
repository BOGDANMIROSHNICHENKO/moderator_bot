from aiogram import Bot, Dispatcher, executor, types

Bot = "6067838225:AAF-r0EP8c4qqd36XBCKts7PwpaMFvG2B9Q"
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def privet(message: types.Message):
        await message.answer('Привет,меня зовут Аися.')


executor.start_polling(dp)
