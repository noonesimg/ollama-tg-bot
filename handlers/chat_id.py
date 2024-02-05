import os
from telegram import Update
from telegram.ext import CommandHandler, ApplicationHandlerStop, TypeHandler

CHAT_IDS = os.environ.get("OLLAMA_BOT_CHAT_IDS")
valid_user_ids = []
if CHAT_IDS is not None:
    valid_user_ids = [int(id) for id in CHAT_IDS.split(',')]


async def get_chat_id(update: Update, _):
    chat_id = update.effective_chat.id
    await update.message.reply_text(chat_id)

get_handler = CommandHandler("chatid", get_chat_id)

async def filter_chat_id(update: Update, _):
    if update.effective_user.id in valid_user_ids or update.message.text == '/chatid':
        pass
    else:
        await update.effective_message.reply_text("access denied")
        print(f"access denied for {update.effective_user.id} {update.effective_user.name} {update.effective_user.full_name}")
        raise ApplicationHandlerStop()

filter_handler = TypeHandler(Update, filter_chat_id)