from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

class MistralAI:
    def __init__(self):
        Settings.llm = LlamaCPP(
            model_path='./data/models/Mistral-7B-Instruct-v0.3.Q2_K.gguf',
            temperature=0.1,
            max_new_tokens=2000,
            context_window=4096,
            model_kwargs={
                "n_threads": 8,
                "n_batch": 512
            },
            verbose=False # verbose=True завалит логами консоль при каждом токене
        )
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.chunk_size = 512

@property
def kg_index(self):
    if self._kg_index is None:
        try:
            gstorage_context = StorageContext.from_defaults(persist_dir='./data/storage_n4')
            self._kg_index = PropertyGraphIndex.from_existing(
                property_graph_store=self.graph_store
            )
        except Exception as e:
            print(f"Ошибка загрузки индекса: {e}")
            raise
    return self._kg_index

def query(self, query_str: str) -> str:
    if not self.kg_index:
        return "Индекс графа не инициализирован."
    
    query_engine = self.kg_index.as_query_engine(
        include_text=True,
        similarity_top_k=2
    )
    
    response = query_engine.query(query_str.strip())  
    return response.response