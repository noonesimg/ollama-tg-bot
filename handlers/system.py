from llm import clinet
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler

import os

SYSTEM_DIR = 'system'

# list system prompts as inline keybard
# clicking a button sets system prompt for current model
async def list_system_prompts(update: Update, _):
    files = os.listdir(SYSTEM_DIR)

    keybaord = [[InlineKeyboardButton(name, callback_data=f'/setsystem {name}')] for name in files]
    reply_markup = InlineKeyboardMarkup(keybaord)

    await update.message.reply_text('select system prompt:', reply_markup=reply_markup)


list_handler = CommandHandler("systems", list_system_prompts)

async def on_set_system(update: Update, _):
    query = update.callback_query
    file_name = query.data.split(' ')[1] 
    await query.answer()

    file_path = os.path.join(SYSTEM_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path) as file:
            system_prompt = file.read()
            clinet.set_system(system_prompt)
            await query.edit_message_text(text=f"the system prompt has been set to: {file_name}\n\n{system_prompt}")

set_handler = CallbackQueryHandler(on_set_system, pattern='^/setsystem')

# list system prompts as buttons
# clicking on a button removes selected system prompt
async def remove_system_prompt(update: Update, _):
    files = os.listdir(SYSTEM_DIR)

    keybaord = [[InlineKeyboardButton(name, callback_data=f'/rmsystem {name}')] for name in files]
    reply_markup = InlineKeyboardMarkup(keybaord)

    await update.message.reply_text(
        '*WARNING:* selected prompt will be removed:', 
        reply_markup=reply_markup,
        parse_mode='markdown'
    )

remove_handler = CommandHandler("rmsystem", remove_system_prompt)

async def on_remove_system(update: Update, _):
    query = update.callback_query
    file_name = query.data.split(' ')[1] 
    await query.answer()

    file_path = os.path.join(SYSTEM_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path) as file:
            system_prompt = file.read()
            clinet.set_system(system_prompt)
            os.remove(file_path)
            await query.edit_message_text(text=f"{file_name} system prompt has been removed\n\n{system_prompt}")

on_remove_handler = CallbackQueryHandler(on_remove_system, pattern='^/rmsystem')

# Define states
SET_NAME, SET_CONTENT = range(2)

# add new system prompt
# 1. enter name
# 2. enter content
# new prompt will be saved to SYSTEM_DIR
async def add_system(update: Update, _):
    await update.message.reply_text(
        text="Enter name for a new system prompt:",
    )
    return SET_NAME

async def on_got_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_name = ''.join(x for x in update.message.text if x.isalnum() or x in '._ ')
    context.user_data['new_name'] = file_name

    if os.path.exists(os.path.join(SYSTEM_DIR, file_name)):
        await update.message.reply_text(
            text=f'*Warning*, existing **{file_name}** will be rewritten\nenter prompt content to continue or /cancel',
            parse_mode='markdown'
        )
    else:
        await update.message.reply_text(
            f"New system prompt will be saved to {file_name}, enter prompt:"
        )
    
    return SET_CONTENT

async def on_got_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_name = context.user_data['new_name']
    with open(os.path.join(SYSTEM_DIR, file_name), 'w') as file:
        file.write(update.message.text)
    
    await update.message.reply_text(f"{file_name} content saved")
    return ConversationHandler.END    

async def cancel(update: Update, _):
    await update.message.reply_text("canceled /addsystem command")
    return ConversationHandler.END

create_new_hanlder = ConversationHandler(
    entry_points=[CommandHandler('addsystem', add_system)],
    states={
        SET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, on_got_name)],
        SET_CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, on_got_content)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)