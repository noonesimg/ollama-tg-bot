FROM python:3.10.13-slim-bookworm

WORKDIR /usr/src/ollama-tg-bot

# install dependencies
COPY requirements.txt /usr/src/ollama-tg-bot/
RUN pip install --no-cache-dir -r requirements.txt

# prefetch embeddings model
RUN pip install -U "huggingface_hub[cli]"
RUN huggingface-cli download BAAI/bge-base-en

COPY main.py /usr/src/ollama-tg-bot/
COPY handlers /usr/src/ollama-tg-bot/handlers
COPY llm /usr/src/ollama-tg-bot/llm
COPY system /usr/src/ollama-tg-bot/system

ENV OLLAMA_BOT_TOKEN ${OLLAMA_BOT_TOKEN}
ENV OLLAMA_BOT_CHAT_IDS ${OLLAMA_BOT_CHAT_IDS}
ENV OLLAMA_BOT_BASE_URL ${OLLAMA_BOT_BASE_URL}

CMD python3 ./main.py