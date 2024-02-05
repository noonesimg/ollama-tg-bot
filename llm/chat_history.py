from langchain.vectorstores.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from chromadb.config import Settings
import os

message_template = """
User: {question}

Assistant: {answer}
"""

model_norm = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-base-en",
    model_kwargs={ 'device': 'cpu' },
    encode_kwargs={ 'normalize_embeddings': True },
)

def get_chroma():
    settings = Settings()
    settings.allow_reset = True
    settings.is_persistent = True

    return Chroma(
        persist_directory=DB_FOLDER,
        embedding_function=model_norm,
        client_settings=settings,
        collection_name='latest_chat'
    )

DB_FOLDER = 'db'

class ChatHistory:
    def __init__(self) -> None:
        self.history = []

    def append(self, question: str, answer: str):
        new_message = message_template.format(
            question=question,
            answer=answer
        )
        self.history.append(new_message)
        self.embed(new_message)

    def reset_history(self):
        self.history = []
        chroma = get_chroma()
        chroma._client.reset()
    
    def embed(self, text: str):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        all_splits = text_splitter.split_text(text)
        
        chroma = get_chroma()
        chroma.add_texts(all_splits)

    def get_context(self, question: str):
        if not os.path.exists(DB_FOLDER):
            return ''
        chroma = get_chroma()
        documents = chroma.similarity_search(query=question, k=4)
        context = '\n'.join([d.page_content for d in documents])
        return context
    
    def get_last_few(self):
        return '\n'.join(self.history[-3:])