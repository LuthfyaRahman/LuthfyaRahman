from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_url: str = "http://qdrant:6333"
    qdrant_collection: str = "gratifikasi_cases"
    qdrant_vector_size: int = 384
    similarity_threshold: float = 0.75
    top_k: int = 5
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
