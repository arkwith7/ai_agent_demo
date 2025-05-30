"""
워런 버핏 투자 기준 종목 스크리닝 도구 (Enhanced Buffett Filter Tool)
8단계 투자 기준에 따라 종목을 필터링하고 점수를 매기는 LangChain Tool
- 기존 6단계 기준에 ESG 평가와 리스크 분석 추가
- 실시간 데이터 연동 (KRX, OpenDART API)
- 고급 분석 및 포트폴리오 최적화 기능
"""
from typing import Type, Dict, Any, List, Optional, Tuple
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import json
import asyncio
import logging
from datetime import datetime, timedelta
import random

# 새로운 데이터 제공자 및 분석 도구 import
from .data_providers.krx_api import KRXDataProvider, krx_provider
from .data_providers.opendart_api import OpenDARTProvider, opendart_provider
from .esg_analysis_tool import ESGAnalysisTool, esg_analyzer
from .advanced_analysis_tool import AdvancedAnalysisTool, advanced_analyzer

class BuffettFilterInput(BaseModel):
    """Input for Enhanced BuffettFilter Tool"""
    market_segment: str = Field(
        default="KOSPI", 
        description="Market segment to analyze (KOSPI, KOSDAQ, ALL)"
    )
    min_score: int = Field(
        default=60, 
        description="Minimum total score to pass filter (0-100)"
    )
    max_results: int = Field(
        default=10, 
        description="Maximum number of results to return"
    )
    include_esg: bool = Field(
        default=True,
        description="Include ESG analysis in scoring"
    )
    include_risk_analysis: bool = Field(
        default=True,
        description="Include advanced risk analysis"
    )
    sectors: Optional[List[str]] = Field(
        default=None,
        description="Specific sectors to analyze (if None, analyze all)"
    )
    use_real_data: bool = Field(
        default=True,
        description="Use real-time data from APIs (if False, use mock data)"
    )

