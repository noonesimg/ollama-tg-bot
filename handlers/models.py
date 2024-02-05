from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
from llm import clinet
from llm.ollama import list_models_names

async def list_models(update: Update, _):
    model_names = list_models_names()
    keybaord = [[InlineKeyboardButton(name, callback_data=f'/setmodel {name}')] for name in model_names]
    reply_markup = InlineKeyboardMarkup(keybaord)

    await update.message.reply_text('!! chat history will be reset !!\nPick a model:', reply_markup=reply_markup)

list_models_handler = CommandHandler("models", list_models)

async def set_model(update: Update, _):
    query = update.callback_query
    model_name = query.data.split(' ')[1] 
    await query.answer()

    clinet.set_model(model_name)
    clinet.reset_history()
    await query.edit_message_text(text=f"selected model: {model_name}")

set_model_handler = CallbackQueryHandler(set_model, pattern='^/setmodel')