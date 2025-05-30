from typing import Type, Dict, Any, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import json
import random
import math

class ValuationToolInput(BaseModel):
    """Input for ValuationTool"""
    stock_symbol: str = Field(description="Stock symbol to value (e.g., '005930' for Samsung)")
    discount_rate: float = Field(default=8.0, description="Discount rate for DCF calculation (default: 8%)")

class ValuationTool(BaseTool):
    """
    5년 FCF 예측 및 DCF 기반 기업 가치 평가 도구
    """
    name: str = "dcf_valuation"
    description: str = """
    DCF(현금흐름할인법) 모델을 사용하여 기업의 내재가치를 계산합니다.
    5년간 FCF 예측, 터미널 가치 계산, 현재가치 할인을 통해 적정주가를 산출합니다.
    
    입력: stock_symbol (종목코드), discount_rate (할인율, 기본값 8%)
    출력: 내재가치, 현재주가 대비 상승/하락 여력, 투자 추천
    """
    args_schema: Type[BaseModel] = ValuationToolInput
    
    def _get_company_name(self, symbol: str) -> str:
        """종목코드에서 회사명 추출"""
        company_names = {
            "005930": "삼성전자",
            "000660": "SK하이닉스", 
            "035420": "NAVER",
            "005380": "현대차",
            "006400": "삼성SDI",
            "207940": "삼성바이오로직스",
            "068270": "셀트리온",
            "035720": "카카오",
            "051910": "LG화학",
            "012330": "현대모비스"
        }
        return company_names.get(symbol, f"기업_{symbol}")
    
    def _get_mock_financial_data(self, symbol: str) -> Dict[str, Any]:
        """모의 재무 데이터 생성"""
        # 종목별 고정 시드로 일관된 데이터 생성
        random.seed(hash(symbol) % 1000)
        
        return {
            "symbol": symbol,
            "company_name": self._get_company_name(symbol),
            "current_price": random.uniform(30000, 80000),
            "shares_outstanding": random.uniform(500000, 8000000),  # 천주 단위
            "current_fcf": random.uniform(2000000, 15000000),  # 백만원 단위
            "revenue": random.uniform(20000000, 300000000),
            "fcf_margin": random.uniform(5.0, 25.0),  # FCF/매출 비율
            "growth_rate_1_3": random.uniform(5.0, 15.0),  # 1-3년 성장률
            "growth_rate_4_5": random.uniform(3.0, 8.0),   # 4-5년 성장률
            "terminal_growth": random.uniform(2.0, 4.0),   # 영구성장률
            "debt": random.uniform(5000000, 30000000),     # 순부채
            "cash": random.uniform(3000000, 20000000),     # 현금성 자산
        }
    
    def _project_fcf(self, data: Dict[str, Any], years: int = 5) -> List[Dict[str, Any]]:
        """5년간 FCF 예측"""
        current_fcf = data["current_fcf"]
        growth_1_3 = data["growth_rate_1_3"] / 100
        growth_4_5 = data["growth_rate_4_5"] / 100
        
        projections = []
        fcf = current_fcf
        
        for year in range(1, years + 1):
            # 1-3년차는 높은 성장률, 4-5년차는 낮은 성장률
            growth_rate = growth_1_3 if year <= 3 else growth_4_5
            fcf = fcf * (1 + growth_rate)
            
            projections.append({
                "year": year,
                "fcf": fcf,
                "growth_rate": growth_rate * 100
            })
        
        return projections
    
    def _calculate_terminal_value(self, final_fcf: float, terminal_growth: float, discount_rate: float) -> float:
        """터미널 가치 계산"""
        # Gordon Growth Model: TV = FCF * (1 + g) / (r - g)
        return (final_fcf * (1 + terminal_growth / 100)) / ((discount_rate / 100) - (terminal_growth / 100))
    
    def _calculate_present_value(self, future_value: float, year: int, discount_rate: float) -> float:
        """현재가치 계산"""
        return future_value / ((1 + discount_rate / 100) ** year)
    
    def _calculate_dcf_value(self, data: Dict[str, Any], discount_rate: float) -> Dict[str, Any]:
        """DCF 기업가치 계산"""
        # 5년간 FCF 예측
        fcf_projections = self._project_fcf(data)
        
        # 각 년도별 FCF 현재가치 계산
        pv_fcf_list = []
        for proj in fcf_projections:
            pv = self._calculate_present_value(proj["fcf"], proj["year"], discount_rate)
            pv_fcf_list.append({
                "year": proj["year"],
                "fcf": proj["fcf"],
                "present_value": pv
            })
        
        # 터미널 가치 계산
        final_fcf = fcf_projections[-1]["fcf"]
        terminal_value = self._calculate_terminal_value(final_fcf, data["terminal_growth"], discount_rate)
        pv_terminal_value = self._calculate_present_value(terminal_value, 5, discount_rate)
        
        # 기업가치 = FCF 현재가치 합계 + 터미널 가치 현재가치
        total_pv_fcf = sum(pv["present_value"] for pv in pv_fcf_list)
        enterprise_value = total_pv_fcf + pv_terminal_value
        
        # 주주가치 = 기업가치 + 현금 - 순부채
        equity_value = enterprise_value + data["cash"] - data["debt"]
        
        # 주당 가치
        value_per_share = equity_value / (data["shares_outstanding"] * 1000)  # 천주 -> 주
        
        return {
            "fcf_projections": pv_fcf_list,
            "terminal_value": terminal_value,
            "pv_terminal_value": pv_terminal_value,
            "total_pv_fcf": total_pv_fcf,
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "value_per_share": value_per_share,
            "discount_rate": discount_rate
        }
    
    def _analyze_valuation(self, current_price: float, intrinsic_value: float) -> Dict[str, Any]:
        """밸류에이션 분석"""
        price_diff = intrinsic_value - current_price
        price_diff_pct = (price_diff / current_price) * 100
        
        if price_diff_pct >= 20:
            valuation_status = "🟢 상당한 저평가"
            recommendation = "Strong Buy"
            comment = "내재가치 대비 20% 이상 저평가, 매수 기회"
        elif price_diff_pct >= 10:
            valuation_status = "🔵 저평가"
            recommendation = "Buy"
            comment = "내재가치 대비 10% 이상 저평가, 매수 권장"
        elif price_diff_pct >= -10:
            valuation_status = "🟡 적정가치"
            recommendation = "Hold"
            comment = "내재가치 수준, 현재 가격 적정"
        elif price_diff_pct >= -20:
            valuation_status = "🟠 고평가"
            recommendation = "Weak Sell"
            comment = "내재가치 대비 10% 이상 고평가, 신중 투자"
        else:
            valuation_status = "🔴 상당한 고평가"
            recommendation = "Strong Sell"
            comment = "내재가치 대비 20% 이상 고평가, 매도 검토"
        
        return {
            "valuation_status": valuation_status,
            "recommendation": recommendation,
            "comment": comment,
            "price_difference": price_diff,
            "price_difference_pct": price_diff_pct,
            "margin_of_safety": max(0, price_diff_pct)
        }
    
    def _run(self, stock_symbol: str, discount_rate: float = 8.0) -> str:
        """도구 실행 메인 로직"""
        try:
            # 재무 데이터 가져오기
            financial_data = self._get_mock_financial_data(stock_symbol)
            
            # DCF 기업가치 계산
            dcf_analysis = self._calculate_dcf_value(financial_data, discount_rate)
            
            # 밸류에이션 분석
            valuation_analysis = self._analyze_valuation(
                financial_data["current_price"],
                dcf_analysis["value_per_share"]
            )
            
            # 민감도 분석 (할인율 ±1% 변동)
            sensitivity_analysis = []
            for rate_change in [-1, 0, 1]:
                test_rate = discount_rate + rate_change
                test_dcf = self._calculate_dcf_value(financial_data, test_rate)
                sensitivity_analysis.append({
                    "discount_rate": test_rate,
                    "value_per_share": round(test_dcf["value_per_share"], 0)
                })
            
            result = {
                "company": financial_data["company_name"],
                "symbol": stock_symbol,
                "current_price": financial_data["current_price"],
                "intrinsic_value": round(dcf_analysis["value_per_share"], 0),
                "valuation_analysis": valuation_analysis,
                "dcf_details": {
                    "enterprise_value": round(dcf_analysis["enterprise_value"], 0),
                    "equity_value": round(dcf_analysis["equity_value"], 0),
                    "total_pv_fcf": round(dcf_analysis["total_pv_fcf"], 0),
                    "pv_terminal_value": round(dcf_analysis["pv_terminal_value"], 0)
                },
                "sensitivity_analysis": sensitivity_analysis,
                "key_assumptions": {
                    "discount_rate": discount_rate,
                    "terminal_growth": financial_data["terminal_growth"],
                    "fcf_growth_1_3": financial_data["growth_rate_1_3"],
                    "fcf_growth_4_5": financial_data["growth_rate_4_5"]
                },
                "summary": f"{financial_data['company_name']}의 DCF 기반 내재가치는 {dcf_analysis['value_per_share']:,.0f}원이며, 현재가 대비 {valuation_analysis['price_difference_pct']:.1f}% {'저평가' if valuation_analysis['price_difference_pct'] > 0 else '고평가'}되었습니다."
            }
            
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return f"밸류에이션 분석 중 오류 발생: {str(e)}"
