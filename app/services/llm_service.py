"""LLM 服务 - DeepSeek API 调用（支持 SSE 流式输出）

面试考点：
- 使用 AsyncOpenAI 异步客户端（生产环境必须用异步）
- stream=True 实现 SSE 流式输出（打字机效果）
- System Prompt 里注入检索结果 + 防幻觉规则
"""

from openai import AsyncOpenAI
from typing import AsyncGenerator
from app.config import get_settings


# 全局异步客户端
_async_client: AsyncOpenAI | None = None


def get_llm_client() -> AsyncOpenAI:
    """获取 DeepSeek 异步客户端单例"""
    global _async_client
    if _async_client is None:
        settings = get_settings()
        _async_client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
    return _async_client


# RAG 问答的 System Prompt
RAG_SYSTEM_PROMPT = """你是一个专业的竞品数据分析师，专注于小红书、抖音等社交媒体平台的内容分析。

规则：
1. 只基于下方【检索结果】中的数据进行分析，不要编造任何数据
2. 如果检索结果中没有相关信息，直接回答"抱歉，知识库中未找到相关数据"
3. 回答中必须引用具体数字（点赞数、粉丝数、互动量等）
4. 用 Markdown 格式回答，包含标题、列表和表格
5. 对比分析时使用表格形式呈现，一目了然
6. 给出有洞察力的分析结论，不要仅仅罗列数据

===== 检索结果 =====
{context}
=================="""


async def chat_with_rag(
    query: str,
    context: str,
    stream: bool = True,
) -> AsyncGenerator[str, None] | str:
    """
    基于 RAG 检索结果调用 LLM 生成回答

    Args:
        query: 用户问题
        context: 从向量库检索到的相关文档（拼接后的文本）
        stream: 是否流式返回

    Yields/Returns:
        流式模式：逐字 yield 文本片段
        非流式模式：返回完整回答字符串
    """
    settings = get_settings()
    client = get_llm_client()

    messages = [
        {"role": "system", "content": RAG_SYSTEM_PROMPT.format(context=context)},
        {"role": "user", "content": query},
    ]

    if stream:
        # 流式输出（SSE）
        response = await client.chat.completions.create(
            model=settings.deepseek_model,
            messages=messages,
            temperature=0.3,
            stream=True,
        )

        async def generate():
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return generate()
    else:
        # 非流式输出
        response = await client.chat.completions.create(
            model=settings.deepseek_model,
            messages=messages,
            temperature=0.3,
            stream=False,
        )
        return response.choices[0].message.content or ""
