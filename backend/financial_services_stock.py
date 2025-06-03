import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import logging

# 환경변수 로드
load_dotenv()

class FinancialServicesStock:
    def __init__(self):
        self.api_key = os.getenv('FSS_API_KEY')
        if not self.api_key:
            raise ValueError("FSS_API_KEY environment variable is not set")
        
        self.base_url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService"
        self.logger = logging.getLogger(__name__)

    def get_stock_data(self, start_date=None, end_date=None):
        """
        주식 시세 데이터를 가져옵니다.
        
        Args:
            start_date (str): 시작일 (YYYYMMDD)
            end_date (str): 종료일 (YYYYMMDD)
            
        Returns:
            pd.DataFrame: 주식 시세 데이터
        """
        try:
            # 날짜 설정
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')

            # API 요청 파라미터
            params = {
                'serviceKey': self.api_key,
                'pageNo': '1',
                'numOfRows': '100',
                'resultType': 'json',
                'beginBasDt': start_date,
                'endBasDt': end_date
            }

            # API 호출
            response = requests.get(f"{self.base_url}/getStockPriceInfo", params=params)
            response.raise_for_status()

            # XML 응답 파싱
            root = ET.fromstring(response.content)
            
            # 데이터 추출
            items = []
            for item in root.findall('.//item'):
                data = {}
                for child in item:
                    data[child.tag] = child.text
                items.append(data)

            # DataFrame 생성
            df = pd.DataFrame(items)
            
            if df.empty:
                self.logger.warning("수집된 시장 데이터가 없습니다.")
                return pd.DataFrame()

            # 컬럼명 한글로 변경
            column_mapping = {
                'basDt': '기준일자',
                'srtnCd': '종목코드',
                'itmsNm': '종목명',
                'clpr': '종가',
                'vs': '대비',
                'fltRt': '등락률',
                'mkp': '시가',
                'hipr': '고가',
                'lopr': '저가',
                'trqu': '거래량',
                'trPrc': '거래대금',
                'lstgStCnt': '상장주식수',
                'mrktTotAmt': '시가총액'
            }
            
            df = df.rename(columns=column_mapping)
            
            # 숫자형 데이터 변환
            numeric_columns = ['종가', '대비', '등락률', '시가', '고가', '저가', '거래량', '거래대금', '상장주식수', '시가총액']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            self.logger.info(f"수집된 시장 데이터: {len(df)}개 종목")
            return df

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API 요청 중 오류 발생: {str(e)}")
            return pd.DataFrame()
        except ET.ParseError as e:
            self.logger.error(f"XML 파싱 중 오류 발생: {str(e)}")
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"데이터 처리 중 오류 발생: {str(e)}")
            return pd.DataFrame()

    def get_market_summary(self):
        """
        시장 요약 정보를 가져옵니다.
        
        Returns:
            dict: 시장 요약 정보
        """
        try:
            df = self.get_stock_data()
            if df.empty:
                return {}

            summary = {
                'total_stocks': len(df),
                'total_market_cap': df['시가총액'].sum(),
                'avg_price': df['종가'].mean(),
                'top_gainers': df.nlargest(5, '등락률')[['종목명', '등락률']].to_dict('records'),
                'top_losers': df.nsmallest(5, '등락률')[['종목명', '등락률']].to_dict('records')
            }

            return summary

        except Exception as e:
            self.logger.error(f"시장 요약 정보 생성 중 오류 발생: {str(e)}")
            return {} 