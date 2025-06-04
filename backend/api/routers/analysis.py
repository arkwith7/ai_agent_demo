from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from services.stock_analysis import StockAnalysisService
from pydantic import BaseModel
from api.deps import get_current_active_user
from schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
    StockRecommendationRequest,
    StockAnalysisRequest
)
from core.agent import StockAnalysisAgent

router = APIRouter()
stock_analysis = StockAnalysisService()

class RecommendationRequest(BaseModel):
    market_segment: str = "KOSPI"
    min_score: int = 60
    max_results: int = 5

@router.post("/collect-market-data")
async def collect_market_data():
    """시장 데이터를 수집하고 저장합니다."""
    try:
        result = await stock_analysis.collect_market_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations/from-latest")
async def get_recommendations(request: RecommendationRequest):
    """최신 데이터를 기반으로 주식 추천을 생성합니다."""
    try:
        recommendations = await stock_analysis.get_recommendations_from_latest({
            "market_segment": request.market_segment,
            "min_score": request.min_score,
            "max_results": request.max_results
        })
        return {
            "success": True,
            "message": "추천 종목을 생성했습니다.",
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stock/{stock_code}")
async def get_stock_analysis(stock_code: str):
    """특정 종목의 상세 분석을 제공합니다."""
    try:
        analysis = await stock_analysis.get_detailed_analysis(stock_code)
        return {
            "success": True,
            "message": "종목 분석을 완료했습니다.",
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 사용자 종목 추천 (직접 지정된 파라미터)
@router.post("/stock/recommendations", response_model=AnalysisResponse)
async def post_stock_recommendations(
    request: StockRecommendationRequest,
    current_user = Depends(get_current_active_user)
):
    try:
        agent = StockAnalysisAgent()
        return await agent.get_stock_recommendations(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 사용자 종목 상세 분석 (직접 지정된 파라미터)
@router.post("/stock/analysis", response_model=AnalysisResponse)
async def post_stock_detailed_analysis(
    request: StockAnalysisRequest,
    current_user = Depends(get_current_active_user)
):
    try:
        agent = StockAnalysisAgent()
        return await agent.get_detailed_analysis(request.stock_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI 채팅 엔드포인트
class MessageRequest(BaseModel):
    message: str
    message_type: str = "general_chat"

@router.post("/chat/message")
async def send_message(request: MessageRequest):
    """채팅 메시지를 처리합니다."""
    try:
        if request.message_type == "stock_recommendation":
            recommendations = await stock_analysis.get_recommendations_from_latest()
            return {
                "content": "추천 종목을 생성했습니다.",
                "message_type": "stock_recommendation",
                "analysis_result": recommendations
            }
        elif request.message_type == "stock_analysis":
            # 종목 코드 추출 (예: "삼성전자 분석해줘" -> "005930")
            stock_code = "005930"  # 임시로 삼성전자 코드 사용
            analysis = await stock_analysis.get_detailed_analysis(stock_code)
            return {
                "content": "종목 분석을 완료했습니다.",
                "message_type": "stock_analysis",
                "analysis_result": analysis
            }
        else:
            return {
                "content": "메시지를 받았습니다. 종목 분석이나 추천을 원하시면 '분석' 또는 '추천'이라는 단어를 포함해서 말씀해주세요.",
                "message_type": "general_chat"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 채팅 기록 조회
@router.get("/chat/history", response_model=List[AnalysisResponse])
async def get_chat_history(
    page: int = 1,
    size: int = 20,
    current_user = Depends(get_current_active_user)
):
    try:
        agent = StockAnalysisAgent()
        return await agent.get_chat_history(current_user.id, page, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 채팅 기록 검색
@router.get("/chat/history/search", response_model=List[AnalysisResponse])
async def search_chat_history(
    keyword: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    current_user = Depends(get_current_active_user)
):
    try:
        agent = StockAnalysisAgent()
        return await agent.search_chat_history(
            current_user.id, keyword, start_date, end_date, page, size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 채팅 기록 요약
@router.post("/chat/history/{history_id}/summarize", response_model=AnalysisResponse)
async def summarize_chat_history(
    history_id: int,
    current_user = Depends(get_current_active_user)
):
    try:
        agent = StockAnalysisAgent()
        return await agent.summarize_chat_history(history_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))