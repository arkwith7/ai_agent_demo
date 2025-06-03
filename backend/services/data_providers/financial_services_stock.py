from typing import Dict, List, Optional, Any
import aiohttp
import asyncio
from core.config import settings
import logging
from datetime import datetime, timedelta
from .base_provider import BaseDataProvider
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import json
import pandas as pd

logger = logging.getLogger(__name__)

class FinancialServicesStockProvider(BaseDataProvider):
    def __init__(self):
        self.api_key = unquote(unquote(settings.FSS_API_KEY))  # 이중 디코딩
        self.base_url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, */*",
            "Connection": "keep-alive"
        }
        logger.info(f"FinancialServicesStockProvider 초기화: API 키 존재 여부 = {bool(self.api_key)}")

    async def _fetch_data_for_date(self, session: aiohttp.ClientSession, date_str: str, stock_code: str = "") -> List[Dict[str, Any]]:
        """특정 날짜의 데이터를 조회합니다."""
        params = {
            "serviceKey": self.api_key,
            "numOfRows": "1000",
            "pageNo": "1",
            "resultType": "json",
            "basDt": date_str
        }
        
        if stock_code:
            params["likeSrtnCd"] = stock_code
            params["mrktCls"] = "KOSPI"
        else:
            params["mrktCls"] = "KOSPI"
            params["likeSrtnCd"] = ""
        
        url = f"{self.base_url}/getStockPriceInfo"
        logger.info(f"날짜 {date_str} 데이터 조회 시도")
        
        try:
            async with session.get(url, params=params, headers=self.headers, ssl=False) as response:
                if response.status == 200:
                    data = await response.json()
                    if not isinstance(data, dict) or 'response' not in data:
                        logger.error("응답 구조 오류")
                        return []
                    
                    body = data['response'].get('body', {})
                    items_raw = body.get('items', {})
                    total_count = int(body.get('totalCount', 0))
                    
                    if total_count > 0:
                        logger.info(f"날짜 {date_str}에서 {total_count}건의 데이터 발견")
                        
                        actual_items = []
                        if isinstance(items_raw, dict):
                            if 'item' in items_raw:
                                item_data = items_raw['item']
                                actual_items = [item_data] if isinstance(item_data, dict) else item_data
                            elif any(key in items_raw for key in ['itmsNm', 'srtnCd', 'clpr']):
                                actual_items = [items_raw]
                        elif isinstance(items_raw, list):
                            actual_items = items_raw
                        
                        if actual_items:
                            # 데이터 검증 및 변환
                            valid_items = []
                            for item in actual_items:
                                try:
                                    if all(key in item for key in ['itmsNm', 'srtnCd', 'clpr']):
                                        # 숫자형 데이터 변환
                                        converted_item = {
                                            '종목코드': str(item['srtnCd']),
                                            '종목명': str(item['itmsNm']),
                                            '시장구분': str(item.get('mrktCtg', 'KOSPI')),
                                            '현재가': float(item['clpr']),
                                            '등락률': float(item.get('fltRt', 0)),
                                            '거래량': float(item.get('trqu', 0)),
                                            '시가총액': float(item.get('mrktTotAmt', 0))
                                        }
                                        valid_items.append(converted_item)
                                except (ValueError, TypeError) as e:
                                    logger.error(f"데이터 변환 오류: {str(e)}")
                                    continue
                            
                            if valid_items:
                                # 중복 제거
                                unique_items = {}
                                for item in valid_items:
                                    code = item['종목코드']
                                    if code not in unique_items:
                                        unique_items[code] = item
                                
                                result = list(unique_items.values())
                                logger.info(f"유효한 데이터 {len(result)}건 추출 완료")
                                return result
                    
                    logger.warning(f"날짜 {date_str}에서 유효한 데이터를 찾을 수 없음")
                    return []
                    
        except Exception as e:
            logger.error(f"데이터 조회 중 오류 발생: {str(e)}")
            return []

    async def get_market_data(self, stock_code: str = "") -> pd.DataFrame:
        """주식 시장 데이터를 수집합니다."""
        try:
            logger.info("=== 시장 데이터 수집 시작 ===")
            logger.info(f"요청된 종목코드: {stock_code}")
            
            if not self.api_key:
                logger.error("API 키가 설정되지 않았습니다.")
                return pd.DataFrame()
            
            async with aiohttp.ClientSession() as session:
                # 오늘부터 최대 10일 전까지 순차적으로 조회
                today = datetime.now()
                for days_ago in range(10):  # 최대 10일 전까지 조회
                    target_date = today - timedelta(days=days_ago)
                    date_str = target_date.strftime("%Y%m%d")
                    
                    data = await self._fetch_data_for_date(session, date_str, stock_code)
                    if data:
                        logger.info(f"데이터 발견: {date_str}")
                        return pd.DataFrame(data)
                    
                    # API 호출 간 딜레이
                    await asyncio.sleep(0.3)  # 0.3초로 증가
                
                logger.warning("10일 이내의 데이터를 찾을 수 없음")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"시장 데이터 수집 중 오류 발생: {str(e)}")
            logger.exception("상세 에러 정보:")
            return pd.DataFrame()

    async def get_stock_price(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """특정 종목의 시세 정보를 조회합니다."""
        try:
            logger.info(f"=== 종목 시세 조회 시작: {stock_code} ===")
            
            async with aiohttp.ClientSession() as session:
                params = {
                    "serviceKey": self.api_key,
                    "numOfRows": "1",
                    "pageNo": "1",
                    "resultType": "json",
                    "likeSrtnCd": stock_code
                }
                
                url = f"{self.base_url}/getStockPriceInfo"
                logger.info(f"API 호출 URL: {url}")
                logger.info(f"API 파라미터: {params}")
                
                async with session.get(url, params=params, headers=self.headers, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        if not isinstance(data, dict) or 'response' not in data:
                            logger.error("응답 구조 오류")
                            return None
                        
                        body = data['response'].get('body', {})
                        items = body.get('items', {})
                        
                        if isinstance(items, dict) and 'item' in items:
                            item = items['item']
                            if isinstance(item, list):
                                item = item[0]
                            
                            return {
                                "종목코드": str(item.get('srtnCd', '')),
                                "종목명": str(item.get('itmsNm', '')),
                                "현재가": float(item.get('clpr', 0)),
                                "등락률": float(item.get('fltRt', 0)),
                                "거래량": float(item.get('trqu', 0)),
                                "시가총액": float(item.get('mrktTotAmt', 0))
                            }
                    else:
                        error_text = await response.text()
                        logger.error(f"API 호출 실패: {response.status}")
                        logger.error(f"에러 응답: {error_text}")
                        return None
                        
        except Exception as e:
            logger.error(f"종목 시세 조회 중 오류 발생: {str(e)}")
            logger.exception("상세 에러 정보:")
            return None

    async def get_company_info(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """특정 기업의 정보를 가져옵니다."""
        try:
            logger.info(f"=== 기업 정보 조회 시작: {stock_code} ===")
            
            url = f"{self.base_url}/getStockCompanyInfo"
            params = {
                "serviceKey": self.api_key,
                "resultType": "json",
                "likeSrtnCd": stock_code
            }
            
            logger.info(f"API 호출 URL: {url}")
            logger.info(f"API 파라미터: {params}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=self.headers, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        if not isinstance(data, dict) or 'response' not in data:
                            logger.error("응답 구조 오류")
                            return None
                        
                        body = data['response'].get('body', {})
                        items = body.get('items', {})
                        
                        if isinstance(items, dict) and 'item' in items:
                            item = items['item']
                            if isinstance(item, list):
                                item = item[0]
                            
                            return {
                                "회사명": str(item.get('corpName', '')),
                                "업종": str(item.get('sector', '')),
                                "주요제품": str(item.get('product', '')),
                                "상장일": str(item.get('listingDate', '')),
                                "결산월": str(item.get('settlementMonth', ''))
                            }
                    else:
                        error_text = await response.text()
                        logger.error(f"API 호출 실패: {response.status}")
                        logger.error(f"에러 응답: {error_text}")
                        return None
                        
        except Exception as e:
            logger.error(f"기업 정보 조회 중 오류 발생: {str(e)}")
            logger.exception("상세 에러 정보:")
            return None

# 싱글톤 인스턴스 생성
fss_provider = FinancialServicesStockProvider() 