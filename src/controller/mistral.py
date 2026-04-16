import io

from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.readers.file import PyMuPDFReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from dotenv import load_dotenv

class Mistral:
    def __init__(self, config):
        Settings.llm = LlamaCPP(
            model_path='./data/models/Mistral-7B-Instruct-v0.3.Q2_K.gguf',
            temperature=0.1,
            max_new_tokens=2000,
            context_window=4096,
            model_kwargs={
                "n_threads": 8,
                "n_batch": 512
            },
            verbose=False 
        )
        Settings.embed_model = HuggingFaceEmbedding()
        Settings.chunk_size = 512

        self.graph_store = Neo4jPropertyGraphStore(
            username=config.get("NEO4J_USER"),
            password=config.get("NEO4J_PASSWORD"),
            url=config.get("NEO4J_URI"),
            database=config.get("NEO4J_DATABASE"),
        )

        self._kg_index = None

    @property
    def kg_index(self):
        if self._kg_index is None:
            try:
                gstorage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
                self._kg_index = PropertyGraphIndex.from_existing(
                    property_graph_store=self.graph_store,
                    storage_context=gstorage_context
                )
            except Exception as e:
                print(f"Ошибка загрузки индекса: {e}")
                raise
        return self._kg_index

    @kg_index.setter
    def kg_index(self, new_index):
        if not isinstance(new_index, PropertyGraphIndex) and new_index is not None:
            raise TypeError("Объект должен быть экземпляром PropertyGraphIndex")
        self._kg_index = new_index

    def query(self, query_str: str) -> str:
        if not self.kg_index:
            return
        
        query_engine = self.kg_index.as_query_engine(
            include_text=True,
            similarity_top_k=2
        )
        
        response = query_engine.query(query_str.strip())  
        return response.response

    def build_knowledge_graph(self, content: bytes, filename: str):
        gstorage_context = StorageContext.from_defaults(graph_store=self.graph_store)

        fb = io.BytesIO(content)
        reader = PyMuPDFReader()
        documents = reader.load_data(file=fb, extra_info={"file_name": file_name})

        self.kg_index = PropertyGraphIndex.from_documents(
            documents,
            storage_context=gstorage_context,
            max_triplets_per_chunk=10,
            include_embeddings=True,
            property_graph_store=self.graph_store,
        )

        gstorage_context.persist(persist_dir=PERSIST_DIR)