"""
🌸 Бот Принятия Даров — Telegram Bot
Команды: /start /gift /me /universe /journal /stats
"""

import os
import json
import random
from datetime import date
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)

# ─── ТОКЕН ───────────────────────────────────────────────────────────────────
TOKEN = os.environ.get("BOT_TOKEN", "ВАШ_ТОКЕН_ЗДЕСЬ")

# ─── ДАННЫЕ ──────────────────────────────────────────────────────────────────
GIFTS = [
    ("🌸", "Ты заслуживаешь всего самого прекрасного в этом мире."),
    ("✨", "Твоя чуткость — это настоящий дар для всех вокруг."),
    ("🌙", "Ты красива — не потому что стараешься, а просто потому что ты есть."),
    ("💛", "Мир стал богаче в тот день, когда ты появилась."),
    ("🌿", "Принять заботу — такая же смелость, как и давать её."),
    ("🕊️", "Ты достойна покоя. Просто так. Без условий."),
    ("💎", "Твои слабости — часть твоей красоты, не её противоположность."),
    ("🌺", "Кто-то прямо сейчас думает о тебе с теплом и улыбкой."),
    ("🫂", "Позволь этому объятию дойти до тебя. Ты в безопасности."),
    ("🌊", "Тебе не нужно ничего делать, чтобы быть любимой."),
    ("🍯", "Вся нежность, которую ты отдаёшь другим — ты тоже достойна её."),
    ("🌟", "Твоё присутствие — это уже подарок для тех, кто рядом."),
    ("🦋", "Ты уже достаточно. Прямо сейчас. Именно такая."),
    ("🌈", "Позволь себе получать столько же, сколько ты даёшь."),
    ("🫶", "Ты умеешь любить — и ты достойна такой же любви к себе."),
]

RESPONSES = [
    "Принято с любовью 💛",
    "Ты это заслуживаешь 🌸",
    "Твоё сердце открывается ✨",
    "Принято. Ты молодец 🌿",
    "Дар получен 🕊️",
    "Это твоё. По праву. 💎",
]

SELF_PROMPTS = [
    "За что ты сегодня благодарна себе?",
    "Что ты сделала хорошо сегодня?",
    "Чем ты гордишься в себе прямо сейчас?",
    "Какое качество в себе ты ценишь?",
    "Как ты позаботилась о себе сегодня?",
    "За какой свой поступок ты хочешь себя похвалить?",
]

UNIVERSE_PROMPTS = [
    "Какой дар ты получила от мира сегодня?",
    "Что красивого ты заметила сегодня?",
    "Какая маленькая радость случилась сегодня?",
    "Что поддержало тебя сегодня?",
    "Какое совпадение или знак ты заметила?",
    "За что ты благодарна жизни прямо сейчас?",
]

ENCOURAGEMENTS = [
    "Принимать — это навык. Ты его развиваешь прямо сейчас.",
    "Каждый раз, когда ты принимаешь — ты говоришь себе «я достойна».",
    "Замечаешь, как сердце чуть теплее?",
    "Ты делаешь что-то важное для себя.",
    "Любовь к себе начинается с маленьких «принимаю».",
]

# ─── СОСТОЯНИЯ ДИАЛОГА ───────────────────────────────────────────────────────
WAITING_ACCEPT = 1
WAITING_SELF   = 2
WAITING_UNIV   = 3

# ─── ХРАНИЛИЩЕ ДАННЫХ (JSON-файл) ────────────────────────────────────────────
DATA_FILE = "data.json"

def load_db() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_db(db: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(db: dict, uid: int) -> dict:
    key = str(uid)
    if key not in db:
        db[key] = {"streak": 0, "self": {}, "universe": {}}
    return db[key]

def today_str() -> str:
    return date.today().isoformat()

# ─── КЛАВИАТУРА ──────────────────────────────────────────────────────────────
def main_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🌸 Получить дар"),   KeyboardButton("💛 Благодарность себе")],
        [KeyboardButton("🌿 Дар Вселенной"),  KeyboardButton("📖 Мой дневник")],
        [KeyboardButton("✨ Статистика")],
    ], resize_keyboard=True)

