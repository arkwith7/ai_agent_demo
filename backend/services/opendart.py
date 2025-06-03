import aiohttp
from typing import Dict, Any, List
from datetime import datetime
from core.config import settings

class OpenDartService:
    def __init__(self):
        self.api_key = settings.OPENDART_API_KEY
        self.base_url = "https://opendart.fss.or.kr/api"
        self.use_mock_data = not self.api_key

    async def get_company_financials(self, stock_code: str) -> Dict[str, Any]:
        """
        기업의 재무제표 데이터를 조회합니다.
        """
        if self.use_mock_data:
            return self._get_mock_financial_data(stock_code)

        try:
            async with aiohttp.ClientSession() as session:
                # 1. 기업 기본 정보 조회
                company_info = await self._get_company_info(session, stock_code)
                
                # 2. 재무제표 데이터 조회
                financial_data = await self._get_financial_statements(session, company_info['corp_code'])
                
                # 3. 배당 정보 조회
                dividend_data = await self._get_dividend_info(session, company_info['corp_code'])
                
                return {
                    "company_info": company_info,
                    "financial_data": financial_data,
                    "dividend_data": dividend_data
                }
        except Exception as e:
            raise Exception(f"OpenDART API 호출 중 오류 발생: {str(e)}")

    async def _get_company_info(self, session: aiohttp.ClientSession, stock_code: str) -> Dict[str, Any]:
        """기업 기본 정보 조회"""
        url = f"{self.base_url}/company.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": stock_code
        }
        
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"기업 정보 조회 실패: {response.status}")
            data = await response.json()
            return data.get("corp_info", {})

    async def _get_financial_statements(self, session: aiohttp.ClientSession, corp_code: str) -> Dict[str, Any]:
        """재무제표 데이터 조회"""
        current_year = datetime.now().year
        financial_data = {}
        
        # 최근 3년간의 재무제표 데이터 조회
        for year in range(current_year - 2, current_year + 1):
            for quarter in range(1, 5):
                url = f"{self.base_url}/fnlttSinglAcnt.json"
                params = {
                    "crtfc_key": self.api_key,
                    "corp_code": corp_code,
                    "bsns_year": str(year),
                    "reprt_code": f"1{quarter:03d}"  # 11011: 1분기, 11012: 반기, 11013: 3분기, 11014: 사업보고서
                }
                
                try:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get("status") == "000":
                                financial_data[f"{year}_Q{quarter}"] = data.get("list", [])
                except Exception as e:
                    print(f"{year}년 {quarter}분기 재무제표 조회 실패: {str(e)}")
                    continue
        
        return financial_data

    async def _get_dividend_info(self, session: aiohttp.ClientSession, corp_code: str) -> Dict[str, Any]:
        """배당 정보 조회"""
        url = f"{self.base_url}/alotMatter.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code
        }
        
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"배당 정보 조회 실패: {response.status}")
            data = await response.json()
            return data.get("list", [])

    def _get_mock_financial_data(self, stock_code: str) -> Dict[str, Any]:
        """Mock 재무 데이터 반환"""
        current_year = datetime.now().year
        mock_financial_data = {}
        
        # 최근 3년간의 Mock 재무제표 데이터 생성
        for year in range(current_year - 2, current_year + 1):
            for quarter in range(1, 5):
                mock_financial_data[f"{year}_Q{quarter}"] = [
                    {
                        "rcept_no": f"{year}0000000",
                        "reprt_code": f"1{quarter:03d}",
                        "bsns_year": str(year),
                        "corp_code": stock_code,
                        "sj_div": "BS",
                        "sj_nm": "재무상태표",
                        "account_id": "ifrs-full_Equity",
                        "account_nm": "자본",
                        "account_detail": "-",
                        "thstrm_nm": "제 1 기",
                        "thstrm_amount": str(100000000000 + (year - current_year + 2) * 10000000000),
                        "frmtrm_nm": "제 2 기",
                        "frmtrm_amount": str(90000000000 + (year - current_year + 2) * 10000000000)
                    }
                ]
        
        return {
            "company_info": {
                "corp_code": stock_code,
                "corp_name": "테스트 기업",
                "stock_code": stock_code,
                "corp_cls": "Y",
                "jurir_no": "1234567890123",
                "bizr_no": "1234567890",
                "adres": "서울특별시 강남구",
                "hm_url": "http://www.test.com",
                "ir_url": "http://www.test.com/ir",
                "phn_no": "02-1234-5678",
                "fax_no": "02-1234-5679",
                "induty_code": "C26",
                "est_dt": "19800101",
                "acc_mt": "12"
            },
            "financial_data": mock_financial_data,
            "dividend_data": [
                {
                    "rcept_no": f"{current_year}0000000",
                    "corp_cls": "Y",
                    "corp_code": stock_code,
                    "corp_name": "테스트 기업",
                    "se": "주주총회",
                    "stock_knd": "보통주",
                    "thdt": f"{current_year}1231",
                    "stk_parprc": "5000",
                    "stk_qty": "1000000",
                    "stk_dvdd_rt": "3.0",
                    "stk_dvdd_pric": "150",
                    "pay_dt": f"{current_year}0401"
                }
            ]
        } 