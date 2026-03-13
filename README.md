# 🔍 SmartCompetitorIntel - AI 竞品情报分析系统

> AI 驱动的全渠道竞品情报分析与智能问答系统

## ✨ 功能特性

- **RAG 智能问答**：基于向量检索的竞品知识库问答，精准引用数据
- **SSE 流式输出**：打字机效果的实时回答，体验流畅
- **语义检索**：使用 bge-small-zh 中文 Embedding 模型，语义理解准确
- **防幻觉机制**：System Prompt 严格约束，只基于检索数据回答
- **模块化架构**：清晰的分层设计，易于扩展

## 🏗️ 技术栈

| 技术 | 用途 |
|---|---|
| **FastAPI** | Web 框架，异步 + SSE 流式 |
| **DeepSeek** | 大模型 API |
| **ChromaDB** | 向量数据库 |
| **bge-small-zh** | 中文 Embedding 模型 |
| **LangChain** | 文本切块工具 |
| **Pydantic** | 数据校验 + 配置管理 |

## 📁 项目结构

```
SmartCompetitorIntel/
├── app/
│   ├── main.py                  # FastAPI 入口（5个API端点）
│   ├── config.py                # Pydantic Settings 配置
│   ├── models/schemas.py        # 数据模型（Pydantic）
│   ├── rag/
│   │   ├── document_processor.py # 文档切块（RecursiveCharacterTextSplitter）
│   │   └── vector_store.py       # ChromaDB 向量存储 + 语义检索
│   ├── services/
│   │   └── llm_service.py        # DeepSeek LLM（SSE流式 + 非流式）
│   └── crawler/
│       └── mock_data.py          # 模拟竞品数据
├── .env.example                  # 环境变量模板
├── requirements.txt
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入你的 DeepSeek API Key
```

### 3. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 导入数据 & 测试问答

```bash
# 导入模拟数据到知识库
curl -X POST http://localhost:8000/api/v1/crawl

# RAG 问答
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "哪个赛道互动量最高？", "stream": false}'
```

### 5. Swagger 文档

启动后访问 http://localhost:8000/docs 查看完整 API 文档。

## 📡 API 接口

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/health` | 健康检查 |
| POST | `/api/v1/chat` | 智能对话（RAG + SSE） |
| POST | `/api/v1/crawl` | 导入数据到知识库 |
| GET | `/api/v1/knowledge/stats` | 知识库状态 |
| POST | `/api/v1/knowledge/clear` | 清空知识库 |

## 🔮 后续规划

- [ ] Agent 工具调用（实时搜索 + 时间查询）
- [ ] 自动日报/周报生成
- [ ] 多轮对话记忆（Redis）
- [ ] Docker 容器化部署
- [ ] 真实平台数据采集器

## 📄 License

MIT
