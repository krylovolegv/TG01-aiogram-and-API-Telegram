import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests
from googletrans import Translator
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

def get_random_joke():
    url = 'https://geek-jokes.sameerkumar.website/api?format=json'
    response = requests.get(url)
    joke = response.json()['joke']
    return joke

def translate_to_russian(text):
    translation = translator.translate(text, src='en', dest='ru')
    return translation.text

@dp.message(Command("joke"))
async def send_joke(message: Message):
    joke = get_random_joke()
    joke_in_russian = translate_to_russian(joke)
    await message.answer(joke_in_russian)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

