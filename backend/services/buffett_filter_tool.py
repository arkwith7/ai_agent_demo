# 워런 버핏 투자 기준 필터 도구 (Buffett Filter Tool)
# 이 코드는 AI Agent의 투자 종목 필터링 핵심 로직을 담당합니다.
# 위치: /backend/app/services/buffett_filter_tool.py

from typing import List, Dict, Any

class BuffettFilter:
    """
    워런 버핏의 6단계 투자 기준에 따라 종목을 필터링하는 클래스
    """
    def __init__(self, stock_data: List[Dict[str, Any]]):
        self.stock_data = stock_data

    def filter_by_market_cap(self) -> List[Dict[str, Any]]:
        # 1. 시가총액 상위 30% 필터
        sorted_data = sorted(self.stock_data, key=lambda x: x['market_cap'], reverse=True)
        top_30pct = int(len(sorted_data) * 0.3)
        return sorted_data[:top_30pct]

    def filter_by_roe(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # 2. 최근 3년 ROE >= 15%
        return [s for s in data if min(s['roe_3y']) >= 15]

    def filter_by_profitability(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # 3. 업종 평균 이상 순이익률 & FCF 상위 30%
        avg_profit = sum(s['net_profit_margin'] for s in data) / len(data)
        profit_filtered = [s for s in data if s['net_profit_margin'] >= avg_profit]
        sorted_fcf = sorted(profit_filtered, key=lambda x: x['fcf_per_share'], reverse=True)
        top_30pct = int(len(sorted_fcf) * 0.3)
        return sorted_fcf[:top_30pct]

    def filter_by_growth(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # 4. 시총 증가율 > 자본 증가율
        return [s for s in data if s['market_cap_growth_3y'] > s['equity_growth_3y']]

    def filter_by_fcf_projection(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # 5. 5년 예상 FCF 합 > 현재 시가총액
        return [s for s in data if s['fcf_projection_5y_sum'] > s['market_cap']]

    def filter(self) -> List[Dict[str, Any]]:
        data = self.filter_by_market_cap()
        data = self.filter_by_roe(data)
        data = self.filter_by_profitability(data)
        data = self.filter_by_growth(data)
        data = self.filter_by_fcf_projection(data)
        return data

# 실제 서비스에서는 외부 데이터 연동, 예외처리, 로깅, 유닛테스트 등 추가 필요
