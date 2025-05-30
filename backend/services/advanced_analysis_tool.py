"""
고급 투자 분석 도구
- 포트폴리오 최적화
- 리스크 분석
- 상관관계 분석
- 시나리오 분석
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
import asyncio
import logging
from datetime import datetime, timedelta
import random
import math

from .data_providers.krx_api import KRXDataProvider
from .data_providers.opendart_api import OpenDARTProvider

logger = logging.getLogger(__name__)

@dataclass
class PortfolioOptimization:
    """포트폴리오 최적화 결과"""
    recommended_weights: Dict[str, float]
    expected_return: float
    expected_risk: float
    sharpe_ratio: float
    max_drawdown: float
    diversification_score: float

@dataclass
class RiskAnalysis:
    """리스크 분석 결과"""
    beta: float
    value_at_risk: float  # VaR 95%
    expected_shortfall: float  # ES 95%
    volatility: float
    downside_risk: float
    risk_grade: str

@dataclass
class MarketScenario:
    """시장 시나리오"""
    scenario_name: str
    probability: float
    market_impact: float
    sector_impacts: Dict[str, float]
    expected_returns: Dict[str, float] = None
    
    def __post_init__(self):
        """초기화 후 처리"""
        if self.expected_returns is None:
            # sector_impacts 기반으로 expected_returns 계산
            self.expected_returns = {
                sector: self.market_impact + impact 
                for sector, impact in self.sector_impacts.items()
            }

class AdvancedAnalysisTool:
    """고급 투자 분석 도구"""
    
    def __init__(self):
        self.krx_provider = KRXDataProvider()
        self.opendart_provider = OpenDARTProvider()
        self.market_scenarios = self._define_market_scenarios()
    
    async def optimize_portfolio(self, stock_list: List[Dict[str, Any]], investment_amount: float = 1000000000) -> PortfolioOptimization:
        """포트폴리오 최적화 (Modern Portfolio Theory 기반)"""
        try:
            if len(stock_list) < 2:
                return self._create_single_stock_portfolio(stock_list[0], investment_amount)
            
            # 1. 과거 수익률 데이터 수집 (Mock)
            returns_matrix = self._generate_historical_returns(stock_list)
            
            # 2. 기대수익률 및 공분산 행렬 계산
            expected_returns = np.mean(returns_matrix, axis=1)
            cov_matrix = np.cov(returns_matrix)
            
            # 3. 효율적 프론티어 계산
            optimal_weights = self._calculate_optimal_weights(expected_returns, cov_matrix)
            
            # 4. 포트폴리오 성과 지표 계산
            portfolio_return = np.dot(optimal_weights, expected_returns) * 252  # 연환산
            portfolio_risk = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights))) * np.sqrt(252)
            sharpe_ratio = portfolio_return / portfolio_risk if portfolio_risk > 0 else 0
            
            # 5. 최대 낙폭 계산
            max_drawdown = self._calculate_max_drawdown(optimal_weights, returns_matrix)
            
            # 6. 다각화 점수 계산
            diversification_score = self._calculate_diversification_score(optimal_weights, stock_list)
            
            # 7. 투자 금액별 주식 수 계산
            recommended_weights = {}
            for i, stock in enumerate(stock_list):
                weight = optimal_weights[i]
                symbol = stock["symbol"]
                recommended_weights[symbol] = {
                    "weight": weight,
                    "amount": investment_amount * weight,
                    "shares": int((investment_amount * weight) / stock["current_price"]),
                    "name": stock["name"]
                }
            
            return PortfolioOptimization(
                recommended_weights=recommended_weights,
                expected_return=portfolio_return,
                expected_risk=portfolio_risk,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                diversification_score=diversification_score
            )
        
        except Exception as e:
            logger.error(f"포트폴리오 최적화 중 오류: {e}")
            return self._create_equal_weight_portfolio(stock_list, investment_amount)
    
    async def analyze_risk(self, stock: Dict[str, Any], market_data: List[Dict[str, Any]]) -> RiskAnalysis:
        """개별 종목 리스크 분석"""
        try:
            symbol = stock["symbol"]
            
            # 1. 베타 계산 (시장 대비 민감도)
            stock_returns = self._generate_stock_returns(symbol)
            market_returns = self._generate_market_returns()
            beta = self._calculate_beta(stock_returns, market_returns)
            
            # 2. VaR 및 ES 계산
            var_95 = np.percentile(stock_returns, 5)  # 5% VaR
            es_95 = np.mean(stock_returns[stock_returns <= var_95])  # Expected Shortfall
            
            # 3. 변동성 지표
            volatility = np.std(stock_returns) * np.sqrt(252)  # 연환산 변동성
            downside_returns = stock_returns[stock_returns < 0]
            downside_risk = np.std(downside_returns) * np.sqrt(252) if len(downside_returns) > 0 else 0
            
            # 4. 리스크 등급 산정
            risk_grade = self._classify_risk_grade(volatility, beta, var_95)
            
            return RiskAnalysis(
                beta=beta,
                value_at_risk=var_95,
                expected_shortfall=es_95,
                volatility=volatility,
                downside_risk=downside_risk,
                risk_grade=risk_grade
            )
        
        except Exception as e:
            logger.error(f"리스크 분석 중 오류 ({stock['symbol']}): {e}")
            return self._generate_mock_risk_analysis(stock)
    
    async def scenario_analysis(self, stock_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """시나리오 분석"""
        try:
            scenario_results = {}
            
            for scenario in self.market_scenarios:
                scenario_returns = {}
                portfolio_impact = 0
                
                for stock in stock_list:
                    sector = stock["sector"]
                    base_return = stock.get("expected_return", 0.08)  # 기본 8% 수익률
                    
                    # 시나리오별 수익률 조정
                    market_impact = scenario.market_impact
                    sector_impact = scenario.sector_impacts.get(sector, 0)
                    scenario_return = base_return * (1 + market_impact + sector_impact)
                    
                    scenario_returns[stock["symbol"]] = {
                        "return": scenario_return,
                        "impact": scenario_return - base_return,
                        "name": stock["name"]
                    }
                    
                    # 동일 가중 포트폴리오 가정
                    portfolio_impact += scenario_return / len(stock_list)
                
                scenario_results[scenario.scenario_name] = {
                    "probability": scenario.probability,
                    "portfolio_return": portfolio_impact,
                    "individual_returns": scenario_returns,
                    "description": self._get_scenario_description(scenario)
                }
            
            # 기대수익률 계산 (확률 가중)
            expected_portfolio_return = sum(
                result["portfolio_return"] * result["probability"]
                for result in scenario_results.values()
            )
            
            return {
                "scenarios": scenario_results,
                "expected_return": expected_portfolio_return,
                "best_case": max(scenario_results.items(), key=lambda x: x[1]["portfolio_return"]),
                "worst_case": min(scenario_results.items(), key=lambda x: x[1]["portfolio_return"]),
                "base_case": scenario_results.get("기본 시나리오", {})
            }
        
        except Exception as e:
            logger.error(f"시나리오 분석 중 오류: {e}")
            return {"error": str(e)}
    
    async def correlation_analysis(self, stock_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """상관관계 분석"""
        try:
            if len(stock_list) < 2:
                return {"message": "상관관계 분석을 위해서는 최소 2개 종목이 필요합니다."}
            
            # 수익률 매트릭스 생성
            returns_matrix = self._generate_historical_returns(stock_list)
            correlation_matrix = np.corrcoef(returns_matrix)
            
            # 상관관계 결과 정리
            correlations = {}
            high_correlations = []
            low_correlations = []
            
            for i, stock1 in enumerate(stock_list):
                correlations[stock1["symbol"]] = {}
                for j, stock2 in enumerate(stock_list):
                    if i != j:
                        corr_value = correlation_matrix[i, j]
                        correlations[stock1["symbol"]][stock2["symbol"]] = {
                            "correlation": corr_value,
                            "name1": stock1["name"],
                            "name2": stock2["name"]
                        }
                        
                        # 높은/낮은 상관관계 식별
                        if abs(corr_value) > 0.7 and i < j:  # 중복 제거
                            high_correlations.append({
                                "stock1": stock1["name"],
                                "stock2": stock2["name"],
                                "correlation": corr_value
                            })
                        elif abs(corr_value) < 0.3 and i < j:
                            low_correlations.append({
                                "stock1": stock1["name"],
                                "stock2": stock2["name"],
                                "correlation": corr_value
                            })
            
            # 포트폴리오 다각화 효과 계산
            avg_correlation = np.mean(correlation_matrix[np.triu_indices_from(correlation_matrix, k=1)])
            diversification_benefit = max(0, (1 - avg_correlation) * 100)
            
            return {
                "correlation_matrix": correlations,
                "average_correlation": avg_correlation,
                "high_correlations": sorted(high_correlations, key=lambda x: abs(x["correlation"]), reverse=True),
                "low_correlations": sorted(low_correlations, key=lambda x: abs(x["correlation"])),
                "diversification_benefit": diversification_benefit,
                "recommendation": self._get_diversification_recommendation(avg_correlation)
            }
        
        except Exception as e:
            logger.error(f"상관관계 분석 중 오류: {e}")
            return {"error": str(e)}
    
    def _generate_historical_returns(self, stock_list: List[Dict[str, Any]], days: int = 252) -> np.ndarray:
        """과거 수익률 데이터 생성 (Mock)"""
        returns_matrix = []
        
        for stock in stock_list:
            symbol = stock["symbol"]
            # 종목별 특성 반영한 수익률 생성
            random.seed(hash(symbol) % 1000)
            
            # 기본 파라미터
            annual_return = random.uniform(0.05, 0.20)  # 5-20% 연수익률
            volatility = random.uniform(0.15, 0.40)     # 15-40% 변동성
            
            # 일일 수익률 생성 (정규분포 가정)
            daily_returns = np.random.normal(
                annual_return / 252,  # 일평균 수익률
                volatility / np.sqrt(252),  # 일변동성
                days
            )
            
            returns_matrix.append(daily_returns)
        
        return np.array(returns_matrix)
    
    def _calculate_optimal_weights(self, expected_returns: np.ndarray, cov_matrix: np.ndarray) -> np.ndarray:
        """최적 포트폴리오 가중치 계산 (최소분산 포트폴리오)"""
        n = len(expected_returns)
        
        # 제약조건: 가중치 합 = 1, 모든 가중치 >= 0
        try:
            # 역공분산 행렬
            inv_cov = np.linalg.inv(cov_matrix)
            ones = np.ones((n, 1))
            
            # 최소분산 포트폴리오 가중치
            weights = np.dot(inv_cov, ones) / np.dot(ones.T, np.dot(inv_cov, ones))
            weights = weights.flatten()
            
            # 음수 가중치 처리 (절댓값 후 정규화)
            weights = np.abs(weights)
            weights = weights / np.sum(weights)
            
            return weights
        
        except np.linalg.LinAlgError:
            # 역행렬 계산 실패 시 동일 가중치 반환
            return np.ones(n) / n
    
    def _calculate_max_drawdown(self, weights: np.ndarray, returns_matrix: np.ndarray) -> float:
        """최대 낙폭 계산"""
        portfolio_returns = np.dot(weights, returns_matrix)
        cumulative_returns = np.cumprod(1 + portfolio_returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max
        return abs(np.min(drawdown))
    
    def _calculate_diversification_score(self, weights: np.ndarray, stock_list: List[Dict[str, Any]]) -> float:
        """다각화 점수 계산"""
        # 1. 가중치 분산도 (가중치가 고르게 분포될수록 높은 점수)
        weight_entropy = -np.sum(weights * np.log(weights + 1e-10))
        max_entropy = np.log(len(weights))
        weight_score = weight_entropy / max_entropy * 100
        
        # 2. 섹터 다각화 점수
        sectors = [stock["sector"] for stock in stock_list]
        unique_sectors = len(set(sectors))
        sector_score = min(100, (unique_sectors / 5) * 100)  # 5개 섹터를 만점으로
        
        # 3. 종합 점수
        diversification_score = (weight_score * 0.6 + sector_score * 0.4)
        return diversification_score
    
    def _generate_stock_returns(self, symbol: str, days: int = 252) -> np.ndarray:
        """개별 종목 수익률 생성"""
        random.seed(hash(symbol) % 1000)
        annual_return = random.uniform(0.05, 0.25)
        volatility = random.uniform(0.20, 0.50)
        
        return np.random.normal(
            annual_return / 252,
            volatility / np.sqrt(252),
            days
        )
    
    def _generate_market_returns(self, days: int = 252) -> np.ndarray:
        """시장 수익률 생성 (KOSPI 기준)"""
        return np.random.normal(0.08 / 252, 0.18 / np.sqrt(252), days)
    
    def _calculate_beta(self, stock_returns: np.ndarray, market_returns: np.ndarray) -> float:
        """베타 계산"""
        covariance = np.cov(stock_returns, market_returns)[0, 1]
        market_variance = np.var(market_returns)
        return covariance / market_variance if market_variance > 0 else 1.0
    
    def _classify_risk_grade(self, volatility: float, beta: float, var: float) -> str:
        """리스크 등급 분류"""
        risk_score = 0
        
        # 변동성 점수
        if volatility > 0.4:
            risk_score += 3
        elif volatility > 0.25:
            risk_score += 2
        else:
            risk_score += 1
        
        # 베타 점수
        if abs(beta) > 1.5:
            risk_score += 3
        elif abs(beta) > 1.0:
            risk_score += 2
        else:
            risk_score += 1
        
        # VaR 점수
        if abs(var) > 0.05:
            risk_score += 3
        elif abs(var) > 0.03:
            risk_score += 2
        else:
            risk_score += 1
        
        if risk_score >= 8:
            return "High Risk"
        elif risk_score >= 6:
            return "Medium Risk"
        else:
            return "Low Risk"
    
    def _define_market_scenarios(self) -> List[MarketScenario]:
        """시장 시나리오 정의"""
        return [
            MarketScenario(
                scenario_name="기본 시나리오",
                probability=0.4,
                market_impact=0.0,
                sector_impacts={
                    "반도체": 0.05, "자동차": 0.02, "바이오": 0.08,
                    "화학": -0.02, "인터넷": 0.10, "금융": 0.03
                }
            ),
            MarketScenario(
                scenario_name="경제 호황",
                probability=0.25,
                market_impact=0.15,
                sector_impacts={
                    "반도체": 0.20, "자동차": 0.18, "바이오": 0.12,
                    "화학": 0.10, "인터넷": 0.25, "금융": 0.15
                }
            ),
            MarketScenario(
                scenario_name="경제 침체",
                probability=0.25,
                market_impact=-0.20,
                sector_impacts={
                    "반도체": -0.25, "자동차": -0.30, "바이오": -0.10,
                    "화학": -0.35, "인터넷": -0.15, "금융": -0.40
                }
            ),
            MarketScenario(
                scenario_name="금리 급등",
                probability=0.1,
                market_impact=-0.15,
                sector_impacts={
                    "반도체": -0.10, "자동차": -0.20, "바이오": -0.25,
                    "화학": -0.15, "인터넷": -0.30, "금융": 0.10
                }
            )
        ]
    
    def _get_scenario_description(self, scenario: MarketScenario) -> str:
        """시나리오 설명"""
        descriptions = {
            "기본 시나리오": "현재 경제 상황이 지속되는 경우",
            "경제 호황": "GDP 성장률 상승, 기업 실적 개선이 지속되는 경우",
            "경제 침체": "글로벌 경기 둔화, 무역 분쟁 확산 등의 부정적 요인",
            "금리 급등": "인플레이션 압력으로 인한 급격한 금리 인상"
        }
        return descriptions.get(scenario.scenario_name, "")
    
    def _get_diversification_recommendation(self, avg_correlation: float) -> str:
        """다각화 권고사항"""
        if avg_correlation > 0.7:
            return "높은 상관관계로 인해 다각화 효과가 제한적입니다. 다른 섹터나 자산군 추가를 고려하세요."
        elif avg_correlation > 0.4:
            return "적정 수준의 다각화가 이루어져 있습니다. 추가적인 섹터 분산을 고려할 수 있습니다."
        else:
            return "우수한 다각화 효과를 보이고 있습니다. 현재 포트폴리오 구성이 적절합니다."
    
    def _create_single_stock_portfolio(self, stock: Dict[str, Any], investment_amount: float) -> PortfolioOptimization:
        """단일 종목 포트폴리오"""
        return PortfolioOptimization(
            recommended_weights={
                stock["symbol"]: {
                    "weight": 1.0,
                    "amount": investment_amount,
                    "shares": int(investment_amount / stock["current_price"]),
                    "name": stock["name"]
                }
            },
            expected_return=0.12,  # 기본 12%
            expected_risk=0.25,    # 기본 25%
            sharpe_ratio=0.48,
            max_drawdown=0.20,
            diversification_score=0  # 단일 종목이므로 0
        )
    
    def _create_equal_weight_portfolio(self, stock_list: List[Dict[str, Any]], investment_amount: float) -> PortfolioOptimization:
        """동일 가중 포트폴리오"""
        n_stocks = len(stock_list)
        weight_per_stock = 1.0 / n_stocks
        
        recommended_weights = {}
        for stock in stock_list:
            amount = investment_amount * weight_per_stock
            recommended_weights[stock["symbol"]] = {
                "weight": weight_per_stock,
                "amount": amount,
                "shares": int(amount / stock["current_price"]),
                "name": stock["name"]
            }
        
        return PortfolioOptimization(
            recommended_weights=recommended_weights,
            expected_return=0.10,
            expected_risk=0.18,
            sharpe_ratio=0.56,
            max_drawdown=0.15,
            diversification_score=75.0
        )
    
    def _generate_mock_risk_analysis(self, stock: Dict[str, Any]) -> RiskAnalysis:
        """Mock 리스크 분석"""
        random.seed(hash(stock["symbol"]) % 1000)
        
        beta = random.uniform(0.5, 1.8)
        volatility = random.uniform(0.15, 0.45)
        var_95 = -random.uniform(0.02, 0.08)
        
        return RiskAnalysis(
            beta=beta,
            value_at_risk=var_95,
            expected_shortfall=var_95 * 1.3,
            volatility=volatility,
            downside_risk=volatility * 0.7,
            risk_grade=self._classify_risk_grade(volatility, beta, var_95)
        )

# 싱글톤 인스턴스
advanced_analyzer = AdvancedAnalysisTool()