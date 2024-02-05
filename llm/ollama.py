from ollama import Client
from langchain.llms.ollama import Ollama
from .chat_history import ChatHistory

ollama_model = 'openhermes'
ollama_host = 'http://10.8.0.100:11435'

default_system_prompt_path = './system/default.md'

def get_client(system=''):
    return Ollama(
        base_url=ollama_host,
        model=ollama_model,
        system=system,
    )

def list_models_names():
    models = Client(ollama_host).list()["models"]
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

    def set_system(self, system):
        self.client.system = system
