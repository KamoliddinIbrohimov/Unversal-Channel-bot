from aiogram import types

from loader import dp
import wikipedia

wikipedia.set_lang("uz")


# Wikipedia

@dp.message_handler()
async def send_wiki(message: types.Message):
    print(message.from_user.full_name)
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
    except:
        await message.answer("Bu mavzuga oid wikipedya topilmadi")