def accept_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🙏 Принимаю")],
        [KeyboardButton("💛 Принимаю с благодарностью")],
        [KeyboardButton("✨ Да, это моё")],
    ], resize_keyboard=True)

# ─── ХЭНДЛЕРЫ ────────────────────────────────────────────────────────────────

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌸 *Привет, дорогая!*\n\n"
        "Я — твой бот практики принятия и любви к себе.\n\n"
        "Здесь ты можешь:\n"
        "• Принимать дары и комплименты\n"
        "• Записывать благодарности себе\n"
        "• Замечать дары от Вселенной\n"
        "• Читать свой дневник\n\n"
        "_Начни с получения первого дара_ 🌸",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

async def send_gift(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    emoji, text = random.choice(GIFTS)
    await update.message.reply_text(
        f"{emoji} _{text}_\n\n"
        f"Просто прими это. Ты достойна.",
        parse_mode="Markdown",
        reply_markup=accept_keyboard()
    )
    return WAITING_ACCEPT

async def handle_accept(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    user = get_user(db, update.effective_user.id)
    user["streak"] = user.get("streak", 0) + 1
    save_db(db)

    streak = user["streak"]
    response = random.choice(RESPONSES)
    text = f"{response}\n\n"

    if streak % 5 == 0:
        text += f"🌟 *{streak} принятий!*\n_{random.choice(ENCOURAGEMENTS)}_"
    elif streak % 3 == 0:
        text += f"_{random.choice(ENCOURAGEMENTS)}_"

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard())
    return ConversationHandler.END

async def ask_self(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    prompt = random.choice(SELF_PROMPTS)
    db = load_db()
    user = get_user(db, update.effective_user.id)
    today = today_str()
    count = len(user["self"].get(today, []))

    status = f"Сегодня уже записано: {count} {'✦' * min(count,3)}\n\n" if count > 0 else ""

    await update.message.reply_text(
        f"💛 *Благодарность себе*\n\n"
        f"{status}"
        f"_{prompt}_\n\n"
        f"Напиши свой ответ 👇",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("← Назад")]], resize_keyboard=True)
    )
    return WAITING_SELF

async def save_self(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "← Назад":
        await update.message.reply_text("Хорошо 🌸", reply_markup=main_keyboard())
        return ConversationHandler.END

    db = load_db()
    user = get_user(db, update.effective_user.id)
    today = today_str()
    if today not in user["self"]:
        user["self"][today] = []
    user["self"][today].append(text)
    save_db(db)

    count = len(user["self"][today])
    dots = "✦" * min(count, 3) + "○" * max(0, 3 - count)

    msg = f"💛 Записано!\n\n_{text}_\n\n{dots}"
    if count >= 3:
        msg += "\n\n🌟 *Три благодарности записаны!*\nТы заботишься о себе — это важно."

    await update.message.reply_text(
        msg, parse_mode="Markdown",
        reply_markup=main_keyboard() if count >= 3 else
        ReplyKeyboardMarkup([[KeyboardButton("💛 Добавить ещё")],[KeyboardButton("← Назад")]], resize_keyboard=True)
    )
    return WAITING_SELF if count < 10 else ConversationHandler.END

async def ask_universe(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    prompt = random.choice(UNIVERSE_PROMPTS)
    db = load_db()
    user = get_user(db, update.effective_user.id)
    today = today_str()
    count = len(user["universe"].get(today, []))
    status = f"Сегодня замечено даров: {count} {'✦' * min(count,3)}\n\n" if count > 0 else ""

    await update.message.reply_text(
        f"🌿 *Дары Вселенной*\n\n"
        f"{status}"
        f"_{prompt}_\n\n"
        f"Напиши свой ответ 👇",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("← Назад")]], resize_keyboard=True)
    )
    return WAITING_UNIV

