from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from schemas.analysis import StockRecommendation, StockAnalysis

class MessageType(str, Enum):
    GENERAL_CHAT = "general_chat"
    STOCK_RECOMMENDATION = "stock_recommendation"
    STOCK_ANALYSIS = "stock_analysis"
    ANALYSIS = "analysis"
    ERROR = "error"

class ChatMessage(BaseModel):
    message_type: MessageType
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()

class ChatResponse(BaseModel):
    message_type: MessageType
    content: str
    analysis_result: Optional[Union[Dict[str, Any], List[StockRecommendation], StockAnalysis]] = None
    timestamp: datetime = datetime.now() 