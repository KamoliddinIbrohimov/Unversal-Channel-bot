from aiogram.dispatcher.filters.state import State, StatesGroup


class CreatePost(StatesGroup):
    NewMessage = State()
    Confirm = State()