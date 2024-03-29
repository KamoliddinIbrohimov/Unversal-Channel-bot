from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS, CHANNELS
from keyboards.inline.manage_post import confirmation_keyboard, post_callback
from loader import dp, bot
from states.createpost import CreatePost


@dp.message_handler(Command("yangi_post"))
async def create_post(message:Message):
    await message.answer("Chop etish uchun post kiriting")
    await CreatePost.NewMessage.set()


@dp.message_handler(state=CreatePost.NewMessage)
async def enter_message(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
    await message.answer(f"Postni adminga yuboraymi?",
                         reply_markup=confirmation_keyboard)
    await CreatePost.next()


@dp.callback_query_handler(post_callback.filter(action='post'), state=CreatePost.Confirm)
async def confirm_post(call:CallbackQuery, state:FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post adminga yuborildi")
    await bot.send_message(ADMINS[0], f"foydalanuvchi {mention} quyidagi postni chop ettirmoqchi:")
    await bot.send_message(ADMINS[0], text, parse_mode="HTML", reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=CreatePost.Confirm)
async def cansel_post(call: CallbackQuery, state:FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer("Post rad etildi")
    await state.finish()

@dp.message_handler(state=CreatePost.Confirm)
async def post_unknown(message: Message):
    await message.answer('Chop etish yoki rad etish tugmasini bosing')


@dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
async def approve_post(call: CallbackQuery):
    await call.answer("Chop etishga ruxsat berdinggiz.", show_alert=True)
    target_channel = "-1001446817061"
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)


@dp.callback_query_handler(post_callback.filter(action="cancel"), user_id=ADMINS)
async def decline_post(call: CallbackQuery):
    await call.answer("Post rad etildi.", show_alert=True)
    await call.message.edit_reply_markup()


