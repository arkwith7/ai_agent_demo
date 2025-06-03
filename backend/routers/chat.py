from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List
from services.stock_analysis import StockAnalysisService
from pydantic import BaseModel

router = APIRouter()
stock_analysis = StockAnalysisService()

class MessageRequest(BaseModel):
    message: str
    message_type: str = "general_chat"

@router.post("/message")
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

@router.get("/history")
async def get_chat_history(skip: int = 0, limit: int = 20):
    """채팅 기록을 반환합니다."""
    try:
        # 임시 데이터 반환
        return {
            "histories": [
                {
                    "id": 1,
                    "query_text": "삼성전자 분석해줘",
                    "response_text": "삼성전자 분석 결과입니다.",
                    "created_at": "2024-03-15T10:00:00"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 