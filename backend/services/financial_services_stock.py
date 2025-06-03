import aiohttp
from typing import Dict, Any, List
from datetime import datetime, timedelta
from core.config import settings

class FinancialServicesStockService:
    def __init__(self):
        self.base_url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService"
        self.api_key = settings.STOCK_API_KEY
        self.use_mock_data = not self.api_key

    async def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        주식 기본 정보를 조회합니다.
        """
        if self.use_mock_data:
            return self._get_mock_stock_data(stock_code)

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/getStockPriceInfo"
                params = {
                    "serviceKey": self.api_key,
                    "resultType": "json",
                    "itmsNm": stock_code,
                    "mrktCls": "KOSPI"
                }
                
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        raise Exception(f"주식 정보 조회 실패: {response.status}")
                    data = await response.json()
                    
                    # 응답 데이터 구조 확인 및 변환
                    if "response" in data and "body" in data["response"]:
                        items = data["response"]["body"]["items"]
                        if isinstance(items, dict) and "item" in items:
                            return items["item"]
                    return data
        except Exception as e:
            raise Exception(f"금융위원회 API 호출 중 오류 발생: {str(e)}")

    async def get_market_data(self, stock_code: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        주식 시장 데이터를 조회합니다.
        """
        if self.use_mock_data:
            return self._get_mock_market_data(stock_code, days)

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/getStockPriceInfo"
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                
                params = {
                    "serviceKey": self.api_key,
                    "resultType": "json",
                    "itmsNm": stock_code,
                    "mrktCls": "KOSPI",
                    "beginBasDt": start_date.strftime("%Y%m%d"),
                    "endBasDt": end_date.strftime("%Y%m%d")
                }
                
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        raise Exception(f"시장 데이터 조회 실패: {response.status}")
                    data = await response.json()
                    
                    # 응답 데이터 구조 확인 및 변환
                    if "response" in data and "body" in data["response"]:
                        items = data["response"]["body"]["items"]
                        if isinstance(items, dict) and "item" in items:
                            return items["item"] if isinstance(items["item"], list) else [items["item"]]
                    return data
        except Exception as e:
            raise Exception(f"금융위원회 API 호출 중 오류 발생: {str(e)}")

    def _get_mock_stock_data(self, stock_code: str) -> Dict[str, Any]:
        """Mock 주식 데이터 반환"""
        return {
            "basDt": "20240315",
            "srtnCd": stock_code,
            "isinCd": "KR7000000000",
            "itmsNm": "테스트 기업",
            "mrktCtg": "KOSPI",
            "clpr": "50000",
            "vs": "1000",
            "fltRt": "2.04",
            "mkp": "49000",
            "hipr": "51000",
            "lopr": "48000",
            "trqu": "1000000",
            "trPrc": "50000000000",
            "lstgStCnt": "10000000",
            "mrktTotAmt": "500000000000"
        }

    def _get_mock_market_data(self, stock_code: str, days: int) -> List[Dict[str, Any]]:
        """Mock 시장 데이터 반환"""
        return [
            {
                "basDt": (datetime.now() - timedelta(days=i)).strftime("%Y%m%d"),
                "srtnCd": stock_code,
                "isinCd": "KR7000000000",
                "itmsNm": "테스트 기업",
                "mrktCtg": "KOSPI",
                "clpr": str(50000 + i * 100),
                "vs": str(1000 + i * 10),
                "fltRt": str(2.04 + i * 0.1),
                "mkp": str(49000 + i * 100),
                "hipr": str(51000 + i * 100),
                "lopr": str(48000 + i * 100),
                "trqu": str(1000000 + i * 10000),
                "trPrc": str(50000000000 + i * 1000000000),
                "lstgStCnt": "10000000",
                "mrktTotAmt": str(500000000000 + i * 10000000000)
            }
            for i in range(days)
        ] 