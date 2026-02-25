import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from openai import OpenAI
from aiohttp import web  # Додаємо для веб-сервера

# КОНФІГУРАЦІЯ
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- БЛОК ДЛЯ RENDER (Щоб не засинав) ---
async def handle(request):
    return web.Response(text="Бот працює! 🐾")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render передає порт через змінну оточення PORT
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Веб-сервер запущено на порту {port}")
# ----------------------------------------

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Додаємо лог, щоб ти бачив запуск у консолі Render
    print(f"!!! БОТА ЗАПУСТИВ: {message.from_user.full_name}") 
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

# ... (решта твоїх функцій mono_consult, run_analysis тощо залишаються без змін)

@dp.message(F.text == "🤖 Консультація по mono")
async def mono_consult(message: types.Message):
    await message.answer("На зв'язку! 🐾\n\nЗапитуй про будь-що.")

@dp.message(F.text == "🚀 Запустити AI-аналіз ринку")
async def run_analysis(message: types.Message):
    status = await message.answer("🔍 Аналізую активність конкурентів... 🐾")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти — професійний аналітик monobank."},
                {"role": "user", "content": "Що там цікавого у конкурентів?"}
            ]
        )
        await status.edit_text(f"📊 **Огляд ринку:**\n\n{response.choices[0].message.content}")
    except Exception as e:
        await status.edit_text(f"❌ Помилка: {e}")

# (Додай сюди інші свої функції, які були в оригінальному коді)

async def main():
    # Запускаємо веб-сервер паралельно з ботом
    await start_webserver()
    # Запускаємо бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот зупинений")
