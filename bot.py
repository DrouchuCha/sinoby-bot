"""
SINOBY MediaPlanBot — Telegram Bot
====================================
Требования:
  pip install aiogram==3.x aiohttp python-dotenv

Запуск:
  python bot.py
"""

import asyncio
import json
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppData,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from dotenv import load_dotenv

load_dotenv()

# ══ НАСТРОЙКИ ══════════════════════════════════════════════
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL  = os.getenv("WEBAPP_URL", "https://drouchucha.github.io/sinoby-mediaplan/")

# ID менеджеров — сюда будут приходить уведомления о новых заявках
# Добавьте свой Telegram ID (узнать можно у @userinfobot)
MANAGER_IDS = [
    267728315,
]
# ═══════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher()


# ── /start ──────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(msg: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text="📋 Создать медиаплан",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    await msg.answer(
        "👋 Добро пожаловать в <b>SINOBY MediaPlanBot</b>\n\n"
        "Нажмите кнопку ниже чтобы создать медиаплан.\n"
        "Это займёт меньше минуты.",
        parse_mode="HTML",
        reply_markup=kb,
    )


# ── Получение данных из Mini App ────────────────────────────
@dp.message(F.web_app_data)
async def on_webapp_data(msg: Message):
    raw  = msg.web_app_data.data
    user = msg.from_user

    log.info(f"Получены данные от {user.id} (@{user.username}): {raw}")

    # Парсим JSON из мини-апп
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        await msg.answer("⚠️ Ошибка при получении данных. Попробуйте ещё раз.")
        return

    # ── Формируем красивое сообщение ──
    category  = data.get("category", "—")
    region    = data.get("region",   "—")
    district  = data.get("district", "—")
    city      = data.get("city",     "—")
    spec      = data.get("spec",     "—")
    goal      = data.get("goal",     "—")
    channel   = data.get("channel",  "—")
    channels  = data.get("channels", [])
    channel_str = ", ".join(channels) if channels else channel
    budget    = data.get("budget",   "—")
    calls     = data.get("forecast_calls")
    price     = data.get("forecast_price")
    ts        = data.get("ts", "")

    # Метка категории детализации
    spec_label = (
        "Бренд"      if category == "Авто" else
        "Категория"  if category == "Недвижимость" else
        "Направление"
    )

    # Время
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        time_str = dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        time_str = datetime.now().strftime("%d.%m.%Y %H:%M")

    # Прогноз (только для Авто)
    forecast_block = ""
    if calls and price:
        forecast_block = (
            f"\n📊 <b>Прогноз (Яндекс Директ)</b>\n"
            f"├ Звонков в месяц: <b>~{calls}</b>\n"
            f"└ Цена звонка: <b>~{price}</b>\n"
        )

    # Имя пользователя
    name = user.full_name or "—"
    username = f"@{user.username}" if user.username else f"ID:{user.id}"

    text = (
        f"📋 <b>Новый запрос на медиаплан</b>\n"
        f"{'─' * 28}\n"
        f"🏷 Сфера: <b>{category}</b>\n"
        f"📍 Регион: <b>{region} ({district})</b>\n"
        f"🏙 Город: <b>{city}</b>\n"
        f"🔖 {spec_label}: <b>{spec}</b>\n"
        f"🎯 Цель: <b>{goal}</b>\n"
        f"📡 Канал: <b>{channel_str}</b>\n"
        f"💰 Бюджет: <b>{budget}</b>\n"
        f"{forecast_block}"
        f"{'─' * 28}\n"
        f"👤 {name} · {username}\n"
        f"🕐 {time_str}"
    )

    # ── Отправляем пользователю подтверждение ──
    await msg.answer(
        f"✅ <b>Запрос принят!</b>\n\n"
        f"Наш менеджер свяжется с вами в ближайшее время.\n\n"
        f"<b>Ваши параметры:</b>\n"
        f"• Сфера: {category}\n"
        f"• Город: {city}\n"
        f"• {spec_label}: {spec}\n"
        f"• Бюджет: {budget}",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )

    # ── Уведомляем всех менеджеров ──
    for manager_id in MANAGER_IDS:
        try:
            await bot.send_message(
                chat_id=manager_id,
                text=text,
                parse_mode="HTML",
            )
            log.info(f"Уведомление отправлено менеджеру {manager_id}")
        except Exception as e:
            log.error(f"Не удалось отправить менеджеру {manager_id}: {e}")


# ── /help ────────────────────────────────────────────────────
@dp.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(
        "ℹ️ <b>SINOBY MediaPlanBot</b>\n\n"
        "Команды:\n"
        "/start — открыть квиз медиаплана\n"
        "/help  — справка\n\n"
        "По вопросам: @sinoby_manager",
        parse_mode="HTML",
    )


# ── Запуск ───────────────────────────────────────────────────
async def main():
    log.info("Бот запускается...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
