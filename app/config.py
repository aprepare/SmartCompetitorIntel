"""应用配置管理 - 使用 Pydantic Settings 从 .env 加载配置"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类，自动从 .env 文件读取环境变量"""

    # DeepSeek API
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    # Embedding 模型
    embedding_model: str = "BAAI/bge-small-zh-v1.5"

    # ChromaDB
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "competitor_docs"

    # 应用
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例（带缓存）"""
    return Settings()
