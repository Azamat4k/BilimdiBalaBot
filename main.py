import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = os.getenv("ADMINS", "").split(",")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Басты мәзір батырмалары
menu_kz = ["📋 Курстарға жазылу", "📚 Курстар тізімі", "🧑‍🏫 Ұстаздарға арналған", "🧠 Олимпиада", "🤲 Қайырымдылық", "🌐 Онлайн курстар", "🏘️ Филиалдар", "📰 Жаңалықтар", "💬 Сұрақ қою", "🔁 Тілді ауыстыру"]
menu_ru = ["📋 Запись на курсы", "📚 Список курсов", "🧑‍🏫 Для учителей", "🧠 Олимпиада", "🤲 Благотворительность", "🌐 Онлайн курсы", "🏘️ Филиалы", "📰 Новости", "💬 Задать вопрос", "🔁 Сменить язык"]

keyboard_kz = ReplyKeyboardMarkup(resize_keyboard=True).add(*[KeyboardButton(b) for b in menu_kz])
keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True).add(*[KeyboardButton(b) for b in menu_ru])

user_lang = {}

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_lang[message.from_user.id] = "kz"
    await message.answer("Тілді таңдаңыз / Выберите язык:
🇰🇿 Қазақша үшін: /kz
🇷🇺 Русский язык: /ru")

@dp.message_handler(commands=["kz"])
async def lang_kz(message: types.Message):
    user_lang[message.from_user.id] = "kz"
    await message.answer("Қош келдіңіз! Мәзірден таңдаңыз:", reply_markup=keyboard_kz)

@dp.message_handler(commands=["ru"])
async def lang_ru(message: types.Message):
    user_lang[message.from_user.id] = "ru"
    await message.answer("Добро пожаловать! Выберите из меню:", reply_markup=keyboard_ru)

@dp.message_handler()
async def menu_handler(message: types.Message):
    lang = user_lang.get(message.from_user.id, "kz")
    text = message.text

    responses = {
        "kz": {
            "📋 Курстарға жазылу": "Курстарға жазылу үшін: https://wa.me/message/OFCXOW7IN3RMM1",
            "📚 Курстар тізімі": "Менталды арифметика, жылдам оқу, каллиграфия, ағылшын тілі, мектепке дайындық және тағы басқа.",
            "🧑‍🏫 Ұстаздарға арналған": "Ұстаздар үшін франшиза, әдістеме және грант алу курстары бар.",
            "🧠 Олимпиада": "Ұшқыр ой олимпиадасына қатысу: https://bilimdibala.kz/olympiada",
            "🤲 Қайырымдылық": "BilimdiBala қайырымдылық қоры туралы толық ақпарат: https://bilimdibala.kz/fund",
            "🌐 Онлайн курстар": "Онлайн курстарға тіркелу: https://bilimdibala.kz/online",
            "🏘️ Филиалдар": "Біздің филиалдар: Щучинск, Шортанды, Степняк. Толығырақ сайттан қараңыз.",
            "📰 Жаңалықтар": "Соңғы жаңалықтар: BilimdiBala Instagram парақшасынан оқыңыз.",
            "💬 Сұрақ қою": "Сұрағыңызды бізге осы жерден жаза аласыз: https://wa.me/message/OFCXOW7IN3RMM1",
            "🔁 Тілді ауыстыру": "🇷🇺 Орыс тілі үшін /ru деп жазыңыз."
        },
        "ru": {
            "📋 Запись на курсы": "Записаться на курсы: https://wa.me/message/OFCXOW7IN3RMM1",
            "📚 Список курсов": "Ментальная арифметика, скорочтение, каллиграфия, английский язык, подготовка к школе и др.",
            "🧑‍🏫 Для учителей": "Франшиза, методики и курсы по получению субсидий для учителей.",
            "🧠 Олимпиада": "Принять участие в олимпиаде 'Ұшқыр ой': https://bilimdibala.kz/olympiada",
            "🤲 Благотворительность": "О благотворительном фонде BilimdiBala: https://bilimdibala.kz/fund",
            "🌐 Онлайн курсы": "Записаться на онлайн курсы: https://bilimdibala.kz/online",
            "🏘️ Филиалы": "Наши филиалы: Щучинск, Шортанды, Степняк. Подробнее на сайте.",
            "📰 Новости": "Последние новости читайте в Instagram: @bilimdibala.shchuchinsk",
            "💬 Задать вопрос": "Вы можете задать вопрос здесь: https://wa.me/message/OFCXOW7IN3RMM1",
            "🔁 Сменить язык": "🇰🇿 Қазақ тілі үшін /kz деп жазыңыз."
        }
    }

    reply = responses.get(lang, {}).get(text, "❗ Бұл пәрмен қолжетімсіз. / Это действие недоступно.")
    await message.answer(reply)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
