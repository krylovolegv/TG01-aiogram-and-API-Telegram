from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Тестовая кнопка 1")],
   [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
   [InlineKeyboardButton(text="Новости", callback_data='news')],
   [InlineKeyboardButton(text="Профиль", callback_data='person')]
])


# Список с четырьмя кнопками
test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

# Асинхронная функция для создания клавиатуры
# async def test_keyboard():
#     keyboard = ReplyKeyboardBuilder()
#     for key in test:
#         keyboard.add(KeyboardButton(text=key))
#     return keyboard.adjust(2).as_markup()

async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   for key in test:
       keyboard.add(InlineKeyboardButton(text=key, url='https://www.youtube.com/watch?v=HfaIcB4Ogxk'))
   return keyboard.adjust(2).as_markup()