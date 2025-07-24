import logging
from aiogram import Bot, Dispatcher, executor, types
import os

# Токен мен админдерді ортадан алу
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = os.getenv("ADMINS", "").split(",")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Тілдерді сақтау
user_lang = {}

# /start пәрмені
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🇰🇿 Қазақша", "🇷🇺 Русский")
    await message.answer("Тілді таңдаңыз / Выберите язык:", reply_markup=kb)

@dp.message_handler(lambda msg: msg.text in ["🇰🇿 Қазақша", "🇷🇺 Русский"])
async def set_language(message: types.Message):
    lang = "kz" if "Қазақ" in message.text else "ru"
    user_lang[message.from_user.id] = lang

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "kz":
        kb.add("🏆 Олимпиада", "📚 Курстар", "❓Сұрақ қою", "📞 Байланыс", "❤️ Қайырымдылық")
        await message.answer("Басты мәзірге қош келдіңіз:", reply_markup=kb)
    else:
        kb.add("🏆 Олимпиада", "📚 Курсы", "❓Задать вопрос", "📞 Контакты", "❤️ Благотворительность")
        await message.answer("Добро пожаловать в главное меню:", reply_markup=kb)

@dp.message_handler(lambda msg: msg.text in ["🏆 Олимпиада", "📚 Курстар", "❓Сұрақ қою", "📞 Байланыс", "❤️ Қайырымдылық", 
                                              "🏆 Олимпиада", "📚 Курсы", "❓Задать вопрос", "📞 Контакты", "❤️ Благотворительность"])
async def main_menu(message: types.Message):
    lang = user_lang.get(message.from_user.id, "kz")
    responses = {
        "kz": {
            "🏆 Олимпиада": "Олимпиада жайлы толық ақпаратты мына сілтеме арқылы ала аласыз: https://bilimdibala.kz/olympiada",
            "📚 Курстар": "Курстар тізімі: менталды арифметика, жылдам оқу, каллиграфия, ағылшын тілі т.б.",
            "❓Сұрақ қою": "Сұрағыңызды бізге осы жерден жаза аласыз.",
            "📞 Байланыс": "Байланыс: +7 777 777 7777
Instagram: @bilimdibala.shchuchinsk",
            "❤️ Қайырымдылық": "Қайырымдылық қоры туралы толық ақпарат: https://bilimdibala.kz/fund"
        },
        "ru": {
            "🏆 Олимпиада": "Полную информацию об олимпиаде вы найдете по ссылке: https://bilimdibala.kz/olympiada",
            "📚 Курсы": "Курсы: ментальная арифметика, скорочтение, каллиграфия, английский язык и др.",
            "❓Задать вопрос": "Вы можете задать вопрос здесь.",
            "📞 Контакты": "Контакты: +7 777 777 7777
Instagram: @bilimdibala.shchuchinsk",
            "❤️ Благотворительность": "Вся информация о фонде: https://bilimdibala.kz/fund"
        }
    }
    await message.answer(responses[lang].get(message.text, "Қате орын алды."))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)