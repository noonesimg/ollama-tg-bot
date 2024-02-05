from telegram import Update
from telegram.ext import MessageHandler, filters
from llm import clinet
import re

# simple filter for proper markdown response
def escape_markdown_except_code_blocks(text):
    # Pattern to match text outside of code blocks and inline code
    pattern = r'(```.*?```|`.*?`)|(_)'
    
    def replace(match):
        # If group 1 (code blocks or inline code) is matched, return it unaltered
        if match.group(1):
            return match.group(1)
        # If group 2 (underscore) is matched, escape it
        elif match.group(2):
            return r'\_'
    
    return re.sub(pattern, replace, text, flags=re.DOTALL)



async def on_message(update: Update, _):
    msg = await update.message.reply_text("...")
    await update.effective_chat.send_action("TYPING")
    try:
        response = clinet.generate(update.message.text)
        try:
            await msg.edit_text(
                escape_markdown_except_code_blocks(response),
                parse_mode='markdown'
            )
        except Exception as e:
            print(e)
            await msg.edit_text(response)
    except:
        await msg.edit_text("failed to generate response")

    await update.effective_chat.send_action("CANCEL")

message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), on_message)

