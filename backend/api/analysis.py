from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..schemas.analysis import (
    AnalysisRequest, 
    AnalysisResponse, 
    StockRecommendation, 
    StockAnalysis,
    StockRecommendationRequest,
    StockAnalysisRequest
)
from ..core.agent import StockAnalysisAgent
from ..api.deps import get_current_user
from ..schemas.user import User

router = APIRouter(prefix="/ai", tags=["analysis"])

@router.post("/chat", response_model=AnalysisResponse)
async def chat_with_ai(
    request: AnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    AI와의 채팅을 처리하는 엔드포인트
    """
    try:
        agent = StockAnalysisAgent()
        response = await agent.process_chat_message(request, current_user)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stock/recommendations", response_model=AnalysisResponse)
async def get_stock_recommendations(
    request: StockRecommendationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    종목 추천을 요청하는 엔드포인트
    """
    try:
        agent = StockAnalysisAgent()
        response = await agent.get_stock_recommendations(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stock/analysis", response_model=StockAnalysis)
async def get_stock_analysis(
    request: StockAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    특정 종목에 대한 상세 분석을 요청하는 엔드포인트
    """
    try:
        agent = StockAnalysisAgent()
        analysis = await agent.get_detailed_analysis(request.stock_code)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history", response_model=List[AnalysisResponse])
async def get_chat_history(
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_user)
):
    """
    사용자의 채팅 기록을 조회하는 엔드포인트
    """
    try:
        agent = StockAnalysisAgent()
        history = await agent.get_chat_history(current_user.id, page, size)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/search", response_model=List[AnalysisResponse])
async def search_chat_history(
    keyword: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_user)
):
    """
    채팅 기록을 검색하는 엔드포인트
    """
    try:
        agent = StockAnalysisAgent()
        results = await agent.search_chat_history(
            current_user.id,
            keyword,
            start_date,
            end_date,
            page,
            size
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/history/{history_id}/summarize", response_model=AnalysisResponse)
async def summarize_chat_history(
    history_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    특정 채팅 기록을 요약하는 엔드포인트
    """
    try:
        agent = StockAnalysisAgent()
        summary = await agent.summarize_chat_history(history_id, current_user.id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 