"""文档处理器 - 将采集的竞品数据切块处理，准备存入向量库

面试考点：
- RecursiveCharacterTextSplitter 优先按段落切，保持语义完整
- chunk_size 500-1000 字符，overlap 100-200 防止语义断裂
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models.schemas import CompetitorNote


class DocumentProcessor:
    """文档处理器：将竞品笔记转换为可向量化的文档块"""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", "，", " "],
        )

    def note_to_text(self, note: CompetitorNote) -> str:
        """将一条竞品笔记转成纯文本（包含元数据，方便检索时还原上下文）"""
        parts = [
            f"【平台】{note.platform}",
            f"【作者】{note.author}（粉丝：{note.author_followers or '未知'}）",
            f"【标题】{note.title}",
            f"【内容】{note.content}",
            f"【数据】点赞 {note.likes} | 收藏 {note.collects} | 评论 {note.comments}",
        ]
        if note.tags:
            parts.append(f"【标签】{'、'.join(note.tags)}")
        if note.publish_time:
            parts.append(f"【发布时间】{note.publish_time}")
        return "\n".join(parts)

    def process_notes(self, notes: list[CompetitorNote]) -> tuple[list[str], list[dict]]:
        """
        批量处理竞品笔记：转文本 → 切块 → 返回文本块和元数据

        Returns:
            texts: 切好的文本块列表
            metadatas: 每个文本块对应的元数据
        """
        all_texts = []
        all_metadatas = []

        for note in notes:
            full_text = self.note_to_text(note)
            chunks = self.splitter.split_text(full_text)

            for i, chunk in enumerate(chunks):
                all_texts.append(chunk)
                all_metadatas.append({
                    "source_id": note.id or "",
                    "platform": note.platform,
                    "author": note.author,
                    "title": note.title,
                    "likes": note.likes,
                    "collects": note.collects,
                    "comments": note.comments,
                    "chunk_index": i,
                })

        return all_texts, all_metadatas
