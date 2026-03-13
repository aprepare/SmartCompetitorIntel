"""FastAPI 主入口 - 竞品情报分析与智能问答系统

API 端点：
- POST /api/v1/chat          智能对话（RAG + SSE 流式）
- POST /api/v1/crawl         手动触发采集（当前用模拟数据）
- GET  /api/v1/knowledge/stats 知识库状态
- POST /api/v1/knowledge/clear 清空知识库
- GET  /health               健康检查
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import json

from app.config import get_settings
from app.models.schemas import ChatRequest, CrawlRequest
from app.rag.document_processor import DocumentProcessor
from app.rag.vector_store import VectorStore
from app.services.llm_service import chat_with_rag
from app.crawler.mock_data import generate_mock_data


# ============ 全局实例 ============
doc_processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
vector_store: VectorStore | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动时初始化向量库"""
    global vector_store
    print("🚀 正在启动竞品分析系统...")
    vector_store = VectorStore()
    print(f"📊 知识库中现有 {vector_store.get_doc_count()} 个文档块")
    yield
    print("👋 系统关闭")


# ============ 创建 FastAPI 应用 ============
app = FastAPI(
    title="竞品情报分析系统",
    description="AI 驱动的全渠道竞品情报分析与智能问答系统",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ API 端点 ============

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "SmartCompetitorIntel",
        "version": "1.0.0",
    }


@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    """
    智能对话接口 - RAG 检索 + LLM 生成

    流程：
    1. 将用户问题向量化
    2. 在 ChromaDB 中检索最相似的文档块
    3. 将检索结果拼接为 context
    4. 连同用户问题一起发给 DeepSeek
    5. SSE 流式返回回答
    """
    if not vector_store:
        raise HTTPException(status_code=503, detail="向量库未初始化")

    # Step 1-2: 语义检索
    search_results = vector_store.search(query=request.query, top_k=5)

    if not search_results:
        # 知识库为空，提示用户先导入数据
        async def empty_stream():
            yield "data: " + json.dumps({"text": "⚠️ 知识库为空，请先调用 /api/v1/crawl 导入数据"}, ensure_ascii=False) + "\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(empty_stream(), media_type="text/event-stream")

    # Step 3: 拼接检索结果为 context
    context_parts = []
    sources = []
    for i, result in enumerate(search_results):
        context_parts.append(f"[文档{i+1}] {result['text']}")
        sources.append({
            "index": i + 1,
            "author": result["metadata"].get("author", ""),
            "title": result["metadata"].get("title", ""),
            "distance": round(result["distance"], 4),
        })
    context = "\n\n".join(context_parts)

    if request.stream:
        # Step 4-5: SSE 流式返回
        async def event_stream():
            # 先发送检索来源信息
            yield "data: " + json.dumps({"type": "sources", "sources": sources}, ensure_ascii=False) + "\n\n"

            # 流式发送 LLM 回答
            generator = await chat_with_rag(
                query=request.query,
                context=context,
                stream=True,
            )
            async for chunk in generator:
                yield "data: " + json.dumps({"type": "text", "text": chunk}, ensure_ascii=False) + "\n\n"

            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")
    else:
        # 非流式返回
        answer = await chat_with_rag(
            query=request.query,
            context=context,
            stream=False,
        )
        return {
            "answer": answer,
            "sources": sources,
        }


@app.post("/api/v1/crawl")
async def crawl_data(request: CrawlRequest = None):
    """
    数据采集接口 - 当前使用模拟数据，后续接入真实爬虫

    将采集到的数据处理后存入向量库
    """
    if not vector_store:
        raise HTTPException(status_code=503, detail="向量库未初始化")

    # 使用模拟数据
    notes = generate_mock_data()

    # 文档处理：转文本 → 切块
    texts, metadatas = doc_processor.process_notes(notes)

    # 存入向量库
    count = vector_store.add_documents(texts, metadatas)

    return {
        "message": f"✅ 成功导入 {len(notes)} 条笔记，切分为 {count} 个文档块",
        "note_count": len(notes),
        "chunk_count": count,
        "total_docs": vector_store.get_doc_count(),
    }


@app.get("/api/v1/knowledge/stats")
async def knowledge_stats():
    """查看知识库状态"""
    if not vector_store:
        raise HTTPException(status_code=503, detail="向量库未初始化")

    return {
        "total_documents": vector_store.get_doc_count(),
        "collection_name": get_settings().chroma_collection_name,
        "embedding_model": get_settings().embedding_model,
    }


@app.post("/api/v1/knowledge/clear")
async def clear_knowledge():
    """清空知识库"""
    if not vector_store:
        raise HTTPException(status_code=503, detail="向量库未初始化")

    vector_store.clear()
    return {"message": "🗑️ 知识库已清空"}


# ============ 启动入口 ============
if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
