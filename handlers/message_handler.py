from telegram import Update
from telegram.ext import MessageHandler, filters

from llm import clinet

async def on_message(update: Update, _):
    msg = await update.message.reply_text("...")
    await update.effective_chat.send_action("TYPING")
    try:
        response = clinet.generate(update.message.text)
        try:
            await msg.edit_text(
                response,
                parse_mode='markdown'
            )
        except:
            await msg.edit_text(response)
    except:
        msg.edit_text("failed to generate response")
        
    await update.effective_chat.send_action("CANCEL")

message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), on_message)

