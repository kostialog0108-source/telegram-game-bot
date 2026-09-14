import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not RENDER_URL:
    raise RuntimeError("RENDER_EXTERNAL_URL is not set")

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Твой игровой бот запущен 🎮"
    )


async def on_startup():
    await bot.set_webhook(
        url=f"{RENDER_URL}/webhook"
    )


async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

app = web.Application()

SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
).register(app, path="/webhook")

setup_application(app, dp, bot=bot)

web.run_app(
    app,
    host="0.0.0.0",
    port=PORT,
)
