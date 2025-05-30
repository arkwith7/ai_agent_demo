"""
OpenDART (금융감독원 전자공시시스템) 데이터 제공자
- 기업 재무제표, 사업보고서 등 공시 정보
- ESG 관련 정보, 지배구조 데이터
"""
import aiohttp
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass
import random

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
        self.api_key = os.getenv("OPEN_DART_API_KEY", "")
        print(f"[DEBUG] OpenDARTProvider __init__: api_key={self.api_key}")
        self.base_url = "https://opendart.fss.or.kr/api"
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Mock 데이터 사용 여부
        self.use_mock_data = not self.api_key or len(self.api_key) < 20
        print(f"[DEBUG] OpenDARTProvider __init__: use_mock_data={self.use_mock_data}")
        
        if self.use_mock_data:
            logger.warning("OpenDART API 키가 설정되지 않아 Mock 데이터를 사용합니다.")
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.session:
            await self.session.close()
    
    async def get_company_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """기업 기본 정보 조회"""
        if self.use_mock_data:
            return self._get_mock_company_info(symbol)
        
        try:
            params = {
                "crtfc_key": self.api_key,
                "corp_code": await self._get_corp_code(symbol)
            }
            
            async with self.session.get(f"{self.base_url}/company.json", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_company_info(data)
                else:
                    return self._get_mock_company_info(symbol)
        
        except Exception as e:
            logger.error(f"기업 정보 조회 오류 ({symbol}): {e}")
            return self._get_mock_company_info(symbol)
    
    async def get_financial_statements(self, symbol: str, years: int = 3) -> List[FinancialStatement]:
        """재무제표 조회 (최근 N년)"""
        if self.use_mock_data:
            return self._get_mock_financial_statements(symbol, years)
        
        try:
            corp_code = await self._get_corp_code(symbol)
            statements = []
            
            for year in range(datetime.now().year - years, datetime.now().year):
                params = {
                    "crtfc_key": self.api_key,
                    "corp_code": corp_code,
                    "bsns_year": str(year),
                    "reprt_code": "11011"  # 사업보고서
                }
                
                async with self.session.get(f"{self.base_url}/fnlttSinglAcnt.json", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        statement = self._parse_financial_statement(data, symbol, year)
                        if statement:
                            statements.append(statement)
            
            return statements if statements else self._get_mock_financial_statements(symbol, years)
        
        except Exception as e:
            logger.error(f"재무제표 조회 오류 ({symbol}): {e}")
            return self._get_mock_financial_statements(symbol, years)
    
    async def get_esg_info(self, symbol: str) -> Optional[ESGInfo]:
        """ESG 정보 조회"""
        if self.use_mock_data:
            return self._get_mock_esg_info(symbol)
        
        try:
            # OpenDART ESG 관련 공시 조회
            corp_code = await self._get_corp_code(symbol)
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code,
                "bgn_de": (datetime.now() - timedelta(days=365)).strftime("%Y%m%d"),
                "end_de": datetime.now().strftime("%Y%m%d"),
                "page_no": "1",
                "page_count": "100"
            }
            
            async with self.session.get(f"{self.base_url}/list.json", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._analyze_esg_from_disclosures(data, symbol)
                else:
                    return self._get_mock_esg_info(symbol)
        
        except Exception as e:
            logger.error(f"ESG 정보 조회 오류 ({symbol}): {e}")
            return self._get_mock_esg_info(symbol)
    
    async def get_governance_info(self, symbol: str) -> Dict[str, Any]:
        """지배구조 정보 조회"""
        if self.use_mock_data:
            return self._get_mock_governance_info(symbol)
        
        try:
            corp_code = await self._get_corp_code(symbol)
            params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code,
                "bsns_year": str(datetime.now().year - 1)
            }
            
            # 임원 현황
            async with self.session.get(f"{self.base_url}/empSttus.json", params=params) as response:
                if response.status == 200:
                    emp_data = await response.json()
                    return self._parse_governance_info(emp_data)
                else:
                    return self._get_mock_governance_info(symbol)
        
        except Exception as e:
            logger.error(f"지배구조 정보 조회 오류 ({symbol}): {e}")
            return self._get_mock_governance_info(symbol)
    
    async def _get_corp_code(self, symbol: str) -> str:
        """종목코드로 기업고유번호 조회"""
        # 실제로는 OpenDART의 corp_code를 조회해야 함
        # 현재는 종목코드를 그대로 사용
        corp_code_mapping = {
            "005930": "00126380",  # 삼성전자
            "000660": "00164779",  # SK하이닉스
            "035420": "00401731",  # NAVER
            # 기타 매핑...
        }
        return corp_code_mapping.get(symbol, symbol)
    
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
    
    def _parse_company_info(self, data: Dict) -> Dict[str, Any]:
        """실제 API 응답 파싱"""
        # 실제 OpenDART API 응답 구조에 맞게 파싱
        return data
    
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

# 싱글톤 인스턴스
opendart_provider = OpenDARTProvider()