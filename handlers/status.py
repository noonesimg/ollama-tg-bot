from telegram import Update
from telegram.ext import CommandHandler
from llm import clinet

async def get_status(update: Update, _):
    host, model, system = clinet.get_status()

    await update.message.reply_text(
        text=f'*ollama_host:* {host}\n\n*model:* {model}\n\n*system prompt:*\n{system}',
        parse_mode='markdown'
    )

status_handler = CommandHandler("status", get_status)