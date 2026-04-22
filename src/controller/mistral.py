import tempfile
import uuid
import os
import shutil

from llama_index.core import (
    PropertyGraphIndex, 
    StorageContext, 
    Settings
)
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.readers.file import PyMuPDFReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

PERSIST_DIR = './data/storage_n4'

class Mistral:
    def __init__(self, config):
        self.llm = LlamaCPP(
            model_path='./data/models/Mistral-7B-Instruct-v0.3.Q2_K.gguf',
            temperature=0.1,
            max_new_tokens=2000,
            context_window=4096,
            model_kwargs={
                "n_threads": 8,
                "n_batch": 512
            },
            verbose=True 
        )
        
        Settings.llm = self.llm
        Settings.embed_model = HuggingFaceEmbedding()
        Settings.chunk_size = 512

        self.graph_store = Neo4jPropertyGraphStore(
            username=config.get("NEO4J_USER", "neo4j"),
            password=config.get("NEO4J_PASSWORD", "password"),
            url=config.get("NEO4J_URI", "bolt://localhost:7687"),
            database=config.get("NEO4J_DATABASE", "neo4j"),
        )

        self._kg_index = None
        self.progress = {} 

    def update_progress(self, task_id: str, status: str, percent: int = 0, message: str = ""):
        self.progress[task_id] = {
            "task_id": task_id,
            "status": status,
            "percent": percent,
            "message": message,
        }

    def get_progress(self, task_id: str):
        return self.progress.get(task_id)

    @property
    def kg_index(self):
        if self._kg_index is None:
            try:
                gstorage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
                self._kg_index = PropertyGraphIndex.from_existing(
                    property_graph_store=self.graph_store
                )
            except Exception as e:
                print(f"Индекс еще не создан: {e}")
                self._kg_index = None
        return self._kg_index

    @kg_index.setter
    def kg_index(self, new_index):
        self._kg_index = new_index

    def query(self, query_str: str) -> dict:
        index = self.kg_index
        if not index:
            return {"answer": "Ошибка: База знаний пуста.", "sources": []}
        
        query_engine = index.as_query_engine(
            include_text=True,
            similarity_top_k=5
        )
        
        response = query_engine.query(query_str.strip())  
        
        sources = []
        for node_with_score in response.source_nodes:
            node = node_with_score.node
            
            source_info = {
                "score": node_with_score.score,       
                "text": node.text,                            
            }
            sources.append(source_info)

        return {
            "answer": response.response,
            "sources": sources 
        }

    def build_knowledge_graph(self, content: bytes, filename: str, task_id: str = None):
        if task_id is None:
            task_id = str(uuid.uuid4())

        self.update_progress(task_id, status="started", percent=5, message="Подготовка файла")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            self.update_progress(task_id, status="reading", percent=20, message="Чтение документа")
            
            """documents = SimpleDirectoryReader(
                input_files=[tmp_path] 
            ).load_data()"""
            loader = PyMuPDFReader()
            documents = loader.load_data(file_path=tmp_path)

            if not documents:
                raise ValueError("Не удалось извлечь текст из PDF.")

            self.update_progress(task_id, status="indexing", percent=50, message="Генерация графа")

            gstorage_context = StorageContext.from_defaults(graph_store=self.graph_store)

            self.kg_index = PropertyGraphIndex.from_documents(
                documents,
                storage_context=gstorage_context,
                max_triplets_per_chunk=10,
                include_embeddings=True,
                property_graph_store=self.graph_store,
            )

            if not os.path.exists(PERSIST_DIR):
                os.makedirs(PERSIST_DIR)
            gstorage_context.persist(persist_dir=PERSIST_DIR)

            self.update_progress(task_id, status="completed", percent=100, message="Успешно завершено")
            
        except Exception as e:
            self.update_progress(task_id, status="failed", percent=100, message=str(e))
            raise
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def clear_neo4j_database(self):
        try:
            cypher_query = "MATCH (n) DETACH DELETE n"
            
            if hasattr(self.graph_store, 'query'):
                self.graph_store.query(cypher_query)
            elif hasattr(self.graph_store, 'structured_query'):
                self.graph_store.structured_query(cypher_query)
            else:
                with self.graph_store._driver.session(database=self.graph_store._database) as session:
                    session.run(cypher_query)
            
            self._kg_index = None
            print("База данных Neo4j успешно полностью очищена.")
        except Exception as e:
            print(f"Ошибка при очистке базы данных Neo4j: {e}")
    
    def clear_all_data(self):
        self.clear_neo4j_database()
        if os.path.exists(PERSIST_DIR):
            try:
                shutil.rmtree(PERSIST_DIR)
                print(f"Локальная директория {PERSIST_DIR} удалена.")
            except Exception as e:
                print(f"Ошибка при удалении {PERSIST_DIR}: {e}")