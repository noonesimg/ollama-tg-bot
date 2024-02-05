from telegram import Update
from telegram.ext import CommandHandler

help_message="""Welcome to ollama bot here's full list of commands

*Here's a full list of commands:*
/start - quick access to common commands
/status - show current bot status
/chatid - get current chat id
/models - select ollama model to chat with
/systems - select system prompt
/addsystem - create new system prompt
/rmsystem - remove system prompt
/sethost - set ollama host URL
/reset - reset chat history
/help - show this help message
"""

async def help(update: Update, _):
    await update.message.reply_text(help_message, parse_mode='markdown')

help_handler = CommandHandler("help", help)
