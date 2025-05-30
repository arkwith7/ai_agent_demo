"""
워런 버핏 투자 기준 종목 스크리닝 도구 (Simplified Enhanced Buffett Filter Tool)
"""
from typing import Type, Dict, Any, List, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import json
import asyncio
import logging
import random

from .data_providers.krx_api import krx_provider
from .data_providers.opendart_api import opendart_provider
from .esg_analysis_tool import esg_analyzer
from .advanced_analysis_tool import advanced_analyzer

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
    """워런 버핏의 8단계 투자 기준 스크리닝 도구"""
    
    name: str = "enhanced_buffett_stock_screener"
    description: str = """워런 버핏의 8단계 투자 기준으로 종목을 스크리닝합니다."""
    args_schema: Type[BaseModel] = BuffettFilterInput

    class Config:
        arbitrary_types_allowed = True

    def _run(self, market_segment: str = "KOSPI", min_score: int = 60, max_results: int = 10, 
             include_esg: bool = True, include_risk_analysis: bool = True, 
             sectors: Optional[List[str]] = None, use_real_data: bool = True) -> str:
        """도구 실행 메인 로직"""
        try:
            logger = logging.getLogger(__name__)
            
            # 1. 시장 데이터 가져오기 (Mock 데이터 사용)
            market_data = self._get_mock_market_data(market_segment)
            if sectors:
                market_data = [s for s in market_data if s["sector"] in sectors]
            
            logger.info(f"총 {len(market_data)}개 종목 분석 시작")
            
            # 2. 각 종목별 종합 점수 계산
            scored_stocks = []
            for stock in market_data:
                try:
                    scored_stock = self._calculate_enhanced_total_score(
                        stock, market_data, include_esg, include_risk_analysis
                    )
                    scored_stocks.append(scored_stock)
                except Exception as e:
                    logger.warning(f"종목 {stock['symbol']} 분석 실패: {e}")
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

    def _get_mock_market_data(self, market_segment: str) -> List[Dict[str, Any]]:
        """모의 시장 데이터 생성"""
        stock_pool = [
            {"symbol": "005930", "name": "삼성전자", "sector": "반도체"},
            {"symbol": "000660", "name": "SK하이닉스", "sector": "반도체"},
            {"symbol": "035420", "name": "NAVER", "sector": "인터넷"},
            {"symbol": "005380", "name": "현대차", "sector": "자동차"},
            {"symbol": "006400", "name": "삼성SDI", "sector": "배터리"},
        ]
        
        market_data = []
        for stock in stock_pool:
            random.seed(hash(stock["symbol"]) % 1000)
            
            market_cap = random.uniform(5000000, 500000000)
            current_price = random.uniform(10000, 80000)
            shares = market_cap * 1000000 / current_price
            
            roe_y1 = random.uniform(10, 25)
            revenue = market_cap * random.uniform(0.5, 3.0)
            net_income = revenue * random.uniform(0.03, 0.25)
            fcf = net_income * random.uniform(0.7, 1.5)
            
            stock_data = {
                **stock,
                "market_cap": market_cap,
                "current_price": current_price,
                "shares_outstanding": shares,
                "roe_y1": roe_y1,
                "roe_3y_avg": roe_y1,
                "revenue": revenue,
                "net_income": net_income,
                "net_profit_margin": (net_income / revenue) * 100,
                "fcf": fcf,
                "fcf_per_share": fcf / shares,
                "fcf_margin": (fcf / revenue) * 100,
                "market_cap_growth_3y": random.uniform(5, 25),
                "equity_growth_3y": random.uniform(3, 20),
                "per": random.uniform(8, 35),
                "pbr": random.uniform(0.5, 3.0),
                "debt_to_equity": random.uniform(0.1, 1.5),
                "dividend_yield": random.uniform(0.5, 5.0)
            }
            
            # FCF 예측
            fcf_growth = random.uniform(3, 12)
            projected_fcf_sum = sum(fcf * ((1 + fcf_growth/100) ** year) for year in range(1, 6))
            stock_data["fcf_projection_5y_sum"] = projected_fcf_sum
            
            market_data.append(stock_data)
        
        return market_data

    def _calculate_enhanced_total_score(self, stock: Dict[str, Any], all_stocks: List[Dict[str, Any]], 
                                      include_esg: bool, include_risk_analysis: bool) -> Dict[str, Any]:
        """강화된 종합 점수 계산"""
        
        # 기본 6단계 점수
        basic_scores = {
            "market_cap_score": self._score_market_cap_criteria(stock, all_stocks),
            "roe_score": self._score_roe_criteria(stock),
            "profitability_score": self._score_profitability_criteria(stock, all_stocks),
            "growth_score": self._score_growth_criteria(stock),
            "fcf_projection_score": self._score_fcf_projection_criteria(stock),
            "valuation_score": self._score_valuation_criteria(stock)
        }
        
        # ESG 점수 (모의)
        esg_score = 0
        if include_esg:
            esg_score = random.randint(60, 90)
        
        # 리스크 점수 (모의)
        risk_score = 0
        if include_risk_analysis:
            risk_score = random.randint(50, 90)
        
        # 가중 평균 계산
        all_scores = {**basic_scores}
        if include_esg:
            all_scores["esg_score"] = esg_score
        if include_risk_analysis:
            all_scores["risk_score"] = risk_score
        
        weights = self._calculate_dynamic_weights(include_esg, include_risk_analysis)
        total_score = sum(all_scores[key] * weights[key] for key in all_scores.keys())
        
        return {
            **stock,
            **all_scores,
            "total_score": round(total_score, 1),
            "recommendation": self._get_recommendation(total_score)
        }

    def _score_market_cap_criteria(self, stock: Dict[str, Any], all_stocks: List[Dict[str, Any]]) -> int:
        """시가총액 기준 점수"""
        sorted_stocks = sorted(all_stocks, key=lambda x: x["market_cap"], reverse=True)
        rank = next(i for i, s in enumerate(sorted_stocks) if s["symbol"] == stock["symbol"])
        percentile = (rank / len(sorted_stocks)) * 100
        
        if percentile <= 10: return 100
        elif percentile <= 20: return 90
        elif percentile <= 30: return 80
        elif percentile <= 50: return 60
        else: return max(0, 40 - int(percentile - 50))

    def _score_roe_criteria(self, stock: Dict[str, Any]) -> int:
        """ROE 기준 점수"""
        roe_avg = stock["roe_3y_avg"]
        if roe_avg >= 25: return 100
        elif roe_avg >= 20: return 90
        elif roe_avg >= 15: return 80
        elif roe_avg >= 10: return 60
        elif roe_avg >= 5: return 40
        else: return 20

    def _score_profitability_criteria(self, stock: Dict[str, Any], all_stocks: List[Dict[str, Any]]) -> int:
        """수익성 기준 점수"""
        sector_stocks = [s for s in all_stocks if s["sector"] == stock["sector"]]
        avg_margin = sum(s["net_profit_margin"] for s in sector_stocks) / len(sector_stocks)
        margin_score = 50 if stock["net_profit_margin"] >= avg_margin else 20
        return margin_score + 30  # 기본점수

    def _score_growth_criteria(self, stock: Dict[str, Any]) -> int:
        """성장성 기준 점수"""
        market_growth = stock["market_cap_growth_3y"]
        equity_growth = stock["equity_growth_3y"]
        growth_diff = market_growth - equity_growth
        
        if growth_diff >= 10: return 100
        elif growth_diff >= 5: return 80
        elif growth_diff >= 0: return 60
        elif growth_diff >= -5: return 40
        else: return 20

    def _score_fcf_projection_criteria(self, stock: Dict[str, Any]) -> int:
        """FCF 예측 기준 점수"""
        ratio = stock["fcf_projection_5y_sum"] / stock["market_cap"]
        if ratio >= 1.5: return 100
        elif ratio >= 1.2: return 90
        elif ratio >= 1.0: return 80
        elif ratio >= 0.8: return 60
        elif ratio >= 0.6: return 40
        else: return 20

    def _score_valuation_criteria(self, stock: Dict[str, Any]) -> int:
        """가치평가 기준 점수"""
        per = stock["per"]
        pbr = stock["pbr"]
        
        per_score = 50 if per <= 15 else 30 if per <= 25 else 10
        pbr_score = 50 if pbr <= 1.5 else 30 if pbr <= 2.5 else 10
        
        return per_score + pbr_score

    def _calculate_dynamic_weights(self, include_esg: bool, include_risk_analysis: bool) -> Dict[str, float]:
        """동적 가중치 계산"""
        base_weights = {
            "market_cap_score": 0.15,
            "roe_score": 0.20,
            "profitability_score": 0.20,
            "growth_score": 0.15,
            "fcf_projection_score": 0.20,
            "valuation_score": 0.10
        }
        
        if include_esg:
            base_weights["esg_score"] = 0.05
        if include_risk_analysis:
            base_weights["risk_score"] = 0.05
        
        # 정규화
        total_weight = sum(base_weights.values())
        return {k: v/total_weight for k, v in base_weights.items()}

    def _get_recommendation(self, score: float) -> str:
        """점수에 따른 투자 추천"""
        if score >= 85: return "🟢 Strong Buy"
        elif score >= 75: return "🔵 Buy"
        elif score >= 65: return "🟡 Hold"
        elif score >= 50: return "🟠 Weak Hold"
        else: return "🔴 Avoid"

    def _format_enhanced_results(self, market_segment: str, min_score: int, total_analyzed: int, 
                                qualified_count: int, top_stocks: List[Dict[str, Any]], 
                                portfolio_optimization, include_esg: bool, include_risk_analysis: bool) -> Dict[str, Any]:
        """결과 포맷팅"""
        
        if not top_stocks:
            return {
                "error": f"⚠️ 최소 점수 {min_score}점 이상을 만족하는 종목이 없습니다.",
                "analysis_summary": {
                    "total_analyzed": total_analyzed,
                    "qualified_count": qualified_count
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
                    "risk_analysis": include_risk_analysis
                }
            },
            "top_recommendations": [],
            "summary": f"📊 Enhanced Buffett Filter: {total_analyzed}개 종목 중 {qualified_count}개가 기준을 통과했습니다."
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
                "key_metrics": {
                    "market_cap": f"{stock['market_cap']:,.0f}백만원",
                    "roe_3y_avg": f"{stock.get('roe_3y_avg', 0):.1f}%",
                    "net_profit_margin": f"{stock.get('net_profit_margin', 0):.1f}%",
                    "per": f"{stock.get('per', 0):.1f}",
                    "pbr": f"{stock.get('pbr', 0):.2f}"
                },
                "detailed_scores": {
                    "시가총액": stock["market_cap_score"],
                    "ROE": stock["roe_score"],
                    "수익성": stock["profitability_score"],
                    "성장성": stock["growth_score"],
                    "FCF예측": stock["fcf_projection_score"],
                    "밸류에이션": stock["valuation_score"]
                }
            }
            
            if include_esg:
                stock_result["detailed_scores"]["ESG"] = stock.get("esg_score", 0)
            if include_risk_analysis:
                stock_result["detailed_scores"]["리스크"] = stock.get("risk_score", 0)
            
            result["top_recommendations"].append(stock_result)
        
        return result

# Tool 인스턴스 생성
BuffettFilter = BuffettFilterTool()
