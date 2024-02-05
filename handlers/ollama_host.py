from telegram import Update
from telegram.ext import filters, CommandHandler, ConversationHandler, MessageHandler
from ollama import Client
from llm import clinet
# Define states
SET_HOST = range(1)

async def set_llama_host(update: Update, _):
    await update.message.reply_text(
        text='Enter ollama host url like, **http://127.0.0.1:11434**',
        parse_mode='markdown'
    )
    return SET_HOST


async def on_got_host(update: Update, _):
    test_client = Client(
        base_url=update.message.text
    )
    try:
        test_client.list()
        clinet.set_host(update.message.text)
        await update.message.reply_text(
            f"ollama host is set to: {update.message.text}"
        )
    except:
        await update.message.reply_text(
            f"couldn't connect to ollama server at:\n{update.message.text}"
        )
    finally:
        return ConversationHandler.END
    
async def cancel(update: Update, _):
    await update.message.reply_text("canceled /sethost command")
    return ConversationHandler.END

set_host_handler = ConversationHandler(
    entry_points=[CommandHandler("sethost", set_llama_host)],
    states={
        SET_HOST: [MessageHandler(filters.TEXT & ~filters.COMMAND, on_got_host)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)