from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.base_class import Base

class QueryHistory(Base):
    __tablename__ = "query_histories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query_text = Column(String, nullable=False)
    response_text = Column(String, nullable=False)
    ai_model_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
