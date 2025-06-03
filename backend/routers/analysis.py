from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from services.stock_analysis import StockAnalysisService
from pydantic import BaseModel

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