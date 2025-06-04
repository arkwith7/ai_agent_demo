from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from services.stock_analysis import StockAnalysisService
from pydantic import BaseModel
from api.deps import get_current_active_user
from schemas.analysis import (
    AnalysisResponse,
    StockRecommendationRequest,
    StockAnalysisRequest,
    StockAnalysis
)
from core.agent import StockAnalysisAgent, get_agent
from schemas.user import User
from schemas.chat import MessageType

router = APIRouter()

@router.post("/collect-market-data")
async def collect_market_data(service: StockAnalysisService = Depends(StockAnalysisService)):
    """시장 데이터를 수집하고 저장합니다."""
    try:
        collected_data = await service.collect_market_data()
        collected_count = len(collected_data) if collected_data is not None else 0
        return {
            "success": True,
            "message": f"시장 데이터 {collected_count}건 수집 및 저장이 완료되었습니다.",
            "collected_count": collected_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 수집 중 오류 발생: {str(e)}")

@router.post("/recommendations/from-latest", response_model=AnalysisResponse)
async def get_recommendations(
    request: StockRecommendationRequest,
    agent: StockAnalysisAgent = Depends(get_agent)
):
    """최신 데이터를 기반으로 주식 추천을 생성합니다."""
    response = await agent.get_stock_recommendations(request)
    if response.message_type == MessageType.ERROR:
        raise HTTPException(status_code=500, detail=response.content)
    return response

@router.get("/stock/{stock_code}", response_model=Optional[StockAnalysis])
async def get_stock_analysis(
    stock_code: str,
    agent: StockAnalysisAgent = Depends(get_agent)
):
    """특정 종목의 상세 분석을 제공합니다."""
    analysis_result = await agent.get_detailed_analysis(stock_code)
    if analysis_result is None:
        raise HTTPException(status_code=404, detail=f"{stock_code}에 대한 분석 정보를 찾을 수 없습니다.")
    return analysis_result

@router.post("/stock/recommendations", response_model=AnalysisResponse)
async def post_stock_recommendations(
    request: StockRecommendationRequest,
    agent: StockAnalysisAgent = Depends(get_agent),
    current_user: User = Depends(get_current_active_user)
):
    response = await agent.get_stock_recommendations(request)
    if response.message_type == MessageType.ERROR:
        raise HTTPException(status_code=500, detail=response.content)
    return response

@router.post("/stock/analysis", response_model=AnalysisResponse)
async def post_stock_detailed_analysis(
    request: StockAnalysisRequest,
    agent: StockAnalysisAgent = Depends(get_agent),
    current_user: User = Depends(get_current_active_user)
):
    stock_analysis_obj = await agent.get_detailed_analysis(request.stock_code)
    if stock_analysis_obj is None:
        return AnalysisResponse(
            message_type=MessageType.ERROR,
            content=f"{request.stock_code}에 대한 분석 정보를 찾을 수 없습니다.",
            analysis_result={}
        )
    
    return AnalysisResponse(
        message_type=MessageType.STOCK_ANALYSIS,
        content=f"{request.stock_code} 종목 상세 분석 결과입니다.",
        analysis_result=stock_analysis_obj.dict()
    )