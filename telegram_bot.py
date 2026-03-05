import os
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

import bot_core

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    print("TELEGRAM_TOKEN not set", file=sys.stderr)
    sys.exit(1)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    reply = bot_core.chat(user_id, text)
    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Telegram bot started")
    app.run_polling()
