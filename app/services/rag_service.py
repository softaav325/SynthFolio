import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List

class RAGService:
    def __init__(self, knowledge_dir='app/knowledge', model_name='all-MiniLM-L6-v2'):
        self.knowledge_dir = knowledge_dir
        # Модель all-MiniLM-L6-v2 легкая, быстрая и отлично подходит для коротких текстов/вопросов
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self._initialize_index()

    def _initialize_index(self):
        """Загружает md-файлы, разбивает их на чанки и строит FAISS индекс."""
        self.chunks = []
        if not os.path.exists(self.knowledge_dir):
            return

        for filename in os.listdir(self.knowledge_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(self.knowledge_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    # Чанкинг по двойному переносу строки (абзацы)
                    # Это сохраняет логическую целостность блоков информации из Markdown
                    paragraphs = text.split('\n\n')
                    for p in paragraphs:
                        if p.strip():
                            self.chunks.append(p.strip())

        if not self.chunks:
            return

        # Генерация эмбеддингов для всех чанков
        embeddings = self.model.encode(self.chunks)
        dimension = embeddings.shape[1]
        
        # IndexFlatL2 реализует поиск по L2-расстоянию (Евклидово расстояние)
        # Для нормализованных векторов это эквивалентно косинусному сходству
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))

    def get_relevant_context(self, query: str, k: int = 3) -> str:
        """Возвращает k самых релевантных фрагментов текста из базы знаний."""
        if not self.index or not self.chunks:
            return ""

        # Векторизация запроса пользователя
        query_vector = self.model.encode([query]).astype('float32')
        
        # Поиск ближайших соседей в векторе
        distances, indices = self.index.search(query_vector, k)
        
        # Сбор текстов соответствующих индексов
        results = [self.chunks[idx] for idx in indices[0] if idx != -1 and idx < len(self.chunks)]
        return "\n\n---\n\n".join(results)

# Создаем экземпляр сервиса как синглтон для всего приложения
rag_service = RAGService()
