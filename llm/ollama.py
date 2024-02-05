from ollama import Client
from langchain.llms.ollama import Ollama
from .chat_history import ChatHistory
import os

ollama_model = 'openhermes'
OLLAMA_HOST = os.environ.get('OLLAMA_BOT_BASE_URL')
if OLLAMA_HOST is None:
    raise ValueError("OLLAMA_BOT_BASE_URL env variable is not set")

default_system_prompt_path = './system/default.md'

def get_client(system=''):
    return Ollama(
        base_url=OLLAMA_HOST,
        model=ollama_model,
        system=system,
    )

def list_models_names():
    models = Client(OLLAMA_HOST).list()["models"]
    return [m['name'] for m in models]


PROMPT_TEMPLATE = """
{context}

{history}

User: {question}

Assistant:
"""

class OllamaClient:
    def __init__(self) -> None:
        with open(default_system_prompt_path) as file:
            self.system_prompt = file.read()

        self.client = get_client(self.system_prompt)
        self.history = ChatHistory()
    
    def generate(self, question) -> str:
        context_content = self.history.get_context(question)
        context = f"CONTEXT: {context_content}" if len(context_content) > 0 else ''

        last_few = self.history.get_last_few()
        history = f"LAST MESSAGES: {last_few}" if len(last_few) > 0 else ''

        prompt = PROMPT_TEMPLATE.format(
            context=context,
            history=history,
            question=question
        )

        answer = self.client.invoke(prompt)

        self.history.append(question, answer)
        return answer

    def reset_history(self):
        self.history.reset_history()
    
    def set_model(self, model_name):
        self.client.model = model_name

    def set_host(self, host):
        self.client.base_url = host

    def set_system(self, system):
        self.client.system = system

    def get_status(self):
        return (
            self.client.base_url, 
            self.client.model,
            self.client.system
        )
