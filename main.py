
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

# Start command with language selection
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🇰🇿 Қазақша"), KeyboardButton("🇷🇺 Русский"))
    await message.answer("Тілді таңдаңыз / Выберите язык:", reply_markup=keyboard)

# Language handlers
@dp.message_handler(lambda message: message.text in ["🇰🇿 Қазақша", "🇷🇺 Русский"])
async def choose_language(message: types.Message):
    lang = message.text
    if lang == "🇰🇿 Қазақша":
        await message.answer("Қош келдіңіз! BilimdiBalaBot сізге көмектеседі.")
    else:
        await message.answer("Добро пожаловать! BilimdiBalaBot поможет вам.")

if __name__ == "__main__":
    executor.start_polling(dp)
