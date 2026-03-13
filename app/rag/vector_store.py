"""向量存储 - ChromaDB 连接、存入、检索

面试考点：
- Embedding 用 bge-small-zh，中文效果最好且免费
- ChromaDB 零配置本地运行，适合入门项目
- 检索 Top-K 条最相似的文档，K 通常设 3-5
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from app.config import get_settings

# 全局变量，延迟加载
_embedding_model: SentenceTransformer | None = None
_chroma_client: chromadb.ClientAPI | None = None


def get_embedding_model() -> SentenceTransformer:
    """获取 Embedding 模型单例"""
    global _embedding_model
    if _embedding_model is None:
        settings = get_settings()
        print(f"🔄 正在加载 Embedding 模型: {settings.embedding_model}...")
        _embedding_model = SentenceTransformer(settings.embedding_model)
        print("✅ Embedding 模型加载完成")
    return _embedding_model


def get_chroma_client() -> chromadb.ClientAPI:
    """获取 ChromaDB 客户端单例"""
    global _chroma_client
    if _chroma_client is None:
        settings = get_settings()
        _chroma_client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        print(f"✅ ChromaDB 已连接: {settings.chroma_persist_dir}")
    return _chroma_client


class VectorStore:
    """向量存储：封装 ChromaDB 的存入和检索操作"""

    def __init__(self):
        settings = get_settings()
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"},  # 使用余弦相似度
        )
        self.model = get_embedding_model()

    def add_documents(self, texts: list[str], metadatas: list[dict]) -> int:
        """
        将文本块向量化并存入 ChromaDB

        Args:
            texts: 文本块列表
            metadatas: 元数据列表

        Returns:
            存入的文档数量
        """
        if not texts:
            return 0

        # 生成向量
        embeddings = self.model.encode(texts).tolist()

        # 生成唯一 ID
        existing_count = self.collection.count()
        ids = [f"doc_{existing_count + i}" for i in range(len(texts))]

        # 存入 ChromaDB
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

        print(f"✅ 已存入 {len(texts)} 个文档块到向量库")
        return len(texts)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        语义检索：将用户问题向量化，在 ChromaDB 中找最相似的文档块

        Args:
            query: 用户查询
            top_k: 返回前 K 条结果

        Returns:
            检索结果列表，每项包含 text, metadata, distance
        """
        # 将查询向量化
        query_embedding = self.model.encode([query]).tolist()

        # 在 ChromaDB 中检索
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        # 整理结果
        search_results = []
        if results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                search_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                })

        return search_results

    def get_doc_count(self) -> int:
        """获取当前向量库中的文档数量"""
        return self.collection.count()

    def clear(self):
        """清空向量库"""
        settings = get_settings()
        self.client.delete_collection(settings.chroma_collection_name)
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        print("🗑️ 向量库已清空")
