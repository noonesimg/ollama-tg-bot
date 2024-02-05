# ollama-tg-bot

A simple telegram bot that allows you to talk with your local ollama models

A word of caution:

`this is something hacked together in a couple of evenings for fun, may contain bugs`

The bot doesn't handle multiple users at least for now.

## Features
1. chat history: stores last four entries directly and uses RAG to pull out context from previous conversation (workaround for small context windows)
2. history can be reset using */reset* command
2. switch between downloaded ollama models
3. edit system prompt, store multiple system prompts, switch between them as you need
4. switch between ollama hosts (in case you have more than one)

## Defaults 
Bot uses [BAAI/bge-base-en](https://huggingface.co/BAAI/bge-base-en) to save embeddings

Default ollama model is [openhermes](https://ollama.ai/library/openhermes) 

After comparing a bunch of different models this one seems to be the most flexible, while being fast enough to run on older hardware
Huge shout-out to [@teknium1](https://github.com/teknium1)

## Running
Bot relies on several env variables to be set:

```bash
OLLAMA_BOT_TOKEN=<your-telegram-bot-token>

# can be aquired by running /chatid command
# this assures that no one else can use your bot
OLLAMA_BOT_CHAT_IDS=<you-telegram-bot-chatid> 

# if you're running ollama and this bot locally
# the url is probably http://127.0.0.1:11434
OLLAMA_BOT_BASE_URL=<URL-to-your-ollama-host>
```

### Using a venv
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 ./main.py
```

### Using docker
```bash
# build the image (takes several minutes)
docker build -t ollama-tg-bot .
# run
docker-compose up 
```
