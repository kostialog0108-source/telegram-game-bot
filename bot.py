import os

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application
)

from database import init_db, create_player, get_player


# =========================
# НАСТРОЙКИ
# =========================

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")


if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not RENDER_URL:
    raise RuntimeError("RENDER_EXTERNAL_URL is not set")


# =========================
# TELEGRAM
# =========================

bot = Bot(TOKEN)
dp = Dispatcher()


# =========================
# КНОПКИ
# =========================

def main_menu():

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="👤 Профиль",
                    callback_data="profile"
                ),

                InlineKeyboardButton(
                    text="💰 Баланс",
                    callback_data="balance"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏢 Бизнесы",
                    callback_data="businesses"
                ),

                InlineKeyboardButton(
                    text="🚗 Транспорт",
                    callback_data="cars"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏠 Недвижимость",
                    callback_data="houses"
                ),

                InlineKeyboardButton(
                    text="📋 Задания",
                    callback_data="quests"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👥 Клан",
                    callback_data="clan"
                )
            ]

        ]
    )

    return keyboard


# =========================
# /START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    user_id = message.from_user.id

    username = message.from_user.username

    if username:
        username = "@" + username
    else:
        username = message.from_user.first_name

    create_player(
        user_id,
        username
    )

    await message.answer(
        "🎮 <b>Добро пожаловать в игру!</b>\n\n"
        "Здесь ты сможешь создавать свою империю, "
        "покупать бизнесы, автомобили и недвижимость.\n\n"
        "Выбирай действие:",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# =========================
# ПРОФИЛЬ
# =========================

@dp.callback_query(lambda callback: callback.data == "profile")
async def profile(callback: CallbackQuery):

    user_id = callback.from_user.id

    player = get_player(user_id)

    if not player:
        create_player(
            user_id,
            callback.from_user.first_name
        )

        player = get_player(user_id)

    user_id = player[0]
    username = player[1]
    balance = player[2]
    level = player[3]
    experience = player[4]

    await callback.message.edit_text(
        f"👤 <b>ПРОФИЛЬ</b>\n\n"
        f"Игрок: {username}\n"
        f"🆔 ID: {user_id}\n\n"
        f"💰 Баланс: ${balance:,}\n"
        f"⭐ Уровень: {level}\n"
        f"✨ Опыт: {experience}/100",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="menu"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# БАЛАНС
# =========================

@dp.callback_query(lambda callback: callback.data == "balance")
async def balance(callback: CallbackQuery):

    player = get_player(
        callback.from_user.id
    )

    if not player:
        create_player(
            callback.from_user.id,
            callback.from_user.first_name
        )

        player = get_player(
            callback.from_user.id
        )

    money = player[2]

    await callback.message.edit_text(
        f"💰 <b>ТВОЙ БАЛАНС</b>\n\n"
        f"На счету:\n"
        f"💵 ${money:,}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="menu"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# БИЗНЕСЫ
# =========================

@dp.callback_query(lambda callback: callback.data == "businesses")
async def businesses(callback: CallbackQuery):

    await callback.message.edit_text(
        "🏢 <b>БИЗНЕСЫ</b>\n\n"
        "Пока у тебя нет бизнеса.\n\n"
        "Скоро здесь можно будет покупать:\n"
        "🏪 Магазины\n"
        "🍕 Рестораны\n"
        "⛽ Заправки\n"
        "🏭 Заводы",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="menu"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# ТРАНСПОРТ
# =========================

@dp.callback_query(lambda callback: callback.data == "cars")
async def cars(callback: CallbackQuery):

    await callback.message.edit_text(
        "🚗 <b>ТРАНСПОРТ</b>\n\n"
        "У тебя пока нет автомобилей.\n\n"
        "Автосалон скоро откроется.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="menu"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# НЕДВИЖИМОСТЬ
# =========================

@dp.callback_query(lambda callback: callback.data == "houses")
async def houses(callback: CallbackQuery):

    await callback.message.edit_text(
        "🏠 <b>НЕДВИЖИМОСТЬ</b>\n\n"
        "У тебя пока нет недвижимости.\n\n"
        "Скоро появятся квартиры, дома и другие объекты.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="menu"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# ЗАДАНИЯ
# =========================

@dp.callback_query(lambda callback: callback.data == "quests")
async def quests(callback: CallbackQuery):

    await callback.message.edit_text(
        "📋 <b>ЗАДАНИЯ</b>\n\n"
        "Сегодняшние задания:\n\n"
        "🔒 Пока нет доступных заданий.\n"
        "Система заданий скоро будет добавлена.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="menu"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# КЛАН
# =========================

@dp.callback_query(lambda callback: callback.data == "clan")
async def clan(callback: CallbackQuery):

    await callback.message.edit_text(
        "👥 <b>КЛАН</b>\n\n"
        "Ты пока не состоишь в клане.\n\n"
        "Позже здесь можно будет:\n"
        "⚔️ создавать кланы\n"
        "🏗️ улучшать базу\n"
        "🌍 захватывать территории\n"
        "⚔️ воевать с другими кланами",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="menu"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# НАЗАД В МЕНЮ
# =========================

@dp.callback_query(lambda callback: callback.data == "menu")
async def menu(callback: CallbackQuery):

    await callback.message.edit_text(
        "🎮 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
        "Выбирай действие:",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================
# ЗАПУСК
# =========================

async def on_startup():

    init_db()

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
    bot=bot
).register(
    app,
    path="/webhook"
)


setup_application(
    app,
    dp,
    bot=bot
)


web.run_app(
    app,
    host="0.0.0.0",
    port=PORT
)
