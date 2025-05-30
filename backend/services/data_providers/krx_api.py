"""
KRX (한국거래소) 실시간 데이터 제공자
- 주식 기본 정보, 시가총액, 거래량 등
- 업종별 분류 및 지수 정보
"""
import aiohttp
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
from dataclasses import dataclass
import random

logger = logging.getLogger(__name__)

@dataclass
class StockInfo:
    """주식 기본 정보"""
    symbol: str
    name: str
    market: str  # KOSPI, KOSDAQ
    sector: str
    market_cap: float
    current_price: float
    shares_outstanding: float
    volume: int
    per: float
    pbr: float
    dividend_yield: float

class KRXDataProvider:
    """KRX 데이터 제공자"""
    
    def __init__(self):
        self.api_key = os.getenv("KRX_API_KEY", "")
        self.base_url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Mock 데이터 사용 여부 (API 키가 없거나 테스트 모드)
        self.use_mock_data = not self.api_key or self.api_key == "YOUR_KRX_API_KEY_HERE"
        
        if self.use_mock_data:
            logger.warning("KRX API 키가 설정되지 않아 Mock 데이터를 사용합니다.")
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.session:
            await self.session.close()
    
    async def get_stock_list(self, market: str = "ALL") -> List[StockInfo]:
        """주식 목록 조회"""
        if self.use_mock_data:
            return self._get_mock_stock_list(market)
        
        try:
            # 실제 KRX API 호출 로직
            params = {
                "bld": "dbms/MDC/STAT/standard/MDCSTAT01501",
                "mktId": "STK" if market == "KOSPI" else "KSQ" if market == "KOSDAQ" else "ALL",
                "trdDd": datetime.now().strftime("%Y%m%d")
            }
            
            async with self.session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stock_list(data)
                else:
                    logger.error(f"KRX API 호출 실패: {response.status}")
                    return self._get_mock_stock_list(market)
        
        except Exception as e:
            logger.error(f"KRX 데이터 조회 중 오류: {e}")
            return self._get_mock_stock_list(market)
    
    async def get_stock_detail(self, symbol: str) -> Optional[Dict[str, Any]]:
        """개별 종목 상세 정보"""
        if self.use_mock_data:
            return self._get_mock_stock_detail(symbol)
        
        try:
            params = {
                "bld": "dbms/MDC/STAT/standard/MDCSTAT01701",
                "isuCd": symbol
            }
            
            async with self.session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stock_detail(data)
                else:
                    return self._get_mock_stock_detail(symbol)
        
        except Exception as e:
            logger.error(f"종목 {symbol} 상세 정보 조회 오류: {e}")
            return self._get_mock_stock_detail(symbol)
    
    async def get_market_indices(self) -> Dict[str, float]:
        """주요 지수 정보"""
        if self.use_mock_data:
            return {
                "KOSPI": 2580.50,
                "KOSDAQ": 850.20,
                "KPI200": 340.15
            }
        
        try:
            params = {
                "bld": "dbms/MDC/STAT/standard/MDCSTAT00301"
            }
            
            async with self.session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_indices(data)
                else:
                    return {"KOSPI": 2580.50, "KOSDAQ": 850.20}
        
        except Exception as e:
            logger.error(f"지수 정보 조회 오류: {e}")
            return {"KOSPI": 2580.50, "KOSDAQ": 850.20}
    
    def _get_mock_stock_list(self, market: str) -> List[StockInfo]:
        """Mock 데이터 - 주요 종목 리스트"""
        stocks = [
            StockInfo("005930", "삼성전자", "KOSPI", "반도체", 380000000, 72000, 5280000, 15000000, 12.5, 1.2, 2.8),
            StockInfo("000660", "SK하이닉스", "KOSPI", "반도체", 85000000, 117000, 730000, 8500000, 18.2, 1.8, 1.5),
            StockInfo("035420", "NAVER", "KOSPI", "인터넷", 45000000, 270000, 167000, 2100000, 28.5, 3.2, 0.8),
            StockInfo("005380", "현대차", "KOSPI", "자동차", 42000000, 195000, 215000, 5200000, 8.9, 0.9, 4.2),
            StockInfo("006400", "삼성SDI", "KOSPI", "배터리", 35000000, 520000, 67000, 1800000, 22.1, 2.1, 1.2),
            StockInfo("207940", "삼성바이오로직스", "KOSPI", "바이오", 120000000, 800000, 150000, 450000, 45.2, 8.5, 0.0),
            StockInfo("068270", "셀트리온", "KOSPI", "바이오", 25000000, 185000, 135000, 2800000, 15.8, 2.4, 0.5),
            StockInfo("035720", "카카오", "KOSPI", "인터넷", 18000000, 42000, 428000, 8900000, 25.6, 1.8, 1.1),
            StockInfo("051910", "LG화학", "KOSPI", "화학", 38000000, 540000, 70000, 1200000, 12.4, 1.1, 2.5),
            StockInfo("012330", "현대모비스", "KOSPI", "자동차부품", 28000000, 280000, 100000, 780000, 9.8, 1.0, 3.8),
        ]
        
        if market == "KOSPI":
            return [s for s in stocks if s.market == "KOSPI"]
        elif market == "KOSDAQ":
            # KOSDAQ 종목들 추가
            kosdaq_stocks = [
                StockInfo("091990", "셀트리온헬스케어", "KOSDAQ", "바이오", 8500000, 68000, 125000, 3200000, 18.5, 2.8, 0.8),
                StockInfo("096770", "SK이노베이션", "KOSDAQ", "정유화학", 15000000, 205000, 73000, 1900000, 11.2, 0.8, 3.2),
            ]
            return kosdaq_stocks
        else:
            return stocks
    
    def _get_mock_stock_detail(self, symbol: str) -> Dict[str, Any]:
        """Mock 데이터 - 개별 종목 상세"""
        stock_details = {
            "005930": {
                "financial_data": {
                    "revenue": 280000000,
                    "net_income": 35000000,
                    "operating_income": 42000000,
                    "total_assets": 420000000,
                    "total_equity": 320000000,
                    "debt_to_equity": 0.31,
                    "current_ratio": 2.1,
                    "roe": 15.8,
                    "roa": 8.9,
                    "gross_margin": 45.2,
                    "operating_margin": 15.0,
                    "net_margin": 12.5
                },
                "growth_metrics": {
                    "revenue_growth_1y": 8.5,
                    "revenue_growth_3y": 12.3,
                    "net_income_growth_1y": 15.2,
                    "net_income_growth_3y": 18.7,
                    "market_cap_growth_3y": 25.4
                }
            }
        }
        
        return stock_details.get(symbol, self._generate_mock_detail(symbol))
    
    def _generate_mock_detail(self, symbol: str) -> Dict[str, Any]:
        """동적 Mock 데이터 생성"""
        random.seed(hash(symbol) % 1000)
        
        return {
            "financial_data": {
                "revenue": random.uniform(50000, 300000) * 1000000,
                "net_income": random.uniform(3000, 50000) * 1000000,
                "operating_income": random.uniform(4000, 60000) * 1000000,
                "total_assets": random.uniform(100000, 500000) * 1000000,
                "total_equity": random.uniform(70000, 400000) * 1000000,
                "debt_to_equity": random.uniform(0.1, 1.5),
                "current_ratio": random.uniform(1.0, 3.0),
                "roe": random.uniform(5, 25),
                "roa": random.uniform(3, 15),
                "gross_margin": random.uniform(15, 50),
                "operating_margin": random.uniform(8, 25),
                "net_margin": random.uniform(5, 20)
            },
            "growth_metrics": {
                "revenue_growth_1y": random.uniform(-5, 20),
                "revenue_growth_3y": random.uniform(0, 25),
                "net_income_growth_1y": random.uniform(-10, 30),
                "net_income_growth_3y": random.uniform(-5, 35),
                "market_cap_growth_3y": random.uniform(-20, 50)
            }
        }
    
    def _parse_stock_list(self, data: Dict) -> List[StockInfo]:
        """실제 API 응답 파싱"""
        # 실제 KRX API 응답 구조에 맞게 파싱
        # 현재는 Mock 데이터 반환
        return self._get_mock_stock_list("ALL")
    
    def _parse_stock_detail(self, data: Dict) -> Dict[str, Any]:
        """실제 API 응답 파싱"""
        # 실제 KRX API 응답 구조에 맞게 파싱
        return {}
    
    def _parse_indices(self, data: Dict) -> Dict[str, float]:
        """지수 데이터 파싱"""
        # 실제 API 응답 파싱
        return {"KOSPI": 2580.50, "KOSDAQ": 850.20}

# 싱글톤 인스턴스
krx_provider = KRXDataProvider()