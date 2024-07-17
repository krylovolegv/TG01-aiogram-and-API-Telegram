import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Задание 1: Создание простого меню с кнопками
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Выберите действие:", reply_markup=main_kb)

@dp.message(F.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(F.text == "Пока")
async def say_goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Задание 2: Кнопки с URL-ссылками
@dp.message(Command("links"))
async def cmd_links(message: Message):
    links_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://news.google.com/")],
        [InlineKeyboardButton(text="Музыка", url="https://www.spotify.com/")],
        [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/")]
    ])
    await message.answer("Выберите, куда хотите перейти:", reply_markup=links_kb)

# Задание 3: Динамическое изменение клавиатуры
@dp.message(Command("dynamic"))
async def cmd_dynamic(message: Message):
    dynamic_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.answer("Нажмите кнопку для получения дополнительных опций:", reply_markup=dynamic_kb)

@dp.callback_query(F.data == "show_more")
async def process_show_more(callback: CallbackQuery):
    new_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option2")]
    ])
    await callback.message.edit_text("Выберите опцию:", reply_markup=new_kb)

@dp.callback_query(F.data.startswith("option"))
async def process_option(callback: CallbackQuery):
    option = callback.data
    await callback.answer(f"Вы выбрали {option}", show_alert=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())