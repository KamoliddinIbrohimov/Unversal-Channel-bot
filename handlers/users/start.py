from aiogram import types
from data.config import CHANNELS
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.subscription import check_button
from utils.misc import subsciription
from loader import dp,bot


@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    channels_format =  str()
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        #logging.info(invite_link)
        channels_format += f"➡<a href='{invite_link}'>{chat.title}</a>\n"

    await message.answer(f"Botimizdan foydalanish uchun quyidagi kanallarga obuna buling: \n"
                         f"{channels_format}",
                         reply_markup=check_button,
                         disable_web_page_preview=True)


@dp.callback_query_handler(text='check_subs')
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await subsciription.check(user_id=call.from_user.id,
                                           channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"✅<b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            invite_link = await channel.export_invite_link()
            result += (f"❌<b>{channel.title}</b> kanaliga obuna bo'lmagansiz."
                       f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")

    await call.message.answer(result, disable_web_page_preview=True)



