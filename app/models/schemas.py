"""数据模型定义 - Pydantic Schema"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ============ 采集数据模型 ============

class CompetitorNote(BaseModel):
    """竞品笔记数据模型（对应一条小红书/抖音内容）"""
    id: Optional[str] = None
    platform: str  # "xiaohongshu" / "douyin" / "shipinhao"
    author: str  # 作者名
    author_followers: Optional[int] = None  # 粉丝数
    title: str  # 标题
    content: str  # 正文内容
    likes: int = 0  # 点赞数
    collects: int = 0  # 收藏数
    comments: int = 0  # 评论数
    tags: list[str] = []  # 标签列表
    publish_time: Optional[str] = None  # 发布时间
    crawl_time: str = ""  # 采集时间
    url: Optional[str] = None  # 原始链接


class CrawlRequest(BaseModel):
    """采集请求"""
    platform: str  # 目标平台
    target: str  # 目标账号或关键词
    max_count: int = 20  # 最多采集条数


# ============ 聊天模型 ============

class ChatRequest(BaseModel):
    """聊天请求"""
    query: str  # 用户问题
    user_id: str = "default"  # 用户标识
    stream: bool = True  # 是否流式返回


class ChatResponse(BaseModel):
    """聊天响应（非流式）"""
    answer: str
    sources: list[dict] = []  # 引用的知识库来源
    tokens_used: int = 0


# ============ 报告模型 ============

class ReportRequest(BaseModel):
    """报告生成请求"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    report_type: str = "weekly"  # "daily" / "weekly"
