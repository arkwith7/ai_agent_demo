from typing import List, Dict, Any, Optional
from datetime import datetime
from schemas.analysis import AnalysisRequest, AnalysisResponse, StockRecommendation, StockAnalysis, StockRecommendationRequest, StockAnalysisRequest
from schemas.user import User
from services.stock_analysis import StockAnalysisService
from services.cache import CacheService
from services.logger import LoggerService
from schemas.chat import MessageType

class StockAnalysisAgent:
    def __init__(self):
        self.cache_service = CacheService()
        self.logger = LoggerService()
        self.analysis_service = StockAnalysisService()

    async def process_chat_message(self, request: AnalysisRequest, user: User) -> AnalysisResponse:
        """
        채팅 메시지를 처리하고 적절한 응답을 반환합니다.
        """
        try:
            self.logger.info(f"Processing chat message: {request.content}")
            
            if request.message_type == MessageType.STOCK_RECOMMENDATION:
                recommendation_req = StockRecommendationRequest(
                    market_segment=request.market_segment if request.market_segment else "KOSPI",
                    min_score=request.min_score if request.min_score else 60,
                    max_results=request.max_results if request.max_results else 5,
                )
                return await self.get_stock_recommendations(recommendation_req)
            elif request.message_type == MessageType.STOCK_ANALYSIS:
                if not request.stock_code:
                    return AnalysisResponse(
                        message_type=MessageType.ERROR,
                        content="종목 코드가 필요합니다.",
                        analysis_result={}
                    )
                analysis_result = await self.get_detailed_analysis(request.stock_code)
                return AnalysisResponse(
                    message_type=MessageType.STOCK_ANALYSIS,
                    content=f"{request.stock_code} 종목 분석 결과입니다.",
                    analysis_result=analysis_result.dict() if analysis_result else {}
                )
            else:
                return await self._process_general_chat(request, user)
                
        except Exception as e:
            self.logger.error(f"Error processing chat message: {str(e)}")
            return AnalysisResponse(
                message_type=MessageType.ERROR,
                content=f"채팅 처리 중 오류 발생: {str(e)}",
                analysis_result={}
            )

    async def get_stock_recommendations(self, request: StockRecommendationRequest) -> AnalysisResponse:
        """
        종목 추천을 수행하고 결과를 반환합니다.
        """
        try:
            self.logger.info(f"Received stock recommendation request: {request}")
            market_data_list = await self.analysis_service.collect_market_data(market_type=request.market_segment)
            
            if not market_data_list:
                self.logger.info(f"No market data found for market segment: {request.market_segment}")
                return AnalysisResponse(
                    message_type=MessageType.STOCK_RECOMMENDATION,
                    content="시장 데이터가 없어 추천할 종목이 없습니다.",
                    analysis_result=[],
                    visualization_data=None
                )

            recommendations = []
            processed_stocks = 0
            for stock_info in market_data_list:
                try:
                    stock_code = stock_info.get('종목코드') or stock_info.get('srtnCd') or stock_info.get('code')
                    stock_name = stock_info.get('종목명') or stock_info.get('itmsNm') or stock_info.get('name')

                    if not stock_code:
                        log_name = stock_name if stock_name else "Unknown Item"
                        self.logger.warning(f"Stock code not found in market data for item: {log_name}. Stock info: {stock_info}")
                        continue
                    
                    if not stock_name:
                        self.logger.warning(f"Stock name not found for stock code: {stock_code} in market data. Stock info: {stock_info}")
                        continue

                    self.logger.info(f"Processing stock_code: {stock_code} ({stock_name})")
                    financial_data_result = await self.analysis_service.collect_financial_data(stock_code)
                    
                    if not financial_data_result:
                        self.logger.warning(f"Financial data result is None for stock: {stock_code} ({stock_name})")
                        continue

                    company_info_name = financial_data_result.get("company_info", {}).get("corp_name", "")
                    if ("(No Local File)" in company_info_name or
                        "(JSON Error)" in company_info_name or
                        "(Unknown Error)" in company_info_name or
                        not financial_data_result.get("financial_statements")):
                        self.logger.warning(f"Essential financial data missing or file error for stock: {stock_code} ({stock_name}). Company Info: {company_info_name}")
                        continue
                    
                    evaluation_input_data = {
                        "market_data": stock_info,
                        "financial_data": financial_data_result
                    }
                    self.logger.info(f"Calling evaluate_buffett_criteria for {stock_code} with market_data keys: {list(stock_info.keys())} and financial_data keys: {list(financial_data_result.keys())}")
                    evaluation = self.analysis_service.evaluate_buffett_criteria(evaluation_input_data)

                    if evaluation and evaluation.get("meets_criteria"):
                        recommendations.append({
                            "code": stock_code,
                            "name": stock_name, # API 응답에는 일관된 키 사용
                            "reason": evaluation.get("reason", "Meets Buffett criteria"),
                            "details": evaluation.get("details", {}),
                            "market": stock_info.get("시장구분"), # 프론트엔드 호환성을 위해 필요한 정보 추가
                            "currentPrice": stock_info.get("현재가"),
                            "changeRate": stock_info.get("등락률"),
                            "volume": stock_info.get("거래량"),
                            "marketCap": stock_info.get("시가총액"),
                        })
                    processed_stocks += 1
                except Exception as e:
                    # 루프 내 개별 항목 처리 중 오류 발생 시 로깅 후 계속 진행
                    item_identifier = stock_info.get('종목코드', stock_info.get('srtnCd', stock_info.get('code', 'Unknown Code')))
                    self.logger.error(f"Error processing stock {item_identifier}: {e}", exc_info=True)
            
            self.logger.info(f"Processed {processed_stocks} stocks, found {len(recommendations)} recommendations.")

            if not recommendations:
                return AnalysisResponse(
                    message_type=MessageType.STOCK_RECOMMENDATION,
                    content="현재 워렌 버핏 기준에 부합하는 추천 종목을 찾지 못했습니다.",
                    analysis_result=[],
                    visualization_data=None
                )

            return AnalysisResponse(
                message_type=MessageType.STOCK_RECOMMENDATION,
                content=f"워렌 버핏 기준 추천 종목 {len(recommendations)}건을 찾았습니다.",
                analysis_result=recommendations,
                visualization_data=None
            )
        except Exception as e:
            self.logger.error(f"Error in get_stock_recommendations: {e}", exc_info=True)
            return AnalysisResponse(
                message_type=MessageType.ERROR,
                content=f"추천 생성 중 오류 발생: {str(e)}",
                analysis_result=[]
            )

    def _generate_recommendation_reason(self, stock_data: Dict[str, Any], 
                                      financial_data: Dict[str, Any],
                                      criteria_scores: Dict[str, float],
                                      esg_scores: Optional[Dict[str, float]],
                                      risk_scores: Optional[Dict[str, float]],
                                      total_score: float) -> str:
        reasons = []
        if criteria_scores:
            top_criteria = sorted(criteria_scores.items(), key=lambda x: x[1], reverse=True)[:2]
            for criterion, score in top_criteria:
                if score >= 80:
                    reasons.append(f"{criterion} 점수가 {score}점으로 우수합니다.")
        
        if not reasons:
            if total_score >= 80:
                reasons.append(f"종합 점수({total_score:.2f}점)가 매우 우수합니다.")
            elif total_score >= 70:
                reasons.append(f"종합 점수({total_score:.2f}점)가 우수합니다.")
            elif total_score >= request.min_score:
                 reasons.append(f"종합 점수({total_score:.2f}점)가 양호합니다.")
            else:
                reasons.append("종합적인 평가를 고려했습니다.")
        
        return " | ".join(reasons) if reasons else "추천 기준을 만족하는 종목입니다."

    async def get_detailed_analysis(self, stock_code: str) -> Optional[StockAnalysis]:
        """
        특정 종목에 대한 상세 분석을 수행합니다.
        """
        try:
            cache_key = f"analysis:{stock_code}"
            cached_result = await self.cache_service.get(cache_key)
            if cached_result:
                if isinstance(cached_result, StockAnalysis):
                    return cached_result
            
            specific_market_data_list = await self.analysis_service.get_specific_stock_market_data(stock_code=stock_code)
            
            if not specific_market_data_list:
                self.logger.warning(f"Market data not found for {stock_code} in get_detailed_analysis.")
                return None

            stock_market_info = specific_market_data_list[0]

            financial_data = await self.analysis_service.collect_financial_data(stock_code)
            
            if not financial_data or not financial_data.get('company_info'):
                 self.logger.warning(f"Financial data or company info not found for {stock_code}.")
                 return None

            criteria_scores = self.analysis_service.evaluate_buffett_criteria({
                "market_data": stock_market_info, 
                "financial_data": financial_data
            })
            
            esg_scores = None
            risk_scores = None
            
            total_score = sum(criteria_scores.values()) / len(criteria_scores) if criteria_scores else 0.0
            
            analysis = StockAnalysis(
                stock_code=stock_code,
                stock_name=financial_data['company_info'].get('corp_name', 'N/A'),
                current_price=float(stock_market_info.get('clpr', 0)),
                market_cap=float(stock_market_info.get('mrktTotAmt', 0)),
                criteria_scores=criteria_scores,
                total_score=total_score,
                financial_data=financial_data,
                market_data=stock_market_info
            )
            
            await self.cache_service.set(cache_key, analysis, ttl=3600)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error getting detailed analysis for {stock_code}: {str(e)}")
            return None

    async def _process_general_chat(self, request: AnalysisRequest, user: User) -> AnalysisResponse:
        """
        일반 채팅 메시지를 처리합니다.
        """
        try:
            await self.analysis_service.save_chat_history(user.id, request)
            
            if "추천" in request.content or "유망" in request.content:
                return await self.get_stock_recommendations(
                    StockRecommendationRequest(
                        market_segment="KOSPI",
                        min_score=60,
                        max_results=10,
                        include_esg=True,
                        include_risk_analysis=True
                    )
                )
            elif "분석" in request.content:
                stock_code = self.analysis_service.extract_stock_code(request.content)
                if stock_code:
                    return await self.get_detailed_analysis(stock_code)
            
            return AnalysisResponse(
                message_type="general_chat",
                content="죄송합니다. 더 구체적인 질문을 해주시면 도움을 드리겠습니다.",
                analysis_result=None
            )
            
        except Exception as e:
            self.logger.error(f"Error processing general chat: {str(e)}")
            raise

    async def get_chat_history(self, user_id: int, page: int = 1, size: int = 20) -> List[AnalysisResponse]:
        """
        사용자의 채팅 기록을 조회합니다.
        """
        try:
            return await self.analysis_service.get_chat_history(user_id, page, size)
        except Exception as e:
            self.logger.error(f"Error getting chat history: {str(e)}")
            raise

    async def search_chat_history(
        self,
        user_id: int,
        keyword: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        size: int = 20
    ) -> List[AnalysisResponse]:
        """
        채팅 기록을 검색합니다.
        """
        try:
            return await self.analysis_service.search_chat_history(
                user_id,
                keyword,
                start_date,
                end_date,
                page,
                size
            )
        except Exception as e:
            self.logger.error(f"Error searching chat history: {str(e)}")
            raise

    async def summarize_chat_history(self, history_id: int, user_id: int) -> AnalysisResponse:
        """
        특정 채팅 기록을 요약합니다.
        """
        try:
            return await self.analysis_service.summarize_chat_history(history_id, user_id)
        except Exception as e:
            self.logger.error(f"Error summarizing chat history: {str(e)}")
            raise

    async def analyze_stocks(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        주식 분석을 수행하는 메인 메서드 - process_chat_message를 통해 라우팅되도록 변경.
        이 메소드는 직접 호출되기보다는 process_chat_message 내부 로직으로 통합될 수 있습니다.
        """
        self.logger.warning("analyze_stocks is called directly, but should be routed via process_chat_message.")
        if request.message_type == MessageType.STOCK_RECOMMENDATION:
            rec_req = StockRecommendationRequest(market_segment=request.market_segment or "KOSPI", min_score=request.min_score or 60, max_results=request.max_results or 5)
            return await self.get_stock_recommendations(rec_req)
        elif request.message_type == MessageType.STOCK_ANALYSIS and request.stock_code:
            analysis_result = await self.get_detailed_analysis(request.stock_code)
            return AnalysisResponse(
                message_type=MessageType.STOCK_ANALYSIS,
                content=f"{request.stock_code} 분석 결과",
                analysis_result=analysis_result.dict() if analysis_result else {}
            )
        return AnalysisResponse(message_type=MessageType.ERROR, content="알 수 없는 분석 요청입니다.", analysis_result={})

async def get_agent() -> StockAnalysisAgent:
    return StockAnalysisAgent()