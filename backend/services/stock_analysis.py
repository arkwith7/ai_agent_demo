from typing import List, Dict, Any, Optional
from datetime import datetime
# from schemas.analysis import StockRecommendation, StockAnalysis # 직접 사용 안 함
from services.data_providers.opendart_api import OpenDARTProvider, opendart_provider # 로컬 파일로 대체 예정
from services.data_providers.financial_services_stock import FinancialServicesStockProvider, fss_provider # 로컬 파일로 대체 예정
from services.logger import LoggerService
import pandas as pd
import os
import logging # 표준 로깅 사용 시
import glob # 추가
import json # 추가

# 로그 디렉토리 생성
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
os.makedirs(log_dir, exist_ok=True)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(log_dir, 'stock_analysis.log'))
    ]
)

logger = logging.getLogger(__name__)
logger.info(f"로그 디렉토리 생성/확인: {log_dir}")

class StockAnalysisService:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StockAnalysisService, cls).__new__(cls)
            cls._instance._initialized = False 
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.logger_service = LoggerService() 
        # 클래스 레벨 로거보다는 인스턴스별 로거 또는 이름있는 로거 사용 권장
        # 기존 logger = logging.getLogger(__name__) 가 있다면 그것을 사용하거나 아래처럼 수정
        # self.logger = self.logger_service.get_logger(type(self).__name__)  # 이 줄 제거

        # 데이터 디렉토리 경로 설정 (os.path.abspath 사용으로 좀 더 명확하게)
        # __file__ 은 현재 파일의 경로
        # os.path.dirname(__file__) 은 services 디렉토리
        # os.path.dirname(os.path.dirname(__file__)) 은 backend 디렉토리
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_root_dir = os.path.join(backend_dir, 'data')
        self.market_data_dir = os.path.join(self.data_root_dir, 'market_data')
        self.financial_data_dir = os.path.join(self.data_root_dir, 'financial_data')
        
        os.makedirs(self.market_data_dir, exist_ok=True)
        os.makedirs(self.financial_data_dir, exist_ok=True)
        
        self.logger_service.info(f"StockAnalysisService initialized. Data directories set.")
        self.logger_service.info(f"Market data directory: {self.market_data_dir}")
        self.logger_service.info(f"Financial data directory: {self.financial_data_dir}")

        # 기존 provider 초기화는 우선 유지 (다음 단계에서 제거/수정)
        if not hasattr(self, 'opendart'):
            self.opendart = opendart_provider 
        if not hasattr(self, 'fss'):
            self.fss = fss_provider
            
        self._initialized = True

    async def get_latest_market_data_path(self) -> Optional[str]:
        """ 가장 최신의 시장 데이터 CSV 파일 경로를 반환합니다. """
        try:
            # market_data_YYYYMMDD_HHMMSS.csv 형식의 파일들을 찾습니다.
            list_of_files = glob.glob(os.path.join(self.market_data_dir, 'market_data_*.csv'))
            if not list_of_files:
                self.logger_service.warning("No market data CSV files found.")
                return None
            
            # 파일명에서 날짜시간 부분을 추출하여 최신 파일 찾기
            def extract_datetime_from_filename(f_path):
                try:
                    # 파일명 예: market_data_20231027_153045.csv
                    name_part = os.path.basename(f_path).replace('market_data_', '').replace('.csv', '')
                    return datetime.strptime(name_part, '%Y%m%d_%H%M%S')
                except ValueError:
                    # 파일명 형식이 다를 경우, 생성 시간(ctime)으로 대체 (덜 정확할 수 있음)
                    self.logger_service.warning(f"Could not parse datetime from filename {os.path.basename(f_path)}, using ctime.")
                    return datetime.fromtimestamp(os.path.getctime(f_path))

            latest_file = max(list_of_files, key=extract_datetime_from_filename)
            self.logger_service.info(f"Latest market data file identified: {latest_file}")
            return latest_file
        except Exception as e:
            self.logger_service.error(f"Error finding latest market data file: {e}", exc_info=True)
            return None

    async def collect_market_data(self, market_type: str = "KOSPI") -> List[Dict[str, Any]]:
        """ 로컬 CSV 파일에서 시장 데이터를 수집합니다. """
        try:
            self.logger_service.info(f"Collecting market data from local CSV for market: {market_type}")
            latest_csv_path = await self.get_latest_market_data_path()
            
            if not latest_csv_path or not os.path.exists(latest_csv_path):
                self.logger_service.warning(f"Latest market data CSV file not found or path is invalid: {latest_csv_path}")
                return []

            # 종목코드를 문자열로 읽도록 dtype 명시
            df = pd.read_csv(latest_csv_path, dtype={'종목코드': str})
            df.columns = df.columns.astype(str) # 모든 컬럼명을 문자열로 변환

            if '종목코드' in df.columns:
                 df['종목코드'] = df['종목코드'].astype(str).str.zfill(6)
            else:
                self.logger_service.warning("'종목코드' column not found in the CSV file.")
                # 종목코드가 없으면 데이터 처리가 어려우므로 빈 리스트 반환 또는 예외 처리
                return []
            
            # Pandas DataFrame의 NaN 값을 Python None으로 변환
            df = df.where(pd.notnull(df), None)
            market_data = df.to_dict(orient='records')
            self.logger_service.info(f"Successfully collected {len(market_data)} market data entries from {latest_csv_path}")
            return market_data
        except FileNotFoundError: # 위에서 체크하지만 이중 방어
            # 이 변수는 try 블록 내에서만 유효할 수 있으므로, 정의되지 않았을 경우를 대비
            path_for_log_fnf = latest_csv_path if 'latest_csv_path' in locals() and latest_csv_path is not None else self.market_data_dir
            self.logger_service.error(f"Market data CSV file not found (FileNotFoundError): {path_for_log_fnf}")
            return []
        except pd.errors.EmptyDataError:
            path_for_log_empty = latest_csv_path if 'latest_csv_path' in locals() and latest_csv_path is not None else 'Unknown CSV path'
            self.logger_service.error(f"Market data CSV file is empty: {path_for_log_empty}")
            return []
        except Exception as e:
            self.logger_service.error(f"Error collecting market data from CSV: {e}", exc_info=True)
            return []

    async def collect_financial_data(self, stock_code: str) -> Dict[str, Any]:
        """ 로컬 JSON 파일에서 특정 종목의 재무 데이터를 수집합니다. 파일이 없으면 기본 빈 딕셔너리를 반환합니다. """
        stock_code_padded = stock_code.zfill(6)
        financial_file_path = os.path.join(self.financial_data_dir, f"{stock_code_padded}_financials.json")
        self.logger_service.info(f"Attempting to collect financial data for stock: {stock_code_padded} from {financial_file_path}")
        
        # 반환될 기본 데이터 구조 정의
        default_empty_data = {
            "company_info": {"corp_code": stock_code_padded, "corp_name": f"{stock_code_padded} (No Local File)"},
            "financial_statements": [],
            "dividend_info": {} # 또는 주요 주주 정보 필드 등 API 응답과 유사한 구조
        }

        try:
            if os.path.exists(financial_file_path):
                with open(financial_file_path, 'r', encoding='utf-8') as f:
                    financial_data = json.load(f)
                self.logger_service.info(f"Successfully loaded financial data for {stock_code_padded} from local file.")
                # 로드된 데이터에 필수 키가 없을 경우를 대비하여 기본값으로 채워줍니다.
                financial_data.setdefault("company_info", default_empty_data["company_info"])
                financial_data.setdefault("financial_statements", default_empty_data["financial_statements"])
                financial_data.setdefault("dividend_info", default_empty_data["dividend_info"])
                # company_info 내부에도 corp_code, corp_name 등이 없을 경우 대비
                if isinstance(financial_data["company_info"], dict):
                    financial_data["company_info"].setdefault("corp_code", stock_code_padded)
                    financial_data["company_info"].setdefault("corp_name", f"{stock_code_padded} (Name Missing in File)")
                else: # company_info가 딕셔너리가 아닌 경우 (잘못된 파일 형식 등)
                    financial_data["company_info"] = default_empty_data["company_info"]
                return financial_data
            else:
                self.logger_service.warning(f"Financial data file not found for {stock_code_padded} at {financial_file_path}. Returning default empty data.")
                return default_empty_data
        except json.JSONDecodeError as e:
            self.logger_service.error(f"Error decoding JSON financial data for {stock_code_padded} from {financial_file_path}: {e}", exc_info=True)
            # JSON 파싱 오류 시에도 기본 빈 데이터 반환
            return {**default_empty_data, "company_info": {"corp_code": stock_code_padded, "corp_name": f"{stock_code_padded} (JSON Error)"}}
        except Exception as e:
            self.logger_service.error(f"Error collecting financial data for {stock_code_padded} from local file: {e}", exc_info=True)
            # 기타 예외 발생 시에도 기본 빈 데이터 반환
            return {**default_empty_data, "company_info": {"corp_code": stock_code_padded, "corp_name": f"{stock_code_padded} (Unknown Error)"}}

    async def get_specific_stock_market_data(self, stock_code: str) -> List[Dict[str, Any]]:
        """ 로컬 CSV에서 특정 종목의 시장 데이터를 가져옵니다. """
        try:
            self.logger_service.info(f"Getting specific stock market data for: {stock_code}")
            all_market_data = await self.collect_market_data() # 이미 로컬 CSV를 사용
            if not all_market_data:
                self.logger_service.warning(f"No market data available to filter for stock: {stock_code}")
                return []
            
            stock_code_padded = stock_code.zfill(6)
            specific_data = [
                stock for stock in all_market_data 
                if stock.get('종목코드') == stock_code_padded
            ]
            
            if not specific_data:
                self.logger_service.warning(f"Stock code {stock_code_padded} not found in the collected market data.")
            else:
                self.logger_service.info(f"Found specific market data for {stock_code_padded}: {len(specific_data)} entr(y/ies)")
            return specific_data
        except Exception as e:
            self.logger_service.error(f"Error getting specific stock market data for {stock_code}: {e}", exc_info=True)
            return []

    def _safe_float_conversion(self, value: Optional[Any], default: float = 0.0) -> float:
        """안전하게 값을 float으로 변환합니다. 변환 실패 시 default 값을 반환합니다."""
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return float(value)
        try:
            # 문자열의 경우 쉼표 제거 후 변환
            return float(str(value).replace(',', ''))
        except (ValueError, TypeError):
            # self.logger.debug(f"Could not convert '{value}' to float, returning default {default}")
            return default

    def evaluate_buffett_criteria(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """워렌 버핏의 투자 기준에 따라 종목을 평가합니다."""
        scores = {
            "market_cap_score": 0.0,
            "roe_score": 0.0,        # 우선 0으로 초기화
            "profit_margin_score": 0.0, # 우선 0으로 초기화
            "debt_ratio_score": 0.0,  # 우선 0으로 초기화
            "dividend_score": 0.0,    # 우선 0으로 초기화
        }
        stock_code_for_log = "Unknown"
        reason_message = "Evaluation based on available data."
        meets_criteria_flag = False
        total_score_calculated = 0.0

        try:
            market_data = data.get("market_data", {})
            financial_data = data.get("financial_data", {})
            
            stock_code_for_log = (
                market_data.get('종목코드') or 
                (financial_data.get("company_info", {}).get("corp_code") 
                 if isinstance(financial_data.get("company_info"), dict) else None) or 
                "Unknown"
            )

            # 1. 시가총액 평가
            market_cap_str = market_data.get("시가총액") or market_data.get("mrktTotAmt")
            market_cap = self._safe_float_conversion(market_cap_str)
            if market_cap_str is None and market_data:
                 self.logger_service.debug(f"[{stock_code_for_log}] Market cap data (시가총액 or mrktTotAmt) not found in market_data.")
            scores["market_cap_score"] = self._evaluate_market_cap(market_cap, stock_code_for_log)

            # financial_statements 및 기타 재무 관련 데이터 추출 (다음 단계에서 사용)
            financial_statements = financial_data.get("financial_statements", [])
            if not isinstance(financial_statements, list):
                self.logger_service.warning(f"[{stock_code_for_log}] financial_statements is not a list, received: {type(financial_statements)}. Treating as empty.")
                financial_statements = []
            
            scores["roe_score"] = self._evaluate_roe(financial_statements, stock_code_for_log)
            scores["profit_margin_score"] = self._evaluate_profit_margin(financial_statements, stock_code_for_log)
            scores["debt_ratio_score"] = self._evaluate_debt_ratio(financial_statements, stock_code_for_log)
            
            # 주석 해제 및 dividend_info 가져오기
            dividend_info = financial_data.get("dividend_info", {})
            scores["dividend_score"] = self._evaluate_dividend(dividend_info, financial_statements, stock_code_for_log)

            valid_scores = [s for s in scores.values() if isinstance(s, (int, float))]
            total_score_calculated = sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
            
            key_criteria_met = (
                scores.get("roe_score", 0) >= 40 and 
                scores.get("profit_margin_score", 0) >= 40 and 
                scores.get("debt_ratio_score", 0) >= 40 and
                scores.get("market_cap_score", 0) >= 40 # 시가총액도 주요 기준으로 포함 (예시)
            )
            meets_criteria_flag = key_criteria_met and total_score_calculated >= 50
            
            reason_parts = [f"{key.replace('_score','').replace('_',' ').capitalize()}: {value:.0f}" for key, value in scores.items()]
            reason_message = ", ".join(reason_parts) + f" (Total: {total_score_calculated:.0f})"
            if not meets_criteria_flag and total_score_calculated > 0 : # 기준 미달이지만 점수가 있다면
                reason_message = f"Did not meet all key Buffett criteria. {reason_message}"
            elif not meets_criteria_flag : # 점수도 거의 없다면
                reason_message = f"Insufficient data or does not meet Buffett criteria. {reason_message}"

        except Exception as e:
            self.logger_service.error(f"[{stock_code_for_log}] Error evaluating Buffett criteria: {e}", exc_info=True)
            reason_message = f"Error during Buffett criteria evaluation for {stock_code_for_log}."
            # scores는 기본 0점으로 유지, total_score 0, meets_criteria False

        return {
            "scores": scores, 
            "total_score": total_score_calculated,
            "meets_criteria": meets_criteria_flag,
            "reason": reason_message
        }

    def _evaluate_market_cap(self, market_cap: float, stock_code: str = "Unknown") -> float:
        """시가총액을 평가하여 점수를 반환합니다."""
        if market_cap <= 0: 
            # self.logger.debug(f"[{stock_code}] Market cap is {market_cap}, score: 0")
            return 0.0
        score = 0.0
        if market_cap >= 1_000_000_000_000: # 1조 이상
            score = 100.0
        elif market_cap >= 500_000_000_000: # 5천억 이상
            score = 80.0
        elif market_cap >= 100_000_000_000: # 1천억 이상
            score = 60.0
        elif market_cap >= 50_000_000_000: # 5백억 이상
            score = 40.0
        else: # 그 외
            score = 20.0
        # self.logger.debug(f"[{stock_code}] Market cap: {market_cap:.0f}, score: {score}")
        return score

    def _extract_yearly_financial_data(self, financial_statements: List[Dict[str, Any]], stock_code: str, num_years: int = 3) -> Dict[str, Dict[str, Optional[float]]]:
        """
        financial_statements에서 최근 N개년 연간(사업보고서) 재무 데이터를 추출하여 연도별 딕셔너리로 반환합니다.
        예: {'2022': {'net_income': 100, 'equity': 500, 'revenue': 800, 'debt': 300, 'cash_dividend': 10}, ...}
        """
        yearly_data: Dict[str, Dict[str, Optional[float]]] = {}
        if not financial_statements:
            return yearly_data

        # 계정 ID 또는 이름과 내부적으로 사용할 키 매핑
        # 실제 OpenDART 응답은 account_id (IFRS 코드) 또는 account_nm (계정명)을 포함합니다.
        # 우선 account_nm을 기준으로 하고, 일반적인 IFRS 계정 ID도 고려합니다.
        account_mapping = {
            'net_income': ['당기순이익', '연결당기순이익', '포괄손익계산서_당기순이익', '손익계산서_당기순이익', 'Profit (loss)', 'ProfitLoss'],
            'equity': ['자본총계', '자본', '지배기업 소유주지분', 'Equity'],
            'revenue': ['매출액', '수익(매출액)', '영업수익', 'Revenue'],
            'debt': ['부채총계', 'Liabilities'],
            'cash_dividend': ['현금배당금', '배당금의 지급', '현금및현금성자산의감소'] # 현금흐름표에서 배당금 지급액을 찾을 때 사용
        }

        # 연도별, 대표 계정별 데이터 집계
        raw_yearly_data: Dict[str, Dict[str, List[float]]] = {}

        for item in financial_statements:
            bsns_year = item.get('bsns_year')
            reprt_code = item.get('reprt_code') # 11011: 사업보고서 (연간)
            account_name = item.get('account_nm')
            account_id = item.get('account_id')
            amount_str = item.get('thstrm_amount')
            sj_div = item.get('sj_div') # BS, IS, CF 등 재무제표 구분
            account_detail = item.get('account_detail') # 배당금 지급 상세 확인용

            if not all([bsns_year, reprt_code, amount_str]):
                continue
            
            if reprt_code != '11011': # 연간 사업보고서 데이터만 사용
                continue

            if bsns_year not in raw_yearly_data:
                raw_yearly_data[bsns_year] = {key: [] for key in account_mapping.keys()}

            val = self._safe_float_conversion(amount_str, None)
            if val is None:
                continue

            for key_internal, possible_names in account_mapping.items():
                # account_id가 IFRS 표준 코드에 해당하거나, account_nm이 일반적인 이름에 해당하면 추가
                # 배당금의 경우 특별 처리: 현금흐름표(CF)의 '현금및현금성자산의감소' 항목 중 account_detail이 배당금 관련일 때
                is_dividend_payment = False
                if key_internal == 'cash_dividend' and sj_div == 'CF' and account_name in possible_names:
                    if isinstance(account_detail, str) and ('배당금지급' in account_detail or '배당금 지급' in account_detail):
                        is_dividend_payment = True
                
                if is_dividend_payment or account_name in possible_names or (account_id and any(mapped_id.lower() in account_id.lower() for mapped_id in possible_names)):
                    raw_yearly_data[bsns_year][key_internal].append(val)
                    break # 하나의 내부 키에 매핑되면 다음 항목으로
        
        # 각 연도, 각 항목에 대해 값 정리 (예: 여러 항목이 매칭된 경우 합계 또는 평균 등, 여기서는 첫번째 값 또는 합계를 가정)
        # 손익계산서 항목은 보통 하나지만, 재무상태표 항목은 연결/별도 등이 섞여있을 수 있음.
        # 여기서는 가장 단순하게 리스트의 첫번째 값을 사용 (또는 합계가 적절한 경우 sum)
        sorted_years = sorted(raw_yearly_data.keys(), reverse=True)[:num_years]
        for year in sorted_years:
            yearly_data[year] = {}
            for key_internal in account_mapping.keys():
                values_for_key = raw_yearly_data[year].get(key_internal, [])
                if values_for_key:
                    # 당기순이익, 매출액 등은 보통 단일 값. 자본, 부채도 연결재무제표 기준 단일 값.
                    # 만약 여러개가 잡힌다면, 가장 대표적인 값이나 합계를 사용해야 함. 지금은 첫번째 값.
                    # 현금배당금은 지출이므로 음수일 수 있음. 절대값을 취하거나 부호를 유지.
                    # 여기서는 배당금 지급액이므로 양수로 가정 (이미 지출된 금액)
                    yearly_data[year][key_internal] = values_for_key[0]
                else:
                    yearly_data[year][key_internal] = None # 해당 연도에 값이 없음
            
            # self.logger.debug(f"[{stock_code}/{year}] Extracted: NI={yearly_data[year].get('net_income')}, Eq={yearly_data[year].get('equity')}, Rev={yearly_data[year].get('revenue')}, Debt={yearly_data[year].get('debt')}, Div={yearly_data[year].get('cash_dividend')}")

        return yearly_data

    def _evaluate_roe(self, financial_statements: List[Dict[str, Any]], stock_code: str = "Unknown") -> float:
        yearly_data = self._extract_yearly_financial_data(financial_statements, stock_code, num_years=3)
        if not yearly_data: return 0.0
        
        roes = []
        for year_data in yearly_data.values():
            net_income = year_data.get('net_income')
            equity = year_data.get('equity')
            if net_income is not None and equity is not None and equity > 0:
                roes.append((net_income / equity) * 100)
        
        if not roes: return 0.0
        avg_roe = sum(roes) / len(roes)
        self.logger_service.debug(f"[{stock_code}] Avg ROE ({len(roes)} years): {avg_roe:.2f}%")

        if avg_roe >= 15: return 100.0
        if avg_roe >= 10: return 80.0
        if avg_roe >= 5: return 60.0
        if avg_roe > 0: return 40.0
        return 0.0

    def _evaluate_profit_margin(self, financial_statements: List[Dict[str, Any]], stock_code: str = "Unknown") -> float:
        yearly_data = self._extract_yearly_financial_data(financial_statements, stock_code, num_years=3)
        if not yearly_data: return 0.0

        margins = []
        for year_data in yearly_data.values():
            net_income = year_data.get('net_income')
            revenue = year_data.get('revenue')
            if net_income is not None and revenue is not None and revenue > 0:
                margins.append((net_income / revenue) * 100)
        
        if not margins: return 0.0
        avg_margin = sum(margins) / len(margins)
        self.logger_service.debug(f"[{stock_code}] Avg Profit Margin ({len(margins)} years): {avg_margin:.2f}%")

        if avg_margin >= 20: return 100.0
        if avg_margin >= 10: return 80.0
        if avg_margin >= 5: return 60.0
        if avg_margin > 0: return 40.0
        return 0.0

    def _evaluate_debt_ratio(self, financial_statements: List[Dict[str, Any]], stock_code: str = "Unknown") -> float:
        # 부채비율은 가장 최근 연도 중시
        yearly_data = self._extract_yearly_financial_data(financial_statements, stock_code, num_years=1)
        if not yearly_data: return 0.0
        
        # num_years=1 이므로, yearly_data는 하나의 연도만 포함하거나 비어있음
        latest_year_data = next(iter(yearly_data.values()), None) 
        if not latest_year_data: return 0.0

        debt = latest_year_data.get('debt')
        equity = latest_year_data.get('equity')
        
        if debt is None or equity is None or equity <= 0:
             self.logger_service.debug(f"[{stock_code}] Debt or Equity not available for Debt Ratio. Debt: {debt}, Equity: {equity}")
             return 0.0 # 부채 또는 자본 정보가 없거나 자본이 0 이하면 점수 없음

        debt_ratio = (debt / equity) * 100
        self.logger_service.debug(f"[{stock_code}] Latest Debt Ratio: {debt_ratio:.2f}%")

        if debt_ratio < 50: return 100.0
        if debt_ratio < 100: return 80.0
        if debt_ratio < 150: return 60.0
        if debt_ratio < 200: return 40.0
        return 0.0

    def _evaluate_dividend(self, dividend_info: Dict[str, Any], financial_statements: List[Dict[str, Any]], stock_code: str = "Unknown") -> float:
        # dividend_info 우선 사용 (예: { "dividends": [ {"year":2022, "dps":500}, ... ] } )
        # 없다면 financial_statements에서 추출한 현금배당금 사용
        has_consistent_dividend = False
        avg_payout_ratio = None # 배당성향
        num_years_with_dividend = 0

        if dividend_info and isinstance(dividend_info.get('dividends'), list) and dividend_info['dividends']:
            self.logger_service.debug(f"[{stock_code}] Using dividend_info for dividend evaluation.")
            dps_values = [d.get('dps', 0) for d in dividend_info['dividends'] if isinstance(d, dict) and d.get('year')]
            dps_values = [dps for dps in dps_values if dps > 0]
            if len(dps_values) >= 2: # 최소 2년 이상 배당 기록
                has_consistent_dividend = True
            num_years_with_dividend = len(dps_values)
        else:
            self.logger_service.debug(f"[{stock_code}] Using financial_statements for dividend evaluation.")
            yearly_data = self._extract_yearly_financial_data(financial_statements, stock_code, num_years=3)
            if yearly_data:
                payout_ratios_temp = []
                dividends_paid_this_many_years = 0
                for year_data in yearly_data.values():
                    cash_dividend = year_data.get('cash_dividend') # 추출된 현금배당금 (양수 값으로 가정)
                    net_income = year_data.get('net_income')
                    if cash_dividend is not None and cash_dividend > 0:
                        dividends_paid_this_many_years +=1
                        if net_income is not None and net_income > 0:
                            payout_ratios_temp.append((cash_dividend / net_income) * 100)
                
                if dividends_paid_this_many_years >=2: # 최소 2년 이상 배당
                    has_consistent_dividend = True
                num_years_with_dividend = dividends_paid_this_many_years
                if payout_ratios_temp:
                    avg_payout_ratio = sum(payout_ratios_temp) / len(payout_ratios_temp)
        
        self.logger_service.debug(f"[{stock_code}] Dividend evaluation - Consistent: {has_consistent_dividend}, Years with div: {num_years_with_dividend}, Avg Payout: {avg_payout_ratio}")

        if has_consistent_dividend and num_years_with_dividend >= 2:
            if avg_payout_ratio is not None and 10 <= avg_payout_ratio <= 70: # 적정 배당 성향
                return 80.0
            return 60.0 # 꾸준한 배당은 하지만 성향이 너무 낮거나 높거나 알수 없음
        elif num_years_with_dividend > 0: # 한해라도 배당했다면
             return 40.0
        return 20.0 # 배당 기록 거의 없거나 불명확

    # _evaluate_management 함수가 있다면 그것도 유사하게 처리
    # def _evaluate_management(self, company_info: Dict[str, Any], stock_code: str = "Unknown") -> float:
    #     self.logger.debug(f"[{stock_code}] _evaluate_management called. Company info present: {bool(company_info)}. Returning placeholder 50.0")
    #     return 50.0

    async def get_latest_market_data_df(self) -> Optional[pd.DataFrame]:
        """ 가장 최신의 시장 데이터 CSV 파일을 DataFrame으로 반환합니다. """
        try:
            latest_csv_path = await self.get_latest_market_data_path()
            if not latest_csv_path or not os.path.exists(latest_csv_path):
                self.logger_service.warning(f"Latest market data CSV file not found for DataFrame: {latest_csv_path}")
                return None

            df = pd.read_csv(latest_csv_path, dtype={'종목코드': str})
            df.columns = df.columns.astype(str)
            if '종목코드' in df.columns:
                 df['종목코드'] = df['종목코드'].astype(str).str.zfill(6)
            else:
                self.logger_service.warning("Cannot create DataFrame: '종목코드' column not found.")
                return None # 종목코드 없으면 DataFrame 생성 의미 없음
            
            self.logger_service.info(f"Loaded latest market data into DataFrame from {latest_csv_path}")
            return df
        except Exception as e:
            self.logger_service.error(f"Error loading latest market data into DataFrame: {e}", exc_info=True)
            return None

    # 기존 OpenDART 및 FSS Provider를 사용하는 메소드들은 제거하거나 주석 처리.
    # 예를 들어, 원래의 OpenDART API를 호출하던 collect_financial_data는 이미 로컬 JSON 사용으로 대체됨.
    # 원래의 FSS API를 호출하던 collect_market_data는 이미 로컬 CSV 사용으로 대체됨.
    # get_recommendations, get_detailed_analysis 등 서비스의 상위 레벨 함수들은
    # 이제 수정된 collect_market_data, collect_financial_data를 호출하여 로컬 데이터를 사용하게 됨.
    # 만약 해당 상위 레벨 함수들이 아직도 이전 provider 인스턴스(self.opendart, self.fss)를 직접 사용한다면
    # 해당 부분도 수정이 필요함. 현재 제공된 코드에서는 이 함수들의 전체 내용이 보이지 않아 확인 불가.

# StockAnalysisService 클래스 외부의 함수나 인스턴스 생성 (예: service = StockAnalysisService())
# 등은 이 파일의 다른 부분에 있을 수 있음.

# 싱글톤 인스턴스 생성
stock_analysis = StockAnalysisService() 