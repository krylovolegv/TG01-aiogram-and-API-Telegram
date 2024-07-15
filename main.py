import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import random
from config import TOKEN
from datetime import datetime, timedelta
from gtts import gTTS
import os

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кэш для хранения данных о погоде
weather_cache = {}
CACHE_EXPIRATION = timedelta(minutes=30)  # Кэш истекает через 30 минут


async def get_weather():
    latitude = 54.7065  # Широта Калининграда
    longitude = 20.5106  # Долгота Калининграда

    # Проверяем, есть ли актуальные данные в кэше
    current_time = datetime.now()
    if 'weather' in weather_cache and current_time - weather_cache['timestamp'] < CACHE_EXPIRATION:
        return weather_cache['weather']

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    try:
        response = requests.get(url, timeout=10)  # Добавляем таймаут
        response.raise_for_status()  # Вызовет исключение для HTTP-ошибок

        data = response.json()
        current = data['current']

        temperature = current['temperature_2m']
        wind_speed = current['wind_speed_10m']

        weather_info = f"Погода в Калининграде:\nТемпература: {temperature}°C\nСкорость ветра: {wind_speed} м/с"

        # Обновляем кэш
        weather_cache['weather'] = weather_info
        weather_cache['timestamp'] = current_time

        return weather_info
    except requests.RequestException as e:
        print(f"Ошибка при запросе погоды: {e}")
        return "Извините, не удалось получить данные о погоде. Попробуйте позже."


@dp.message(Command('weather'))
async def weather(message: Message):
    weather_info = await get_weather()
    await message.answer(weather_info)

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('samurai2.mp4')
    await message.answer_video(video=video)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('house.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save('training.mp3')
   audio = FSInputFile('training.mp3')
   await bot.send_audio(message.chat.id, audio)
   os.remove("training.mp3")

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://avatanplus.com/files/resources/original/58cc4caaaf88815ade0b7adf.png',
            'https://i.ebayimg.com/images/g/x7EAAOSwGzxdbG~j/s-l500.jpg',
            'https://avatars.mds.yandex.net/i?id=818f796dfb4c6612baccd142f4664084b19963f1-2417823-images-thumbs&n=13']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /weather \n /photo")


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.full_name}')

@dp.message()
async def start(message: Message):
		if message.text.lower() == 'test':
                    await message.answer('Тестируем')

@dp.message()
async def start(message: Message):
    await message.send_copy(chat_id=message.chat.id)

@dp.message()
async def start(message: Message):
    await message.answer("Я тебе ответил")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())