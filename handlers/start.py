from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler

async def start(update: Update, _): 
    await update.message.reply_text(
        "Ask a question to start conversation",
    )
    keyboard = [
        ['/status'],
        ['/models'],
        ['/systems'],
        ['/reset']
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        one_time_keyboard=True, 
        resize_keyboard=True
    )
    await update.message.reply_text(
        "You can also use this commands:",
        reply_markup=reply_markup
    )

start_handler = CommandHandler("start", start)