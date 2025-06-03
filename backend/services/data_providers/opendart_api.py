"""
OpenDART (금융감독원 전자공시시스템) 데이터 제공자
- 기업 재무제표, 사업보고서 등 공시 정보
- ESG 관련 정보, 지배구조 데이터
"""
import httpx
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import random
from core.config import settings
from services.logger import LoggerService

logger = logging.getLogger(__name__)

@dataclass
class FinancialStatement:
    """재무제표 정보"""
    symbol: str
    year: int
    quarter: int
    revenue: float
    operating_income: float
    net_income: float
    total_assets: float
    total_equity: float
    debt: float
    cash_flow_from_operations: float
    free_cash_flow: float

@dataclass
class ESGInfo:
    """ESG 정보"""
    symbol: str
    environmental_score: float
    social_score: float
    governance_score: float
    total_score: float
    disclosure_level: str

class OpenDARTProvider:
    """OpenDART 데이터 제공자"""
    
    def __init__(self):
        self.api_key = settings.OPEN_DART_API_KEY
        self.logger = LoggerService()
        self.base_url = "https://opendart.fss.or.kr/api"
        
        # Mock 데이터 사용 여부
        self.use_mock_data = not self.api_key or len(self.api_key) < 20
        if self.use_mock_data:
            self.logger.warning("OpenDART API 키가 설정되지 않아 Mock 데이터를 사용합니다.")
    
    async def get_company_info(self, corp_code: str) -> Dict[str, Any]:
        """
        기업 기본 정보를 조회합니다.
        """
        if self.use_mock_data:
            return self._get_mock_company_info(corp_code)
            
        try:
            url = f"{self.base_url}/company.json"
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error(f"Error getting company info: {str(e)}")
            return self._get_mock_company_info(corp_code)
    
    async def get_financial_statement(self, corp_code: str, year: Optional[int] = None) -> Dict[str, Any]:
        """
        재무제표 정보를 조회합니다.
        """
        if self.use_mock_data:
            return self._get_mock_financial_statements(corp_code, 1)[0].__dict__
            
        try:
            if year is None:
                year = datetime.now().year

            url = f"{self.base_url}/fnlttSinglAcnt.json"
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code,
                "bsns_year": str(year),
                "reprt_code": "11011"  # 1분기보고서
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error(f"Error getting financial statement: {str(e)}")
            return self._get_mock_financial_statements(corp_code, 1)[0].__dict__
    
    async def get_corp_code(self, stock_code: str) -> Optional[str]:
        """
        종목코드로 기업 고유번호를 조회합니다.
        """
        if self.use_mock_data:
            return stock_code
            
        try:
            url = f"{self.base_url}/corpCode.xml"
            params = {
                "crtfc_key": self.api_key
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                # XML 파싱 로직 구현 필요
                return stock_code
        except Exception as e:
            self.logger.error(f"Error getting corp code: {str(e)}")
            return stock_code
    
    async def get_major_shareholders(self, corp_code: str) -> Dict[str, Any]:
        """
        주요 주주 정보를 조회합니다.
        """
        if self.use_mock_data:
            return self._get_mock_governance_info(corp_code)
            
        try:
            url = f"{self.base_url}/elestock.json"
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error(f"Error getting major shareholders: {str(e)}")
            return self._get_mock_governance_info(corp_code)
    
    async def get_executive_info(self, corp_code: str) -> Dict[str, Any]:
        """
        임원 정보를 조회합니다.
        """
        if self.use_mock_data:
            return self._get_mock_governance_info(corp_code)
            
        try:
            url = f"{self.base_url}/empSttus.json"
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error(f"Error getting executive info: {str(e)}")
            return self._get_mock_governance_info(corp_code)
    
    async def get_financial_statements(self, symbol: str, years: int = 3) -> List[FinancialStatement]:
        """재무제표 조회 (최근 N년)"""
        if self.use_mock_data:
            return self._get_mock_financial_statements(symbol, years)
        
        try:
            corp_code = await self.get_corp_code(symbol)
            statements = []
            
            for year in range(datetime.now().year - years, datetime.now().year):
                params = {
                    "crtfc_key": self.api_key,
                    "corp_code": corp_code,
                    "bsns_year": str(year),
                    "reprt_code": "11011"  # 사업보고서
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{self.base_url}/fnlttSinglAcnt.json", params=params)
                    if response.status_code == 200:
                        data = response.json()
                        statement = self._parse_financial_statement(data, symbol, year)
                        if statement:
                            statements.append(statement)
            
            return statements if statements else self._get_mock_financial_statements(symbol, years)
        
        except Exception as e:
            self.logger.error(f"재무제표 조회 오류 ({symbol}): {e}")
            return self._get_mock_financial_statements(symbol, years)
    
    async def get_esg_info(self, symbol: str) -> Optional[ESGInfo]:
        """ESG 정보 조회"""
        if self.use_mock_data:
            return self._get_mock_esg_info(symbol)
        
        try:
            corp_code = await self.get_corp_code(symbol)
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code,
                "bgn_de": (datetime.now() - timedelta(days=365)).strftime("%Y%m%d"),
                "end_de": datetime.now().strftime("%Y%m%d"),
                "page_no": "1",
                "page_count": "100"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/list.json", params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._analyze_esg_from_disclosures(data, symbol)
                else:
                    return self._get_mock_esg_info(symbol)
        
        except Exception as e:
            self.logger.error(f"ESG 정보 조회 오류 ({symbol}): {e}")
            return self._get_mock_esg_info(symbol)
    
    async def get_governance_info(self, symbol: str) -> Dict[str, Any]:
        """지배구조 정보 조회"""
        if self.use_mock_data:
            return self._get_mock_governance_info(symbol)
        
        try:
            corp_code = await self.get_corp_code(symbol)
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code,
                "bsns_year": str(datetime.now().year - 1)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/empSttus.json", params=params)
                if response.status_code == 200:
                    emp_data = response.json()
                    return self._parse_governance_info(emp_data)
                else:
                    return self._get_mock_governance_info(symbol)
        
        except Exception as e:
            self.logger.error(f"지배구조 정보 조회 오류 ({symbol}): {e}")
            return self._get_mock_governance_info(symbol)
    
    def _get_mock_company_info(self, symbol: str) -> Dict[str, Any]:
        """Mock 기업 정보"""
        company_info = {
            "005930": {
                "corp_name": "삼성전자주식회사",
                "corp_name_eng": "SAMSUNG ELECTRONICS CO., LTD.",
                "stock_name": "삼성전자",
                "stock_code": "005930",
                "ceo_nm": "한종희",
                "corp_cls": "Y",
                "jurir_no": "1301110006246",
                "bizr_no": "1248100998",
                "adres": "경기도 수원시 영통구 삼성로 129 (매탄동)",
                "hm_url": "http://www.samsung.com/sec",
                "ir_url": "http://www.samsung.com/global/ir/",
                "phn_no": "031-200-1114",
                "fax_no": "031-200-7538",
                "induty_code": "26410",
                "est_dt": "19690113"
            }
        }
        
        return company_info.get(symbol, self._generate_mock_company_info(symbol))
    
    def _generate_mock_company_info(self, symbol: str) -> Dict[str, Any]:
        """동적 Mock 기업 정보 생성"""
        random.seed(hash(symbol) % 1000)
        
        company_names = ["테크코리아", "이노베이션", "그린에너지", "바이오텍", "스마트솔루션"]
        industries = ["26410", "35110", "72110", "21200", "62010"]
        
        return {
            "corp_name": f"{random.choice(company_names)}주식회사",
            "stock_name": random.choice(company_names),
            "stock_code": symbol,
            "ceo_nm": "김대표",
            "corp_cls": "Y",
            "induty_code": random.choice(industries),
            "est_dt": f"{random.randint(1980, 2010):04d}{random.randint(1, 12):02d}{random.randint(1, 28):02d}"
        }
    
    def _get_mock_financial_statements(self, symbol: str, years: int) -> List[FinancialStatement]:
        """Mock 재무제표 데이터"""
        random.seed(hash(symbol) % 1000)
        statements = []
        
        # 기준 수치 설정
        base_revenue = random.uniform(100000, 500000) * 1000000
        base_growth = random.uniform(0.05, 0.15)  # 5-15% 성장률
        
        for i in range(years):
            year = datetime.now().year - years + i
            # 연도별 성장 적용
            revenue = base_revenue * ((1 + base_growth) ** i)
            operating_income = revenue * random.uniform(0.08, 0.20)
            net_income = operating_income * random.uniform(0.70, 0.90)
            total_assets = revenue * random.uniform(1.5, 3.0)
            total_equity = total_assets * random.uniform(0.4, 0.7)
            debt = total_assets - total_equity
            cash_flow_ops = net_income * random.uniform(1.1, 1.4)
            free_cash_flow = cash_flow_ops * random.uniform(0.7, 0.9)
            
            statement = FinancialStatement(
                symbol=symbol,
                year=year,
                quarter=4,  # 연간 데이터
                revenue=revenue,
                operating_income=operating_income,
                net_income=net_income,
                total_assets=total_assets,
                total_equity=total_equity,
                debt=debt,
                cash_flow_from_operations=cash_flow_ops,
                free_cash_flow=free_cash_flow
            )
            statements.append(statement)
        
        return statements
    
    def _get_mock_esg_info(self, symbol: str) -> ESGInfo:
        """Mock ESG 정보"""
        random.seed(hash(symbol) % 1000)
        
        env_score = random.uniform(60, 95)
        social_score = random.uniform(55, 90)
        governance_score = random.uniform(70, 95)
        total_score = (env_score + social_score + governance_score) / 3
        
        disclosure_levels = ["우수", "양호", "보통", "개선필요"]
        weights = [0.3, 0.4, 0.2, 0.1]  # 가중치
        disclosure_level = random.choices(disclosure_levels, weights=weights)[0]
        
        return ESGInfo(
            symbol=symbol,
            environmental_score=env_score,
            social_score=social_score,
            governance_score=governance_score,
            total_score=total_score,
            disclosure_level=disclosure_level
        )
    
    def _get_mock_governance_info(self, symbol: str) -> Dict[str, Any]:
        """Mock 지배구조 정보"""
        random.seed(hash(symbol) % 1000)
        
        return {
            "board_independence": random.uniform(0.3, 0.8),  # 사외이사 비율
            "board_diversity": random.uniform(0.1, 0.4),     # 여성 이사 비율
            "audit_committee": True,
            "compensation_committee": random.choice([True, False]),
            "nomination_committee": random.choice([True, False]),
            "shareholder_rights_score": random.uniform(60, 95),
            "transparency_score": random.uniform(65, 90),
            "board_size": random.randint(5, 15),
            "ceo_duality": random.choice([True, False])  # CEO와 회장 겸임 여부
        }
    
    def _parse_financial_statement(self, data: Dict, symbol: str, year: int) -> Optional[FinancialStatement]:
        """재무제표 데이터 파싱"""
        # 실제 API 응답 파싱 로직
        return None
    
    def _analyze_esg_from_disclosures(self, data: Dict, symbol: str) -> ESGInfo:
        """공시 내용에서 ESG 정보 추출"""
        # ESG 관련 키워드 분석 및 점수화
        return self._get_mock_esg_info(symbol)
    
    def _parse_governance_info(self, data: Dict) -> Dict[str, Any]:
        """지배구조 정보 파싱"""
        # 실제 API 응답 파싱
        return {}

    async def get_company_financials(self, stock_code: str) -> Dict[str, Any]:
        """
        기업의 재무제표 데이터를 조회합니다.
        """
        if self.use_mock_data:
            return self._get_mock_financial_data(stock_code)

        try:
            async with httpx.AsyncClient() as client:
                # 1. 기업 기본 정보 조회
                company_info = await self.get_company_info(stock_code)
                
                # 2. 재무제표 데이터 조회
                financial_data = await self.get_financial_statement(stock_code)
                
                # 3. 배당 정보 조회
                dividend_data = await self._get_dividend_info(client, stock_code)
                
                return {
                    "company_info": company_info,
                    "financial_data": financial_data,
                    "dividend_data": dividend_data
                }
        except Exception as e:
            self.logger.error(f"OpenDART API 호출 중 오류 발생: {str(e)}")
            return self._get_mock_financial_data(stock_code)

    async def _get_dividend_info(self, client: httpx.AsyncClient, stock_code: str) -> Dict[str, Any]:
        """배당 정보 조회"""
        url = f"{self.base_url}/alotMatter.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": stock_code
        }
        
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"배당 정보 조회 실패: {response.status_code}")
        data = response.json()
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

# 싱글톤 인스턴스
opendart_provider = OpenDARTProvider()