async def save_universe(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "← Назад":
        await update.message.reply_text("Хорошо 🌸", reply_markup=main_keyboard())
        return ConversationHandler.END

    db = load_db()
    user = get_user(db, update.effective_user.id)
    today = today_str()
    if today not in user["universe"]:
        user["universe"][today] = []
    user["universe"][today].append(text)
    save_db(db)

    count = len(user["universe"][today])
    dots = "✦" * min(count, 3) + "○" * max(0, 3 - count)
    msg = f"🌿 Записано!\n\n_{text}_\n\n{dots}"
    if count >= 3:
        msg += "\n\n🌟 *Три дара замечены!*\nМир заботится о тебе — и ты это видишь."

    await update.message.reply_text(
        msg, parse_mode="Markdown",
        reply_markup=main_keyboard() if count >= 3 else
        ReplyKeyboardMarkup([[KeyboardButton("🌿 Добавить ещё")],[KeyboardButton("← Назад")]], resize_keyboard=True)
    )
    return WAITING_UNIV if count < 10 else ConversationHandler.END

async def show_journal(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    user = get_user(db, update.effective_user.id)

    self_data = user.get("self", {})
    univ_data = user.get("universe", {})

    all_dates = sorted(set(list(self_data.keys()) + list(univ_data.keys())), reverse=True)[:7]

    if not all_dates:
        await update.message.reply_text(
            "📖 Дневник пока пуст.\n\nНачни записывать благодарности себе и замечать дары Вселенной 🌸",
            reply_markup=main_keyboard()
        )
        return

    lines = ["📖 *Твой дневник* (последние 7 дней)\n"]
    for d in all_dates:
        lines.append(f"━━━ {d} ━━━")
        if d in self_data and self_data[d]:
            lines.append("💛 *Себе:*")
            for item in self_data[d]:
                lines.append(f"  · {item}")
        if d in univ_data and univ_data[d]:
            lines.append("🌿 *Вселенной:*")
            for item in univ_data[d]:
                lines.append(f"  · {item}")
        lines.append("")

    await update.message.reply_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

async def show_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    user = get_user(db, update.effective_user.id)

    streak = user.get("streak", 0)
    self_total = sum(len(v) for v in user.get("self", {}).values())
    univ_total = sum(len(v) for v in user.get("universe", {}).values())
    self_days  = len(user.get("self", {}))
    univ_days  = len(user.get("universe", {}))

    today = today_str()
    self_today = len(user.get("self", {}).get(today, []))
    univ_today = len(user.get("universe", {}).get(today, []))

    await update.message.reply_text(
        f"✨ *Твоя практика*\n\n"
        f"🌸 Принятий даров: *{streak}*\n\n"
        f"💛 Благодарностей себе:\n"
        f"  · Всего: *{self_total}* за *{self_days}* дн.\n"
        f"  · Сегодня: *{self_today}/3* {'✦'*min(self_today,3)}\n\n"
        f"🌿 Даров Вселенной:\n"
        f"  · Всего: *{univ_total}* за *{univ_days}* дн.\n"
        f"  · Сегодня: *{univ_today}/3* {'✦'*min(univ_today,3)}\n\n"
        f"_Ты растёшь. Каждый день._",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

async def fallback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "принима" in text.lower() or "спасибо" in text.lower() or "благодар" in text.lower():
        await update.message.reply_text(random.choice(RESPONSES), reply_markup=main_keyboard())
    else:
        await update.message.reply_text("🌸 Используй кнопки меню или /start", reply_markup=main_keyboard())

# ─── ЗАПУСК ──────────────────────────────────────────────────────────────────

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    gift_conv = ConversationHandler(
        entry_points=[
            CommandHandler("gift", send_gift),
            MessageHandler(filters.Regex("^🌸 Получить дар$"), send_gift),
        ],
        states={
            WAITING_ACCEPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_accept)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    self_conv = ConversationHandler(
        entry_points=[
            CommandHandler("me", ask_self),
            MessageHandler(filters.Regex("^💛"), ask_self),
        ],
        states={
            WAITING_SELF: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_self)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    univ_conv = ConversationHandler(
        entry_points=[
            CommandHandler("universe", ask_universe),
            MessageHandler(filters.Regex("^🌿"), ask_universe),
        ],
        states={
            WAITING_UNIV: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_universe)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("journal", show_journal))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(MessageHandler(filters.Regex("^📖"), show_journal))
    app.add_handler(MessageHandler(filters.Regex("^✨ Стат"), show_stats))
    app.add_handler(gift_conv)
    app.add_handler(self_conv)
    app.add_handler(univ_conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    print("🌸 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
