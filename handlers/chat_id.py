import os
from telegram import Update
from telegram.ext import CommandHandler, ApplicationHandlerStop, TypeHandler

chat_ids = os.environ.get("BOT_CHAT_IDS")
valid_user_ids = []
if chat_ids is not None:
    valid_user_ids = [int(id) for id in chat_ids.split(',')]


async def get_chat_id(update: Update, _):
    chat_id = update.effective_chat.id
    await update.message.reply_text(chat_id)

get_handler = CommandHandler("chatid", get_chat_id)

async def filter_chat_id(update: Update, _):
    if update.effective_user.id in valid_user_ids:
        pass
    else:
        await update.effective_message.reply_text("access denied")
        print(f"access denied for {update.effective_user.id} {update.effective_user.name} {update.effective_user.full_name}")
        raise ApplicationHandlerStop()

filter_handler = TypeHandler(Update, filter_chat_id)