from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseDataProvider(ABC):
    """데이터 프로바이더의 기본 클래스"""
    
    @abstractmethod
    async def get_market_data(self) -> List[Dict[str, Any]]:
        """시장 데이터를 가져옵니다."""
        pass
    
    @abstractmethod
    async def get_stock_price(self, stock_code: str) -> Dict[str, Any]:
        """특정 종목의 시세 정보를 가져옵니다."""
        pass
    
    @abstractmethod
    async def get_company_info(self, stock_code: str) -> Optional[Dict]:
        """기업 정보를 가져옵니다."""
        pass 