from fastapi import APIRouter, Depends
from schemas.user import UserRead
from api import deps
from services import azure_openai_service
from services.agent import process_query, get_agent
from api.routers.crud import crud_token_usage_log, crud_query_history
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks
from core.config import settings
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

router = APIRouter()

# Enhanced Warren Buffett Analysis Request Schema
class BuffettAnalysisRequest(BaseModel):
    """Enhanced Warren Buffett 8-step analysis request"""
    question: str = Field(..., description="Analysis question or request")
    market_segment: str = Field(default="KOSPI", description="Market segment (KOSPI, KOSDAQ, ALL)")
    min_score: int = Field(default=60, ge=0, le=100, description="Minimum score filter")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum results")
    include_esg: bool = Field(default=True, description="Include ESG analysis")
    include_risk_analysis: bool = Field(default=True, description="Include risk analysis")
    sectors: Optional[List[str]] = Field(default=None, description="Specific sectors to analyze")
    use_real_data: bool = Field(default=True, description="Use real-time API data")

class BuffettAnalysisResponse(BaseModel):
    """Enhanced Warren Buffett analysis response"""
    success: bool
    analysis_type: str
    recommendations: List[str]
    tools_used: List[str]
    analysis_metadata: Dict[str, Any]
    raw_output: str

@router.post("/chat")
async def chat_with_ai(
    query: str,
    background_tasks: BackgroundTasks,
    current_user: UserRead = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    ai_response, input_tokens, output_tokens = await azure_openai_service.get_ai_response(query)
    background_tasks.add_task(
        crud_query_history.create_query_log,
        db=db,
        user_id=current_user.id,
        query_text=query,
        response_text=ai_response,
        ai_model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
    )
    background_tasks.add_task(
        crud_token_usage_log.create_token_usage_log,
        db=db,
        user_id=current_user.id,
        ai_model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
    return {"response": ai_response}

@router.post("/warren-buffett-analysis", response_model=BuffettAnalysisResponse)
async def enhanced_warren_buffett_analysis(
    request: BuffettAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: UserRead = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Enhanced Warren Buffett 8-step stock analysis with ESG and risk assessment
    
    This endpoint provides comprehensive stock analysis using:
    - Traditional 6-step Buffett criteria
    - ESG (Environmental, Social, Governance) evaluation
    - Advanced risk analysis (Beta, VaR, volatility)
    - Portfolio optimization recommendations
    - Real-time data integration (KRX, OpenDART APIs)
    """
    try:
        # Get the enhanced Warren Buffett agent
        agent = await get_agent()
        
        # Enhance the query with specific parameters
        enhanced_query = f"""
        워런 버핏의 8단계 투자 기준으로 종목을 분석해주세요.
        
        요청사항: {request.question}
        
        분석 조건:
        - 시장: {request.market_segment}
        - 최소 점수: {request.min_score}점 이상
        - 최대 결과 수: {request.max_results}개
        - ESG 분석 포함: {'예' if request.include_esg else '아니오'}
        - 리스크 분석 포함: {'예' if request.include_risk_analysis else '아니오'}
        - 대상 업종: {', '.join(request.sectors) if request.sectors else '전체'}
        - 실시간 데이터 사용: {'예' if request.use_real_data else '아니오 (Mock 데이터)'}
        
        enhanced_buffett_stock_screener 도구를 사용하여 8단계 종합 분석을 수행해주세요.
        결과에는 다음을 포함해주세요:
        1. 8단계 기준별 점수와 분석
        2. ESG 평가 및 Buffett 호환성
        3. 리스크 분석 (Beta, 변동성, VaR)
        4. 포트폴리오 최적화 제안
        5. 투자 추천 등급과 근거
        """
        
        # Perform the analysis
        result = await agent.analyze_stock(enhanced_query)
        
        # Log the query and response
        background_tasks.add_task(
            crud_query_history.create_query_log,
            db=db,
            user_id=current_user.id,
            query_text=request.question,
            response_text=str(result["recommendations"]),
            ai_model_name="Enhanced Warren Buffett AI Agent"
        )
        
        # Prepare the response
        response = BuffettAnalysisResponse(
            success=result["success"],
            analysis_type="Enhanced Warren Buffett 8-Step Analysis",
            recommendations=result["recommendations"],
            tools_used=result["tools_used"],
            analysis_metadata={
                "market_segment": request.market_segment,
                "min_score": request.min_score,
                "max_results": request.max_results,
                "include_esg": request.include_esg,
                "include_risk_analysis": request.include_risk_analysis,
                "sectors": request.sectors,
                "use_real_data": request.use_real_data,
                "criteria_used": "8-step Enhanced Buffett Filter" if request.include_esg and request.include_risk_analysis 
                              else "7-step Buffett Filter (ESG)" if request.include_esg
                              else "7-step Buffett Filter (Risk)" if request.include_risk_analysis
                              else "6-step Traditional Buffett Filter"
            },
            raw_output=result["raw_output"]
        )
        
        return response
        
    except Exception as e:
        # Return error response
        return BuffettAnalysisResponse(
            success=False,
            analysis_type="Enhanced Warren Buffett 8-Step Analysis",
            recommendations=[
                f"❌ 분석 중 오류가 발생했습니다: {str(e)}",
                "💡 네트워크 연결을 확인하시거나 잠시 후 다시 시도해주세요.",
                "🔧 문제가 지속되면 관리자에게 문의해주세요."
            ],
            tools_used=[],
            analysis_metadata={
                "error": str(e),
                "market_segment": request.market_segment,
                "min_score": request.min_score,
                "max_results": request.max_results
            },
            raw_output=str(e)
        )

@router.post("/stock-analysis")
async def stock_analysis(
    question: str,
    background_tasks: BackgroundTasks,
    current_user: UserRead = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    General stock analysis using Warren Buffett AI Agent
    
    This is a simpler endpoint for general stock analysis questions.
    For advanced 8-step analysis, use /warren-buffett-analysis endpoint.
    """
    try:
        # Use the enhanced agent for general stock analysis
        recommendations = await process_query(question)
        
        # Log the interaction
        background_tasks.add_task(
            crud_query_history.create_query_log,
            db=db,
            user_id=current_user.id,
            query_text=question,
            response_text=str(recommendations),
            ai_model_name="Warren Buffett AI Agent"
        )
        
        return {
            "success": True,
            "question": question,
            "recommendations": recommendations
        }
        
    except Exception as e:
        return {
            "success": False,
            "question": question,
            "recommendations": [
                f"❌ 분석 중 오류가 발생했습니다: {str(e)}",
                "💡 다시 시도하시거나 다른 질문으로 문의해주세요."
            ],
            "error": str(e)
        }
