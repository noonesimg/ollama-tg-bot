from telegram import Update
from telegram.ext import CommandHandler
from llm import clinet

async def history_reset(update: Update, _):
    clinet.reset_history()
    await update.message.reply_text("history cleared")

reset_handler = CommandHandler("reset", history_reset)