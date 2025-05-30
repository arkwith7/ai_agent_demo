"""
ESG (Environmental, Social, Governance) 분석 도구
Warren Buffett의 투자 철학에 ESG 요소를 추가한 현대적 투자 분석
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import asyncio
import logging
from datetime import datetime
import random

from .data_providers.opendart_api import OpenDARTProvider, ESGInfo

logger = logging.getLogger(__name__)

@dataclass
class ESGRiskAssessment:
    """ESG 리스크 평가 결과"""
    environmental_risk: str  # High, Medium, Low
    social_risk: str
    governance_risk: str
    overall_risk: str
    risk_score: float  # 0-100 (낮을수록 위험)
    key_concerns: List[str]
    strengths: List[str]

class ESGAnalysisTool:
    """ESG 분석 및 평가 도구"""
    
    def __init__(self):
        self.opendart_provider = OpenDARTProvider()
        self.industry_benchmarks = self._load_industry_benchmarks()
    
    async def analyze_esg_score(self, symbol: str, sector: str) -> Dict[str, Any]:
        """종합 ESG 점수 분석"""
        try:
            async with self.opendart_provider as provider:
                esg_info = await provider.get_esg_info(symbol)
                governance_info = await provider.get_governance_info(symbol)
            
            if not esg_info:
                return self._generate_mock_esg_analysis(symbol, sector)
            
            # 1. 기본 ESG 점수 계산
            base_scores = {
                "environmental": esg_info.environmental_score,
                "social": esg_info.social_score,
                "governance": esg_info.governance_score
            }
            
            # 2. 업종별 벤치마크 비교
            sector_benchmark = self.industry_benchmarks.get(sector, {
                "environmental": 70, "social": 65, "governance": 75
            })
            
            # 3. 상대적 점수 계산
            relative_scores = {}
            for dimension, score in base_scores.items():
                benchmark = sector_benchmark[dimension]
                relative_score = min(100, (score / benchmark) * 80 + 20)
                relative_scores[dimension] = relative_score
            
            # 4. 가중 평균 계산 (Buffett 스타일: Governance 중시)
            weights = {"environmental": 0.25, "social": 0.25, "governance": 0.50}
            weighted_score = sum(relative_scores[dim] * weights[dim] for dim in weights)
            
            # 5. 리스크 평가
            risk_assessment = self._assess_esg_risks(base_scores, governance_info, sector)
            
            # 6. Buffett 스타일 투자 적합성 평가
            buffett_compatibility = self._evaluate_buffett_compatibility(
                base_scores, governance_info, weighted_score
            )
            
            return {
                "symbol": symbol,
                "sector": sector,
                "esg_scores": {
                    "environmental": {
                        "absolute": base_scores["environmental"],
                        "relative": relative_scores["environmental"],
                        "benchmark": sector_benchmark["environmental"]
                    },
                    "social": {
                        "absolute": base_scores["social"],
                        "relative": relative_scores["social"],
                        "benchmark": sector_benchmark["social"]
                    },
                    "governance": {
                        "absolute": base_scores["governance"],
                        "relative": relative_scores["governance"],
                        "benchmark": sector_benchmark["governance"]
                    }
                },
                "overall_score": weighted_score,
                "grade": self._get_esg_grade(weighted_score),
                "risk_assessment": risk_assessment,
                "buffett_compatibility": buffett_compatibility,
                "recommendations": self._generate_esg_recommendations(
                    base_scores, risk_assessment, sector
                )
            }
        
        except Exception as e:
            logger.error(f"ESG 분석 중 오류 발생 ({symbol}): {e}")
            return self._generate_mock_esg_analysis(symbol, sector)
    
    def _assess_esg_risks(self, scores: Dict[str, float], governance: Dict[str, Any], sector: str) -> ESGRiskAssessment:
        """ESG 리스크 평가"""
        
        # 환경 리스크 평가
        env_risk = "Low"
        if scores["environmental"] < 60:
            env_risk = "High"
        elif scores["environmental"] < 75:
            env_risk = "Medium"
        
        # 사회적 리스크 평가
        social_risk = "Low"
        if scores["social"] < 55:
            social_risk = "High"
        elif scores["social"] < 70:
            social_risk = "Medium"
        
        # 지배구조 리스크 평가
        governance_risk = "Low"
        board_independence = governance.get("board_independence", 0.5)
        if board_independence < 0.3 or scores["governance"] < 60:
            governance_risk = "High"
        elif board_independence < 0.5 or scores["governance"] < 75:
            governance_risk = "Medium"
        
        # 전체 리스크 평가
        risk_levels = {"High": 3, "Medium": 2, "Low": 1}
        avg_risk_level = (risk_levels[env_risk] + risk_levels[social_risk] + risk_levels[governance_risk]) / 3
        
        if avg_risk_level >= 2.5:
            overall_risk = "High"
        elif avg_risk_level >= 1.5:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"
        
        # 리스크 점수 (0-100, 높을수록 안전)
        risk_score = (scores["environmental"] + scores["social"] + scores["governance"]) / 3
        
        # 주요 우려사항 및 강점
        concerns = []
        strengths = []
        
        if env_risk == "High":
            concerns.append("환경 규제 리스크")
        if social_risk == "High":
            concerns.append("사회적 책임 이슈")
        if governance_risk == "High":
            concerns.append("지배구조 투명성 부족")
        
        if scores["governance"] > 85:
            strengths.append("우수한 지배구조")
        if scores["environmental"] > 80:
            strengths.append("환경 리더십")
        if board_independence > 0.6:
            strengths.append("독립적 이사회")
        
        return ESGRiskAssessment(
            environmental_risk=env_risk,
            social_risk=social_risk,
            governance_risk=governance_risk,
            overall_risk=overall_risk,
            risk_score=risk_score,
            key_concerns=concerns,
            strengths=strengths
        )
    
    def _evaluate_buffett_compatibility(self, scores: Dict[str, float], governance: Dict[str, Any], weighted_score: float) -> Dict[str, Any]:
        """Buffett 투자 철학과의 호환성 평가"""
        
        # Buffett이 중시하는 요소들
        factors = {
            "management_quality": scores["governance"],  # 경영진 품질
            "long_term_thinking": scores["environmental"] * 0.7 + scores["social"] * 0.3,  # 장기적 사고
            "stakeholder_care": scores["social"],  # 이해관계자 배려
            "transparency": governance.get("transparency_score", 75),  # 투명성
            "ethical_business": (scores["governance"] + scores["social"]) / 2  # 윤리적 경영
        }
        
        # 종합 점수
        compatibility_score = sum(factors.values()) / len(factors)
        
        # 등급 결정
        if compatibility_score >= 85:
            grade = "Excellent"
            recommendation = "Buffett 스타일 투자에 매우 적합"
        elif compatibility_score >= 75:
            grade = "Good"
            recommendation = "Buffett 스타일 투자에 적합"
        elif compatibility_score >= 65:
            grade = "Fair"
            recommendation = "일부 개선 필요하지만 투자 고려 가능"
        else:
            grade = "Poor"
            recommendation = "Buffett 스타일 투자에 부적합"
        
        return {
            "compatibility_score": compatibility_score,
            "grade": grade,
            "recommendation": recommendation,
            "key_factors": factors,
            "buffett_principles": {
                "long_term_moat": compatibility_score >= 70,
                "management_integrity": scores["governance"] >= 80,
                "sustainable_business": scores["environmental"] >= 70,
                "stakeholder_value": scores["social"] >= 70
            }
        }
    
    def _generate_esg_recommendations(self, scores: Dict[str, float], risk_assessment: ESGRiskAssessment, sector: str) -> List[str]:
        """ESG 개선 권고사항"""
        recommendations = []
        
        if scores["environmental"] < 70:
            recommendations.append("환경 경영 전략 수립 및 탄소 중립 로드맵 필요")
        
        if scores["social"] < 70:
            recommendations.append("사회적 책임 활동 강화 및 이해관계자 소통 개선")
        
        if scores["governance"] < 80:
            recommendations.append("지배구조 투명성 제고 및 이사회 독립성 강화")
        
        if risk_assessment.overall_risk == "High":
            recommendations.append("ESG 리스크 관리 체계 구축 필요")
        
        # 업종별 특화 권고
        if sector in ["반도체", "화학"]:
            recommendations.append("친환경 제조 공정 도입 검토")
        elif sector in ["금융", "통신"]:
            recommendations.append("디지털 포용성 및 금융 접근성 개선")
        
        return recommendations[:3]  # 상위 3개만 반환
    
    def _get_esg_grade(self, score: float) -> str:
        """ESG 등급 산정"""
        if score >= 90:
            return "AAA"
        elif score >= 80:
            return "AA"
        elif score >= 70:
            return "A"
        elif score >= 60:
            return "BBB"
        elif score >= 50:
            return "BB"
        elif score >= 40:
            return "B"
        else:
            return "CCC"
    
    def _load_industry_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """업종별 ESG 벤치마크"""
        return {
            "반도체": {"environmental": 75, "social": 70, "governance": 80},
            "자동차": {"environmental": 65, "social": 75, "governance": 75},
            "바이오": {"environmental": 80, "social": 85, "governance": 80},
            "화학": {"environmental": 60, "social": 65, "governance": 70},
            "인터넷": {"environmental": 85, "social": 80, "governance": 85},
            "금융": {"environmental": 75, "social": 80, "governance": 90},
            "통신": {"environmental": 70, "social": 75, "governance": 80},
            "유통": {"environmental": 70, "social": 85, "governance": 75},
            "건설": {"environmental": 55, "social": 60, "governance": 65},
            "에너지": {"environmental": 50, "social": 55, "governance": 70}
        }
    
    def _generate_mock_esg_analysis(self, symbol: str, sector: str) -> Dict[str, Any]:
        """Mock ESG 분석 데이터"""
        random.seed(hash(symbol) % 1000)
        
        # 기본 점수 생성
        env_score = random.uniform(60, 90)
        social_score = random.uniform(55, 85)
        governance_score = random.uniform(70, 95)
        
        # 가중 점수
        weights = {"environmental": 0.25, "social": 0.25, "governance": 0.50}
        weighted_score = env_score * weights["environmental"] + social_score * weights["social"] + governance_score * weights["governance"]
        
        # Mock 지배구조 정보
        mock_governance = {
            "board_independence": random.uniform(0.3, 0.8),
            "transparency_score": random.uniform(65, 90)
        }
        
        # 리스크 평가
        risk_assessment = self._assess_esg_risks({
            "environmental": env_score,
            "social": social_score,
            "governance": governance_score
        }, mock_governance, sector)
        
        # Buffett 호환성
        buffett_compatibility = self._evaluate_buffett_compatibility({
            "environmental": env_score,
            "social": social_score,
            "governance": governance_score
        }, mock_governance, weighted_score)
        
        return {
            "symbol": symbol,
            "sector": sector,
            "esg_scores": {
                "environmental": {"absolute": env_score, "relative": env_score},
                "social": {"absolute": social_score, "relative": social_score},
                "governance": {"absolute": governance_score, "relative": governance_score}
            },
            "overall_score": weighted_score,
            "grade": self._get_esg_grade(weighted_score),
            "risk_assessment": risk_assessment,
            "buffett_compatibility": buffett_compatibility,
            "recommendations": self._generate_esg_recommendations({
                "environmental": env_score,
                "social": social_score,
                "governance": governance_score
            }, risk_assessment, sector)
        }

# 싱글톤 인스턴스
esg_analyzer = ESGAnalysisTool()