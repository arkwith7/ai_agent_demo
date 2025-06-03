from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class StockRecommendationRequest(BaseModel):
    market_segment: str = Field(default="KOSPI", description="시장 구분 (KOSPI/KOSDAQ)")
    min_score: float = Field(default=60.0, description="최소 추천 점수")
    max_results: int = Field(default=5, description="최대 결과 수")
    include_esg: bool = Field(default=True, description="ESG 분석 포함 여부")
    include_risk_analysis: bool = Field(default=True, description="리스크 분석 포함 여부")

class StockAnalysisRequest(BaseModel):
    stock_code: str = Field(..., description="종목 코드")
    include_esg: bool = Field(default=True, description="ESG 분석 포함 여부")
    include_risk_analysis: bool = Field(default=True, description="리스크 분석 포함 여부")

class AnalysisRequest(BaseModel):
    message_type: str = Field(default="general_chat", description="메시지 타입")
    content: str = Field(..., description="메시지 내용")
    market_segment: Optional[str] = Field(default=None, description="시장 구분")
    min_score: Optional[float] = Field(default=None, description="최소 추천 점수")
    max_results: Optional[int] = Field(default=None, description="최대 결과 수")
    include_esg: Optional[bool] = Field(default=None, description="ESG 분석 포함 여부")
    include_risk_analysis: Optional[bool] = Field(default=None, description="리스크 분석 포함 여부")
    stock_code: Optional[str] = Field(default=None, description="종목 코드")

class StockRecommendation(BaseModel):
    name: str = Field(..., description="종목명")
    market: str = Field(..., description="시장 구분 (KOSPI/KOSDAQ)")
    currentPrice: float = Field(..., description="현재가")
    changeRate: float = Field(..., description="등락률")
    volume: float = Field(..., description="거래량")
    marketCap: float = Field(..., description="시가총액")
    reason: str = Field(..., description="추천 이유")
    criteria_scores: Optional[Dict[str, float]] = Field(default=None, description="버핏 기준 점수")
    esg_scores: Optional[Dict[str, float]] = Field(default=None, description="ESG 점수")
    risk_scores: Optional[Dict[str, float]] = Field(default=None, description="리스크 점수")
    total_score: Optional[float] = Field(default=None, description="종합 점수")

class StockAnalysis(BaseModel):
    stock_code: str = Field(..., description="종목 코드")
    stock_name: str = Field(..., description="종목명")
    current_price: float = Field(..., description="현재가")
    market_cap: float = Field(..., description="시가총액")
    criteria_scores: Dict[str, float] = Field(..., description="버핏 기준 점수")
    esg_scores: Optional[Dict[str, float]] = Field(default=None, description="ESG 점수")
    risk_scores: Optional[Dict[str, float]] = Field(default=None, description="리스크 점수")
    total_score: float = Field(..., description="종합 점수")
    recommendation: str = Field(..., description="투자 추천")
    financial_data: Dict[str, Any] = Field(..., description="재무 데이터")
    market_data: List[Dict[str, Any]] = Field(..., description="시장 데이터")

class AnalysisResponse(BaseModel):
    message_type: str = Field(..., description="메시지 타입")
    content: str = Field(..., description="응답 내용")
    analysis_result: Optional[Any] = Field(default=None, description="분석 결과")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")

class ChatHistory(BaseModel):
    id: int = Field(..., description="채팅 기록 ID")
    user_id: int = Field(..., description="사용자 ID")
    message_type: str = Field(..., description="메시지 타입")
    content: str = Field(..., description="메시지 내용")
    response: AnalysisResponse = Field(..., description="응답")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간") 