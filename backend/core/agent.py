from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from schemas.analysis import AnalysisRequest, AnalysisResponse, StockRecommendation, StockAnalysis, StockRecommendationRequest, StockAnalysisRequest
from schemas.user import User
from services.stock_analysis import StockAnalysisService
from services.cache import CacheService
from services.logger import LoggerService
from services.data_providers import OpenDARTProvider, FinancialServicesStockProvider

class StockAnalysisAgent(ABC):
    @abstractmethod
    async def analyze_stocks(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        주식 분석을 수행하는 메인 메서드
        """
        pass

    @abstractmethod
    async def get_stock_recommendations(self, request: StockRecommendationRequest) -> AnalysisResponse:
        """
        종목 추천을 수행하고 결과를 반환합니다.
        """
        pass

    @abstractmethod
    async def get_detailed_analysis(self, stock_code: str) -> StockAnalysis:
        """
        특정 종목에 대한 상세 분석을 수행합니다.
        """
        pass

    @abstractmethod
    async def collect_financial_data(self, stock_code: str) -> Dict[str, Any]:
        """
        OpenDART API를 통해 재무 데이터를 수집하는 메서드
        """
        pass

    @abstractmethod
    async def collect_market_data(self, stock_code: str) -> Dict[str, Any]:
        """
        금융위원회 API를 통해 시장 데이터를 수집하는 메서드
        """
        pass

    def __init__(self):
        self.cache_service = CacheService()
        self.logger = LoggerService()
        self.opendart = OpenDARTProvider()
        self.fss = FinancialServicesStockProvider()
        self.analysis_service = StockAnalysisService(self)

    async def process_chat_message(self, request: AnalysisRequest, user: User) -> AnalysisResponse:
        """
        채팅 메시지를 처리하고 적절한 응답을 반환합니다.
        """
        try:
            self.logger.info(f"Processing chat message: {request.content}")
            
            # 메시지 타입에 따른 처리
            if request.message_type == "stock_recommendation":
                return await self.get_stock_recommendations(
                    StockRecommendationRequest(
                        market_segment=request.market_segment,
                        min_score=request.min_score,
                        max_results=request.max_results,
                        include_esg=request.include_esg,
                        include_risk_analysis=request.include_risk_analysis
                    )
                )
            elif request.message_type == "stock_analysis":
                return await self.get_detailed_analysis(request.stock_code)
            else:
                # 일반 채팅 처리
                return await self._process_general_chat(request, user)
                
        except Exception as e:
            self.logger.error(f"Error processing chat message: {str(e)}")
            raise

    async def get_stock_recommendations(self, request: StockRecommendationRequest) -> AnalysisResponse:
        """
        종목 추천을 수행하고 결과를 반환합니다.
        """
        try:
            # 캐시 확인
            cache_key = f"recommendations:{request.market_segment}:{request.min_score}"
            cached_result = await self.cache_service.get(cache_key)
            if cached_result:
                return cached_result

            # 시장 데이터 수집
            market_data = await self.analysis_service.get_market_data(request.market_segment)
            
            # 종목 분석
            recommendations = []
            for stock_data in market_data:
                try:
                    # 재무 데이터 조회
                    financial_data = await self.analysis_service.get_financial_data(stock_data['srtnCd'])
                    
                    # 버핏 기준 평가
                    criteria_scores = self.analysis_service.evaluate_buffett_criteria({
                        "market_data": stock_data,
                        "financial_data": financial_data
                    })
                    
                    # ESG 분석
                    esg_scores = await self.analysis_service.get_esg_scores(stock_data['srtnCd']) if request.include_esg else None
                    
                    # 리스크 분석
                    risk_scores = await self.analysis_service.get_risk_scores(stock_data['srtnCd']) if request.include_risk_analysis else None
                    
                    # 종합 점수 계산
                    total_score = self.analysis_service.calculate_total_score(
                        criteria_scores,
                        esg_scores,
                        risk_scores
                    )
                    
                    if total_score >= request.min_score:
                        # 추천 이유 생성
                        reason = self._generate_recommendation_reason(
                            stock_data,
                            financial_data,
                            criteria_scores,
                            esg_scores,
                            risk_scores,
                            total_score
                        )
                        
                        recommendations.append(StockRecommendation(
                            name=stock_data['itmsNm'],
                            market=stock_data.get('mrktCtg', 'KOSPI'),  # 시장 구분
                            currentPrice=float(stock_data['clpr']),
                            changeRate=float(stock_data.get('fltRt', 0)),
                            volume=float(stock_data.get('trqu', 0)),
                            marketCap=float(stock_data['mrktTotAmt']),
                            reason=reason,
                            criteria_scores=criteria_scores,
                            esg_scores=esg_scores,
                            risk_scores=risk_scores,
                            total_score=total_score
                        ))
                except Exception as e:
                    self.logger.error(f"Error analyzing stock {stock_data['srtnCd']}: {str(e)}")
                    continue
            
            # 점수 기준으로 정렬하고 결과 제한
            recommendations.sort(key=lambda x: x.total_score, reverse=True)
            recommendations = recommendations[:request.max_results]
            
            # 결과 캐싱
            response = AnalysisResponse(
                message_type=MessageType.STOCK_RECOMMENDATION,
                content="종목 추천 결과입니다.",
                analysis_result=recommendations
            )
            await self.cache_service.set(cache_key, response, ttl=3600)  # 1시간 캐시
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error getting stock recommendations: {str(e)}")
            raise

    def _generate_recommendation_reason(self, stock_data: Dict[str, Any], 
                                      financial_data: Dict[str, Any],
                                      criteria_scores: Dict[str, float],
                                      esg_scores: Optional[Dict[str, float]],
                                      risk_scores: Optional[Dict[str, float]],
                                      total_score: float) -> str:
        """추천 이유를 생성합니다."""
        reasons = []
        
        # 버핏 기준 기반 추천 이유
        if criteria_scores:
            top_criteria = sorted(criteria_scores.items(), key=lambda x: x[1], reverse=True)[:2]
            for criterion, score in top_criteria:
                if score >= 80:
                    reasons.append(f"{criterion} 점수가 매우 높습니다 ({score}점)")
        
        # ESG 기반 추천 이유
        if esg_scores:
            if esg_scores.get('overall_score', 0) >= 80:
                reasons.append("ESG 평가가 우수합니다")
        
        # 리스크 기반 추천 이유
        if risk_scores:
            if risk_scores.get('overall_risk', 0) <= 20:
                reasons.append("리스크가 낮습니다")
        
        # 기본 추천 이유
        if not reasons:
            if total_score >= 80:
                reasons.append("종합 평가가 매우 우수합니다")
            elif total_score >= 70:
                reasons.append("종합 평가가 우수합니다")
            else:
                reasons.append("안정적인 투자 대상입니다")
        
        return " | ".join(reasons)

    async def get_detailed_analysis(self, stock_code: str) -> StockAnalysis:
        """
        특정 종목에 대한 상세 분석을 수행합니다.
        """
        try:
            # 캐시 확인
            cache_key = f"analysis:{stock_code}"
            cached_result = await self.cache_service.get(cache_key)
            if cached_result:
                return cached_result

            # 시장 데이터 수집
            market_data = await self.analysis_service.get_market_data(stock_code=stock_code)
            
            # 재무 데이터 수집
            financial_data = await self.analysis_service.get_financial_data(stock_code)
            
            # 버핏 기준 평가
            criteria_scores = self.analysis_service.evaluate_buffett_criteria({
                "market_data": market_data[0] if market_data else {},
                "financial_data": financial_data
            })
            
            # ESG 분석
            esg_scores = await self.analysis_service.get_esg_scores(stock_code)
            
            # 리스크 분석
            risk_scores = await self.analysis_service.get_risk_scores(stock_code)
            
            # 종합 점수 계산
            total_score = self.analysis_service.calculate_total_score(
                criteria_scores,
                esg_scores,
                risk_scores
            )
            
            # 분석 결과 생성
            analysis = StockAnalysis(
                stock_code=stock_code,
                stock_name=financial_data['company_info']['corp_name'],
                current_price=float(market_data[0]['clpr']) if market_data else 0.0,
                market_cap=float(market_data[0]['mrktTotAmt']) if market_data else 0.0,
                criteria_scores=criteria_scores,
                esg_scores=esg_scores,
                risk_scores=risk_scores,
                total_score=total_score,
                recommendation=self.analysis_service.get_recommendation(total_score),
                financial_data=financial_data,
                market_data=market_data
            )
            
            # 결과 캐싱
            await self.cache_service.set(cache_key, analysis, ttl=3600)  # 1시간 캐시
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error getting detailed analysis for {stock_code}: {str(e)}")
            raise

    async def _process_general_chat(self, request: AnalysisRequest, user: User) -> AnalysisResponse:
        """
        일반 채팅 메시지를 처리합니다.
        """
        try:
            # 채팅 기록 저장
            await self.analysis_service.save_chat_history(user.id, request)
            
            # 메시지 내용에 따른 처리
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
                # 종목 코드 추출 로직
                stock_code = self.analysis_service.extract_stock_code(request.content)
                if stock_code:
                    return await self.get_detailed_analysis(stock_code)
            
            # 기본 응답
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
        주식 분석을 수행하는 메인 메서드
        """
        try:
            self.logger.info(f"Starting stock analysis for request: {request}")
            
            if request.message_type == "stock_recommendation":
                return await self.get_stock_recommendations(
                    StockRecommendationRequest(
                        market_segment=request.market_segment,
                        min_score=request.min_score,
                        max_results=request.max_results,
                        include_esg=request.include_esg,
                        include_risk_analysis=request.include_risk_analysis
                    )
                )
            elif request.message_type == "stock_analysis":
                return await self.get_detailed_analysis(request.stock_code)
            else:
                return await self._process_general_chat(request)
                
        except Exception as e:
            self.logger.error(f"Error in analyze_stocks: {str(e)}")
            raise

    async def collect_financial_data(self, stock_code: str) -> Dict[str, Any]:
        """
        OpenDART API를 통해 재무 데이터를 수집하는 메서드
        """
        try:
            self.logger.info(f"Collecting financial data for stock: {stock_code}")
            financial_data = await self.opendart.get_company_financials(stock_code)
            self.logger.info(f"Successfully collected financial data for {stock_code}")
            return financial_data
        except Exception as e:
            self.logger.error(f"Error collecting financial data for {stock_code}: {str(e)}")
            raise

    async def collect_market_data(self, stock_code: str) -> Dict[str, Any]:
        """
        금융위원회 API를 통해 시장 데이터를 수집하는 메서드
        """
        try:
            self.logger.info(f"Collecting market data for stock: {stock_code}")
            market_data = await self.fss.get_market_data(stock_code)
            self.logger.info(f"Successfully collected market data for {stock_code}")
            return market_data
        except Exception as e:
            self.logger.error(f"Error collecting market data for {stock_code}: {str(e)}")
            raise 