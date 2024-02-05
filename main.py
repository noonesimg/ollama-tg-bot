#!/usr/bin/python3
import os
from rich.traceback import install
install()

from telegram.ext import ApplicationBuilder

from handlers.start import start_handler
from handlers.message_handler import message_handler
from handlers.ollama_host import set_host_handler
from handlers.status import status_handler
from handlers.help import help_handler

import handlers.chat_id as chat_id
import handlers.models as models
import handlers.system as sys_prompt
import handlers.history as history


OLLAMA_BOT_TOKEN = os.environ.get("OLLAMA_BOT_TOKEN")
if OLLAMA_BOT_TOKEN is None:
    raise ValueError("OLLAMA_BOT_TOKEN env variable is not set")

if __name__ == "__main__":
    application = ApplicationBuilder().token(OLLAMA_BOT_TOKEN).build()

    application.add_handler(chat_id.filter_handler, group=-1)

    application.add_handlers([
        start_handler,
        help_handler,
        status_handler,

        chat_id.get_handler,
        history.reset_handler,
        
        models.list_models_handler,
        models.set_model_handler,
        
        sys_prompt.list_handler,
        sys_prompt.set_handler,
        sys_prompt.create_new_hanlder,
        sys_prompt.remove_handler,
        sys_prompt.on_remove_handler,
        set_host_handler,
        message_handler,
    ])

    application.run_polling()