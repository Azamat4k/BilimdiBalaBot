
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = os.getenv("ADMINS", "").split(",")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

user_lang = {}

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("🏁 Тілді ауыстыру / Сменить язык"))

@dp.message_handler(lambda msg: msg.text in ["🏁 Тілді ауыстыру / Сменить язык"])
async def choose_language(message: types.Message):
    kb_lang = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_lang.add(KeyboardButton("Қазақша"), KeyboardButton("Русский"))
    await message.answer("Тілді таңдаңыз / Выберите язык:", reply_markup=kb_lang)

@dp.message_handler(lambda msg: msg.text in ["Қазақша", "Русский"])
async def set_language(message: types.Message):
    lang = "kz" if message.text == "Қазақша" else "ru"
    user_lang[message.from_user.id] = lang
    await main_menu(message)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_lang[message.from_user.id] = "kz"
    await message.answer("Главное меню / Басты мәзір:", reply_markup=kb)
    await main_menu(message)

@dp.message_handler(lambda msg: msg.text in [
    "🧠 Олимпиада", "📚 Курстар", "❓ Сұрақ қою", "📞 Байланыс", "❤️ Қайырымдылық",
    "🗣 Тілді ауыстыру", "📚 Курсы", "❓ Задать вопрос", "📞 Контакты", "❤️ Благотворительность", "🗣 Сменить язык"])
async def main_menu(message: types.Message):
    lang = user_lang.get(message.from_user.id, "kz")
    responses = {
        "kz": {
            "🧠 Олимпиада": "Олимпиада туралы ақпарат: https://bilimdibala.kz/olympiada",
            "📚 Курстар": "Барлық курстар: менталды арифметика, каллиграфия, ағылшын тілі т.б.",
            "❓ Сұрақ қою": "Сұрағыңызды бізге жазыңыз.",
            "📞 Байланыс": "Тел: +7 777 777 7777 | Instagram: @bilimdibala.shchuchinsk",
            "❤️ Қайырымдылық": "Қайырымдылық туралы: https://bilimdibala.kz/fund"
        },
        "ru": {
            "🧠 Олимпиада": "Информация об олимпиаде: https://bilimdibala.kz/olympiada",
            "📚 Курсы": "Курсы: ментальная арифметика, каллиграфия, английский язык и др.",
            "❓ Задать вопрос": "Вы можете задать свой вопрос здесь.",
            "📞 Контакты": "Тел: +7 777 777 7777 | Instagram: @bilimdibala.shchuchinsk",
            "❤️ Благотворительность": "О фонде: https://bilimdibala.kz/fund"
        }
    }
    text = responses[lang].get(message.text, "Қате команда / Неверная команда")
    await message.answer(text, reply_markup=kb)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