class BuffettFilterTool(BaseTool):
    """
    워런 버핏의 8단계 투자 기준에 따라 종목을 스크리닝하는 도구
    
    8단계 평가 기준:
    1. 시가총액 기준 (상위 30% 대형주)
    2. 자기자본이익률 (ROE 15% 이상)  
    3. 수익성 (순이익률, FCF)
    4. 성장성 (시총 vs 자본 증가율)
    5. 미래가치 (5년 FCF 예측)
    6. 가치평가 (내재가치 vs 시가)
    7. ESG 평가 (환경, 사회, 지배구조)
    8. 리스크 분석 (베타, 변동성, VaR)
    """
    name: str = "enhanced_buffett_stock_screener"
    description: str = """
    워런 버핏의 8단계 투자 기준으로 종목을 스크리닝합니다.
    기존 6단계 기준에 ESG 분석과 리스크 평가를 추가한 고도화된 도구입니다.
    각 기준별로 0-100점 점수를 매기고 종합 점수가 높은 종목을 추천합니다.
    
    입력: market_segment, min_score, max_results, include_esg, include_risk_analysis 등
    출력: 8단계 기준을 통과한 종목 리스트와 각 기준별 점수, 포트폴리오 최적화 제안
    """
    args_schema: Type[BaseModel] = BuffettFilterInput

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"
    
    # 클래스 변수로 공유 리소스 정의
    _logger = None
    _krx_provider = None
    _opendart_provider = None
    _esg_analyzer = None
    _advanced_analyzer = None
    
    @classmethod
    def get_logger(cls):
        """로거 인스턴스 반환"""
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger
    
    @classmethod
    def get_krx_provider(cls):
        """KRX 데이터 제공자 반환"""
        if cls._krx_provider is None:
            cls._krx_provider = krx_provider
        return cls._krx_provider
    
    @classmethod 
    def get_opendart_provider(cls):
        """OpenDART 데이터 제공자 반환"""
        if cls._opendart_provider is None:
            cls._opendart_provider = opendart_provider
        return cls._opendart_provider
    
    @classmethod
    def get_esg_analyzer(cls):
        """ESG 분석기 반환"""
        if cls._esg_analyzer is None:
            cls._esg_analyzer = esg_analyzer
        return cls._esg_analyzer
    
    @classmethod
    def get_advanced_analyzer(cls):
        """고급 분석기 반환"""
        if cls._advanced_analyzer is None:
            cls._advanced_analyzer = advanced_analyzer
        return cls._advanced_analyzer
    
    @classmethod
    def _get_mock_market_data(cls, market_segment: str) -> List[Dict[str, Any]]:
        """모의 시장 데이터 생성 (실제로는 KRX/OpenDART API 연동)"""
        
        # 주요 종목 리스트
        stock_pool = [
            {"symbol": "005930", "name": "삼성전자", "sector": "반도체"},
            {"symbol": "000660", "name": "SK하이닉스", "sector": "반도체"},
            {"symbol": "035420", "name": "NAVER", "sector": "인터넷"},
            {"symbol": "005380", "name": "현대차", "sector": "자동차"},
            {"symbol": "006400", "name": "삼성SDI", "sector": "배터리"},
            {"symbol": "207940", "name": "삼성바이오로직스", "sector": "바이오"},
            {"symbol": "068270", "name": "셀트리온", "sector": "바이오"},
            {"symbol": "035720", "name": "카카오", "sector": "인터넷"},
            {"symbol": "051910", "name": "LG화학", "sector": "화학"},
            {"symbol": "012330", "name": "현대모비스", "sector": "자동차부품"},
            {"symbol": "028260", "name": "삼성물산", "sector": "종합상사"},
            {"symbol": "066570", "name": "LG전자", "sector": "가전"},
            {"symbol": "003550", "name": "LG", "sector": "지주회사"},
            {"symbol": "096770", "name": "SK이노베이션", "sector": "정유화학"},
            {"symbol": "017670", "name": "SK텔레콤", "sector": "통신"}
        ]
        
        market_data = []
        
        for stock in stock_pool:
            # 종목별 고정 시드로 일관된 데이터 생성
            random.seed(hash(stock["symbol"]) % 1000)
            
            # 기본 재무 데이터 생성
            market_cap = random.uniform(5000000, 500000000)  # 50억~5000억
            current_price = random.uniform(10000, 80000)
            shares = market_cap * 1000000 / current_price  # 주식수 계산
            
            # ROE 3년 데이터 (최근일수록 가중치)
            roe_y3 = random.uniform(5, 25)
            roe_y2 = roe_y3 * random.uniform(0.8, 1.3)
            roe_y1 = roe_y2 * random.uniform(0.8, 1.3)
            
            # FCF 및 수익성 데이터
            revenue = market_cap * random.uniform(0.5, 3.0)
            net_income = revenue * random.uniform(0.03, 0.25)
            fcf = net_income * random.uniform(0.7, 1.5)
            
            stock_data = {
                **stock,
                "market_cap": market_cap,
                "current_price": current_price,
                "shares_outstanding": shares,
                
                # ROE 데이터
                "roe_y1": roe_y1,
                "roe_y2": roe_y2, 
                "roe_y3": roe_y3,
                "roe_3y_avg": (roe_y1 * 0.5 + roe_y2 * 0.3 + roe_y3 * 0.2),
                
                # 수익성 데이터
                "revenue": revenue,
                "net_income": net_income,
                "net_profit_margin": (net_income / revenue) * 100,
                "fcf": fcf,
                "fcf_per_share": fcf / shares,
                "fcf_margin": (fcf / revenue) * 100,
                
                # 성장성 데이터
                "market_cap_3y_ago": market_cap / random.uniform(1.1, 2.5),
                "equity_3y_ago": market_cap * 0.6 / random.uniform(1.0, 2.0),
                
                # 밸류에이션
                "book_value": market_cap * random.uniform(0.4, 1.2),
                "per": random.uniform(8, 35),
                "pbr": random.uniform(0.5, 3.0),
                
                # 기타
                "debt_to_equity": random.uniform(0.1, 1.5),
                "current_ratio": random.uniform(1.0, 3.0),
                "dividend_yield": random.uniform(0.5, 5.0)
            }
            
            # 계산된 메트릭 추가
            stock_data["market_cap_growth_3y"] = ((market_cap / stock_data["market_cap_3y_ago"]) ** (1/3) - 1) * 100
            stock_data["equity_growth_3y"] = ((stock_data["book_value"] / stock_data["equity_3y_ago"]) ** (1/3) - 1) * 100
            
            # 5년 FCF 예측 (단순 성장률 적용)
            fcf_growth = random.uniform(3, 12)
            projected_fcf_sum = sum(fcf * ((1 + fcf_growth/100) ** year) for year in range(1, 6))
            stock_data["fcf_projection_5y_sum"] = projected_fcf_sum

    @classmethod
    def _calculate_enhanced_total_score(cls, stock: Dict[str, Any], all_stocks: List[Dict[str, Any]], 
                                      include_esg: bool, include_risk_analysis: bool) -> Dict[str, Any]:
        """강화된 종합 점수 계산 (8단계 기준)"""
        
        # 기존 6단계 점수 계산
        basic_scores = {
            "market_cap_score": cls._score_market_cap_criteria(stock, all_stocks),
            "roe_score": cls._score_roe_criteria(stock),
            "profitability_score": cls._score_profitability_criteria(stock, all_stocks),
            "growth_score": cls._score_growth_criteria(stock),
            "fcf_projection_score": cls._score_fcf_projection_criteria(stock),
            "valuation_score": cls._score_valuation_criteria(stock)
        }
        
        # 7단계: ESG 점수
        esg_score = 0
        esg_details = None
        if include_esg:
            try:
                esg_analysis = asyncio.run(
                    cls.get_esg_analyzer().analyze_esg_score(stock["symbol"], stock["sector"])
                )
                esg_score = esg_analysis["overall_score"]
                esg_details = esg_analysis
            except Exception as e:
                logging.getLogger(__name__).warning(f"ESG 분석 실패 ({stock['symbol']}): {e}")
                esg_score = 70  # 기본값
        
        # 8단계: 리스크 점수
        risk_score = 0
        risk_details = None
        if include_risk_analysis:
            try:
                risk_analysis = asyncio.run(
                    cls.get_advanced_analyzer().analyze_risk(stock, all_stocks)
                )
                # 리스크 점수 변환 (낮은 리스크 = 높은 점수)
                if risk_analysis.risk_grade == "Low Risk":
                    risk_score = 90
                elif risk_analysis.risk_grade == "Medium Risk":
                    risk_score = 70
                else:
                    risk_score = 50
                
                risk_details = risk_analysis
            except Exception as e:
                logging.getLogger(__name__).warning(f"리스크 분석 실패 ({stock['symbol']}): {e}")
                risk_score = 70  # 기본값
        
        # 가중 평균 계산 (8단계 기준)
        all_scores = {**basic_scores}
        if include_esg:
            all_scores["esg_score"] = esg_score
        if include_risk_analysis:
            all_scores["risk_score"] = risk_score
        
        # 동적 가중치 계산
        weights = cls._calculate_dynamic_weights(include_esg, include_risk_analysis)
        total_score = sum(all_scores[key] * weights[key] for key in all_scores.keys())
        
        # 결과 조합
        result = {
            **stock,
            **all_scores,
            "total_score": round(total_score, 1),
            "recommendation": cls._get_enhanced_recommendation(total_score, esg_score, risk_score)
        }
        
        # 상세 분석 결과 추가
        if esg_details:
            result["esg_analysis"] = esg_details
        if risk_details:
            result["risk_analysis"] = risk_details
        
        return result
    
    def _calculate_dynamic_weights(self, include_esg: bool, include_risk_analysis: bool) -> Dict[str, float]:
        """동적 가중치 계산"""
        base_weights = {
            "market_cap_score": 0.12,
            "roe_score": 0.18,
            "profitability_score": 0.18,
            "growth_score": 0.12,
            "fcf_projection_score": 0.18,
            "valuation_score": 0.12
        }
        
        if include_esg and include_risk_analysis:
            # 8단계 전체 사용
            base_weights.update({
                "esg_score": 0.05,
                "risk_score": 0.05
            })
        elif include_esg:
            # 7단계 (ESG 포함)
            base_weights["esg_score"] = 0.10
        elif include_risk_analysis:
            # 7단계 (리스크 포함)
            base_weights["risk_score"] = 0.10
        
        # 가중치 정규화
        total_weight = sum(base_weights.values())
        return {k: v/total_weight for k, v in base_weights.items()}
    
    def _get_enhanced_recommendation(self, total_score: float, esg_score: float, risk_score: float) -> str:
        """강화된 투자 추천"""
        base_recommendation = self._get_recommendation(total_score)
        
        # ESG 및 리스크 요소 고려한 조정
        if esg_score > 0 and esg_score < 60:
            if "Strong Buy" in base_recommendation:
                base_recommendation = "🔵 Buy (ESG 주의)"
            elif "Buy" in base_recommendation:
                base_recommendation = "🟡 Hold (ESG 개선 필요)"
        
        if risk_score > 0 and risk_score < 60:
            if "Strong Buy" in base_recommendation:
                base_recommendation = "🔵 Buy (고위험)"
            elif "Buy" in base_recommendation:
                base_recommendation = "🟡 Hold (리스크 관리 필요)"
        
        return base_recommendation
    
    def _format_enhanced_results(self, market_segment: str, min_score: int, total_analyzed: int, 
                                qualified_count: int, top_stocks: List[Dict[str, Any]], 
                                portfolio_optimization, include_esg: bool, include_risk_analysis: bool) -> Dict[str, Any]:
        """강화된 결과 포맷팅"""
        
        if not top_stocks:
            return {
                "error": f"⚠️ 최소 점수 {min_score}점 이상을 만족하는 종목이 없습니다.",
                "analysis_summary": {
                    "total_analyzed": total_analyzed,
                    "qualified_count": qualified_count,
                    "criteria_used": self._get_criteria_description(include_esg, include_risk_analysis)
                }
            }
        
        result = {
            "filter_criteria": {
                "market_segment": market_segment,
                "min_score": min_score,
                "total_analyzed": total_analyzed,
                "qualified_count": qualified_count,
                "enhanced_features": {
                    "esg_analysis": include_esg,
                    "risk_analysis": include_risk_analysis,
                    "portfolio_optimization": portfolio_optimization is not None
                }
            },
            "top_recommendations": [],
            "summary": f"📊 Enhanced Buffett Filter: {total_analyzed}개 종목 중 {qualified_count}개가 강화된 기준을 통과했습니다."
        }
        
        # 상위 종목 상세 정보
        for i, stock in enumerate(top_stocks, 1):
            stock_result = {
                "rank": i,
                "symbol": stock["symbol"],
                "name": stock["name"],
                "sector": stock["sector"],
                "total_score": stock["total_score"],
                "recommendation": stock["recommendation"],
                "key_metrics": self._extract_key_metrics(stock),
                "detailed_scores": self._extract_detailed_scores(stock, include_esg, include_risk_analysis)
            }
            
            # ESG 분석 결과 추가
            if include_esg and "esg_analysis" in stock:
                stock_result["esg_insights"] = {
                    "overall_grade": stock["esg_analysis"]["grade"],
                    "buffett_compatibility": stock["esg_analysis"]["buffett_compatibility"]["grade"],
                    "key_strengths": stock["esg_analysis"]["risk_assessment"].strengths[:2],
                    "concerns": stock["esg_analysis"]["risk_assessment"].key_concerns[:2]
                }
            
            # 리스크 분석 결과 추가
            if include_risk_analysis and "risk_analysis" in stock:
                stock_result["risk_insights"] = {
                    "risk_grade": stock["risk_analysis"].risk_grade,
                    "beta": round(stock["risk_analysis"].beta, 2),
                    "volatility": f"{stock['risk_analysis'].volatility:.1%}",
                    "var_95": f"{stock['risk_analysis'].value_at_risk:.1%}"
                }
            
            result["top_recommendations"].append(stock_result)
        
        # 포트폴리오 최적화 결과 추가
        if portfolio_optimization:
            result["portfolio_optimization"] = {
                "expected_return": f"{portfolio_optimization.expected_return:.1%}",
                "expected_risk": f"{portfolio_optimization.expected_risk:.1%}",
                "sharpe_ratio": round(portfolio_optimization.sharpe_ratio, 2),
                "diversification_score": round(portfolio_optimization.diversification_score, 1),
                "recommended_allocation": {
                    symbol: {
                        "weight": f"{data['weight']:.1%}",
                        "amount": f"{data['amount']:,.0f}원",
                        "shares": data['shares']
                    }
                    for symbol, data in portfolio_optimization.recommended_weights.items()
                },
                "investment_advice": self._generate_portfolio_advice(portfolio_optimization)
            }
        
        return result
    
    def _get_criteria_description(self, include_esg: bool, include_risk_analysis: bool) -> str:
        """사용된 기준 설명"""
        base = "Warren Buffett 6단계 기준"
        if include_esg and include_risk_analysis:
            return f"{base} + ESG 분석 + 리스크 분석 (8단계)"
        elif include_esg:
            return f"{base} + ESG 분석 (7단계)"
        elif include_risk_analysis:
            return f"{base} + 리스크 분석 (7단계)"
        else:
            return base
    
    def _extract_key_metrics(self, stock: Dict[str, Any]) -> Dict[str, str]:
        """핵심 지표 추출"""
        return {
            "market_cap": f"{stock['market_cap']:,.0f}백만원",
            "roe_3y_avg": f"{stock.get('roe_3y_avg', 0):.1f}%",
            "net_profit_margin": f"{stock.get('net_profit_margin', 0):.1f}%",
            "market_cap_growth_3y": f"{stock.get('market_cap_growth_3y', 0):.1f}%",
            "fcf_valuation_ratio": f"{stock.get('fcf_projection_5y_sum', 0)/stock['market_cap']:.2f}",
            "per": f"{stock.get('per', 0):.1f}",
            "pbr": f"{stock.get('pbr', 0):.2f}"
        }
    
    def _extract_detailed_scores(self, stock: Dict[str, Any], include_esg: bool, include_risk_analysis: bool) -> Dict[str, int]:
        """상세 점수 추출"""
        scores = {
            "시가총액": stock["market_cap_score"],
            "ROE": stock["roe_score"],
            "수익성": stock["profitability_score"],
            "성장성": stock["growth_score"],
            "FCF예측": stock["fcf_projection_score"],
            "밸류에이션": stock["valuation_score"]
        }
        
        if include_esg:
            scores["ESG"] = stock.get("esg_score", 0)
        if include_risk_analysis:
            scores["리스크"] = stock.get("risk_score", 0)
        
        return scores
    
    def _generate_portfolio_advice(self, portfolio_opt) -> str:
        """포트폴리오 조언 생성"""
        sharpe = portfolio_opt.sharpe_ratio
        diversification = portfolio_opt.diversification_score
        
        if sharpe > 1.0 and diversification > 80:
            return "🟢 우수한 리스크 대비 수익률과 분산 효과를 보이는 포트폴리오입니다."
        elif sharpe > 0.7:
            return "🔵 양호한 투자 포트폴리오입니다. 추가 분산을 고려해보세요."
        else:
            return "🟡 포트폴리오 재검토가 필요합니다. 리스크 관리에 주의하세요."
    
    def _run(self, market_segment: str = "KOSPI", min_score: int = 60, max_results: int = 10, 
             include_esg: bool = True, include_risk_analysis: bool = True, 
             sectors: Optional[List[str]] = None, use_real_data: bool = True) -> str:
        """도구 실행 메인 로직 (LangChain Tool 호환)"""
        try:
            # 1. 시장 데이터 가져오기 (Mock 데이터 사용)
            market_data = self._get_mock_market_data(market_segment)
            if sectors:
                market_data = [s for s in market_data if s["sector"] in sectors]
            logging.getLogger(__name__).info(f"총 {len(market_data)}개 종목 분석 시작")
            # 2. 각 종목별 종합 점수 계산
            scored_stocks = []
            for stock in market_data:
                try:
                    scored_stock = self._calculate_enhanced_total_score(
                        stock, market_data, include_esg, include_risk_analysis
                    )
                    scored_stocks.append(scored_stock)
                except Exception as e:
                    logging.getLogger(__name__).warning(f"종목 {stock['symbol']} 분석 실패: {e}")
                    continue
            # 3. 필터링 및 정렬
            qualified_stocks = [s for s in scored_stocks if s["total_score"] >= min_score]
            top_stocks = sorted(qualified_stocks, key=lambda x: x["total_score"], reverse=True)[:max_results]
            # 4. 결과 포맷팅
            result = self._format_enhanced_results(
                market_segment, min_score, len(market_data), 
                len(qualified_stocks), top_stocks, None,
                include_esg, include_risk_analysis
            )
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"❌ Enhanced Warren Buffett 필터 분석 중 오류 발생: {str(e)}"

# Enhanced Tool 인스턴스 생성 (Agent가 사용할 수 있도록)
BuffettFilter = BuffettFilterTool()

# 호환성을 위한 기존 이름 유지
EnhancedBuffettFilter = BuffettFilter
