import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from openai import OpenAI

# КОНФІГУРАЦІЯ
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="🚀 Запустити AI-аналіз ринку")],
        [types.KeyboardButton(text="📊 Отримати пріоритети беклогу")],
        [types.KeyboardButton(text="📱 Аналіз відгуків (Social/AppStore)")],
        [types.KeyboardButton(text="🤖 Консультація по mono")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        "Привіт! Я твій AI-аналітик у стилі monobank. 🐾\n\n"
        "Допоможу розібратися з ринком, беклогом та відгуками. Обирай потрібний розділ нижче:",
        reply_markup=keyboard
    )

@dp.message(F.text == "🤖 Консультація по mono")
async def mono_consult(message: types.Message):
    await message.answer(
        "На зв'язку! 🐾\n\n"
        "Запитуй про будь-що, що стосується нашого банку. Я працюю виключно в межах проекту monobank."
    )

@dp.message(F.text == "🚀 Запустити AI-аналіз ринку")
async def run_analysis(message: types.Message):
    status = await message.answer("🔍 Аналізую активність конкурентів... 🐾")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти — професійний аналітик monobank. Твій стиль: лаконічність, експертність та дружність. Використовуй емодзі котиків або лапок лише на початку або в кінці повідомлення, не зловживай вигуками."},
                {"role": "user", "content": "Що там цікавого у конкурентів (Sense, Privat, Pumb)?"}
            ]
        )
        await status.edit_text(f"📊 **Огляд ринку:**\n\n{response.choices[0].message.content}")
    except Exception as e:
        await status.edit_text(f"❌ Помилка аналізу: {e}")

@dp.message(F.text == "📊 Отримати пріоритети беклогу")
async def get_backlog(message: types.Message):
    status = await message.answer("📈 Формую стратегію... 🐈")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти — Senior PM у monobank. Надавай чіткі, структуровані пріоритети. Спілкуйся впевнено, як людина. Можеш додати один котячий емодзі в кінці."},
                {"role": "user", "content": "Запропонуй 3 головні задачі для mono на цей квартал."}
            ]
        )
        await status.edit_text(f"🎯 **Пріоритети беклогу:**\n\n{response.choices[0].message.content}")
    except Exception as e:
        await status.edit_text(f"❌ Не вдалося сформувати список: {e}")

@dp.message(F.text == "📱 Аналіз відгуків (Social/AppStore)")
async def analyze_social(message: types.Message):
    status = await message.answer("🔍 Вивчаю фідбек користувачів... 📱")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти аналізуєш відгуки клієнтів mono. Будь конструктивним та емпатичним. Користуйся стилем mono, але без зайвого котячого сленгу."},
                {"role": "user", "content": "Зроби Sentiment Analysis останніх відгуків про mono."}
            ]
        )
        await status.edit_text(f"📱 **Аналіз настроїв:**\n\n{response.choices[0].message.content}")
    except Exception as e:
        await status.edit_text(f"❌ Помилка доступу до даних: {e}")

@dp.message()
async def handle_free_text(message: types.Message):
    if message.text.startswith('/'): return
    
    status = await message.answer("🔄 Обробляю запит... 🤔")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Ти — AI-консультант monobank. Твоя спеціалізація — тільки monobank. "
                        "Відповідай людяно, але стримано. Не використовуй 'Мур' у кожному реченні. "
                        "Якщо питання не про моно — ввічливо відмов. Додавай лапки 🐾 лише як підпис у кінці."
                    )
                },
                {"role": "user", "content": message.text}
            ]
        )
        await status.edit_text(response.choices[0].message.content)
    except Exception as e:
        await status.edit_text(f"❌ Помилка зв'язку: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот зупинений")
