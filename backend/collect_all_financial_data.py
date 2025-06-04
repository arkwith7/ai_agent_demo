import argparse
import asyncio
import json
import logging
import os
import sys
import time
from typing import Dict, Any, List, Optional
import datetime

# 프로젝트 루트 디렉토리를 sys.path에 추가하여 내부 모듈 임포트
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# 이제 내부 모듈 임포트 가능
try:
    from services.data_providers.opendart_api import OpenDARTProvider
    from services.stock_analysis import StockAnalysisService # KOSPI 종목 목록 가져오기용
    from services.logger import LoggerService # 프로젝트 로거 사용 시
except ImportError as e:
    print(f"Error importing project modules: {e}")
    print("Please ensure the script is in the \'backend\' directory and the project structure is correct.")
    sys.exit(1)

# 로깅 설정
log_dir = os.path.join(project_root, 'backend', 'log')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(log_dir, 'collect_financial_data_script.log'))
    ]
)
logger = logging.getLogger(__name__)

# 데이터 저장 디렉토리
DEFAULT_OUTPUT_DIR = os.path.join(project_root, 'backend', 'data', 'financial_data')

async def fetch_and_save_financial_data(
    opendart_provider: OpenDARTProvider,
    stock_code: str,
    stock_name: str,
    output_dir: str,
    overwrite: bool
) -> bool:
    """특정 종목의 재무 데이터를 가져와 JSON 파일로 저장합니다."""
    output_path = os.path.join(output_dir, f"{stock_code}_financials.json")

    if not overwrite and os.path.exists(output_path):
        logger.info(f"File already exists for {stock_code} ({stock_name}) and overwrite is false. Skipping.")
        return True # 이미 존재하고 덮어쓰지 않으므로 성공으로 간주

    try:
        logger.info(f"Fetching financial statement for {stock_code} ({stock_name})")
        # OpenDARTProvider의 get_financial_statement는 corp_code, bsns_year, reprt_code를 받음
        # 최근 3개년 사업보고서(11011)를 가져오도록 가정
        # 실제 get_financial_statement는 하나의 사업보고서 내용을 반환하므로, 여러 해를 가져오려면 반복 호출 필요
        # 여기서는 단순화를 위해 가장 최근 사업보고서의 전체 항목을 가져온다고 가정.
        # 또는, 해당 메소드가 이미 여러 기간을 포함하여 반환한다고 가정.
        # 실제 API와 Provider 구현에 따라 이 부분은 조정이 필요할 수 있음.
        # 지금은 provider가 한번의 호출로 해당 종목의 "모든" 재무제표 항목을 가져온다고 가정.
        
        # 참고: 원래 OpenDARTProvider.get_financial_statement는 다음과 같은 파라미터를 받습니다.
        # (self, corp_code: str, bsns_year: str, reprt_code: str = "11011", fs_div: Optional[str] = None)
        # 한 번에 모든 연도의 모든 재무제표를 가져오는 기능은 없으므로,
        # 최근 3-5개년 정도를 루프 돌면서 가져오거나, 별도의 포괄적인 함수가 Provider에 필요.
        # 여기서는 설명을 위해 "전체 재무제표 항목"으로 가정하고,
        # 실제로는 가장 최근 3개년의 주요 재무제표를 가져오는 식으로 구현해야 함.
        
        # 여기서는 시범적으로 최근 3개년(2023, 2022, 2021) 사업보고서를 가져온다고 가정
        financial_statements_all_years: List[Dict[str, Any]] = []
        current_year = datetime.datetime.now().year
        
        report_years_to_fetch = [str(current_year - 1 - year_offset) for year_offset in range(3)]

        for report_year in report_years_to_fetch:
            try:
                logger.debug(f"Fetching {report_year} financial statement for {stock_code}")
                # fs_div (재무제표 구분 OFS: 개별/연결, CFS: 연결) - 연결재무제표 우선
                # OpenDARTProvider.get_financial_statement는 이제 reprt_code와 fs_div를 인자로 받음
                stmt_cfs = await opendart_provider.get_financial_statement(corp_code=stock_code, bsns_year=report_year, reprt_code="11011", fs_div="CFS")
                if stmt_cfs and stmt_cfs.get('status') == '000' and stmt_cfs.get('list'):
                    financial_statements_all_years.extend(stmt_cfs['list'])
                else:
                    logger.debug(f"CFS not found for {stock_code} {report_year}, trying OFS. Status: {stmt_cfs.get('status')}, Message: {stmt_cfs.get('message')}")
                    stmt_ofs = await opendart_provider.get_financial_statement(corp_code=stock_code, bsns_year=report_year, reprt_code="11011", fs_div="OFS")
                    if stmt_ofs and stmt_ofs.get('status') == '000' and stmt_ofs.get('list'):
                        financial_statements_all_years.extend(stmt_ofs['list'])
                    else:
                        logger.warning(f"Could not fetch financial statement (CFS/OFS) for {stock_code} {report_year}. Status CFS: {stmt_cfs.get('status')}, OFS: {stmt_ofs.get('status')}")
            except Exception as e_fs_year:
                logger.warning(f"Exception while fetching {report_year} financial statement for {stock_code}: {e_fs_year}")

        # 배당 정보 수집 로직 수정
        dividends_for_json = []
        logger.info(f"Fetching dividend history for {stock_code} ({stock_name}) for years: {report_years_to_fetch}")
        for dividend_year in report_years_to_fetch: # 재무제표와 동일한 연도 범위 사용
            try:
                logger.debug(f"Fetching {dividend_year} dividend report for {stock_code}")
                dividend_report_raw = await opendart_provider.get_dividend_report(corp_code=stock_code, bsns_year=dividend_year)
                
                if dividend_report_raw and dividend_report_raw.get('status') == '000' and dividend_report_raw.get('list'):
                    for item in dividend_report_raw['list']:
                        # OpenDART alotMatter.json 응답에서 현금 배당금액 필드는 'cdd' (주당현금배당금액) 또는 'cash_div_smt' 등 API 버전에 따라 다를 수 있음.
                        # 예시 JSON과 유사하게 처리하기 위해 'cdd'를 우선 확인하고, 없으면 'cash_div_smt' 시도.
                        dps_str = item.get('cdd') # 주당 현금 배당금 (DART 표준)
                        if dps_str is None:
                            dps_str = item.get('cash_div_smt') # 이전 스크립트에서 사용하던 키 (혹시 모를 호환성)
                        
                        # 배당금액 문자열이 유효한지 확인 (숫자 또는 '-' 형태)
                        if dps_str and dps_str.strip() != "-":
                            try:
                                dps_value = float(dps_str.replace(',', '').strip())
                                dividends_for_json.append({
                                    "year": int(dividend_year), # 해당 조회 연도
                                    "dps": dps_value
                                })
                                logger.debug(f"Added dividend for {stock_code} year {dividend_year}: {dps_value}")
                            except ValueError:
                                logger.warning(f"Could not parse DPS '{dps_str}' for {stock_code} in year {dividend_year}")
                elif dividend_report_raw and dividend_report_raw.get('status') != '000':
                     logger.warning(f"Failed to fetch dividend data for {stock_code} year {dividend_year}. Status: {dividend_report_raw.get('status')}, Message: {dividend_report_raw.get('message')}")

            except Exception as e_div_year:
                logger.warning(f"Exception while fetching {dividend_year} dividend report for {stock_code}: {e_div_year}")
        
        # 데이터 가공
        financial_data_json = {
            "company_info": {
                "corp_code": stock_code,
                "corp_name": stock_name
            },
            "financial_statements": financial_statements_all_years, # API 응답 리스트
            "dividend_info": {"dividends": dividends_for_json}
        }

        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(financial_data_json, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved financial data for {stock_code} ({stock_name}) to {output_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to fetch or save data for {stock_code} ({stock_name}): {e}", exc_info=True)
        return False

async def main(args):
    logger.info("Starting financial data collection script.")
    
    # 명령줄 인자로 API 키가 제공되면 환경 변수 설정
    if args.api_key:
        os.environ['OPEN_DART_API_KEY'] = args.api_key
        logger.info("Using API key provided via command-line argument.")

    # settings를 통해 API 키를 읽어오므로, OpenDARTProvider 초기화 시 인자 불필요
    # API 키 존재 여부는 OpenDARTProvider 내부에서 확인 (settings.OPEN_DART_API_KEY 사용)
    # 또는 스크립트 시작 시점에서 settings.OPEN_DART_API_KEY를 직접 확인할 수도 있음
    
    # settings 모듈을 다시 로드하거나, settings 값이 동적으로 반영된다고 가정.
    # 가장 확실한 방법은 settings.py에서 환경변수를 읽는 시점인데,
    # 여기서는 스크립트 실행 전에 환경변수가 설정되거나, 여기서 설정 후 provider가 읽는다고 가정.
    
    # API 키 확인 로직 (선택적 강화)
    # from core.config import settings # 다시 import 하거나, 이미 로드된 settings 사용
    # if not settings.OPEN_DART_API_KEY:
    #     logger.error("OpenDART API key is not set. Please set OPEN_DART_API_KEY environment variable or use --api_key argument.")
    #     return

    opendart_provider = OpenDARTProvider() # api_key 인자 제거
    stock_service = StockAnalysisService() # 로컬 CSV에서 시장 데이터 로드용

    logger.info(f"Loading market data for {args.market} market...")
    try:
        # StockAnalysisService.collect_market_data는 이미 로컬 CSV를 사용함
        market_data_list = await stock_service.collect_market_data(market_type=args.market)
        if not market_data_list:
            logger.error(f"No market data found for {args.market}. Exiting.")
            return
        logger.info(f"Loaded {len(market_data_list)} stocks from {args.market} market data.")
    except Exception as e:
        logger.error(f"Failed to load market data: {e}", exc_info=True)
        return

    # 처리할 종목 범위 설정 (선택적)
    start_idx = args.start_index if args.start_index is not None else 0
    end_idx = args.end_index if args.end_index is not None else len(market_data_list)
    
    # 인덱스가 유효한 범위 내에 있는지 확인
    start_idx = max(0, start_idx)
    end_idx = min(len(market_data_list), end_idx)

    if start_idx >= end_idx:
        logger.info(f"Start index ({start_idx}) is greater than or equal to end index ({end_idx}). No stocks to process.")
        return
        
    stocks_to_process = market_data_list[start_idx:end_idx]
    
    logger.info(f"Processing {len(stocks_to_process)} stocks (index {start_idx} to {end_idx-1}). Output directory: {args.output_dir}")

    success_count = 0
    fail_count = 0

    for i, stock_info in enumerate(stocks_to_process):
        stock_code = stock_info.get('종목코드')
        stock_name = stock_info.get('종목명')

        if not stock_code or not stock_name:
            logger.warning(f"Skipping item with missing stock code or name: {stock_info}")
            continue
        
        logger.info(f"Processing stock {start_idx + i + 1}/{len(market_data_list)} (Overall): {stock_code} ({stock_name})")
        
        if await fetch_and_save_financial_data(opendart_provider, stock_code, stock_name, args.output_dir, args.overwrite):
            success_count += 1
        else:
            fail_count += 1
        
        if i < len(stocks_to_process) - 1: # 마지막 요청 후에는 sleep 불필요
            logger.debug(f"Waiting for {args.delay} seconds before next API call...")
            time.sleep(args.delay)

    logger.info("Financial data collection finished.")
    logger.info(f"Successfully processed: {success_count} stocks.")
    logger.info(f"Failed to process: {fail_count} stocks.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect financial data for KOSPI/KOSDAQ stocks using OpenDART API.")
    parser.add_argument("--api_key", type=str, help="OpenDART API key. If provided, it overrides the OPEN_DART_API_KEY environment variable for this script run.")
    parser.add_argument("--market", type=str, default="KOSPI", choices=['KOSPI', 'KOSDAQ'], help="Market to collect data for (KOSPI or KOSDAQ).")
    parser.add_argument("--output_dir", type=str, default=DEFAULT_OUTPUT_DIR, help="Directory to save JSON files.")
    parser.add_argument("--overwrite", action='store_true', help="Overwrite existing files if they exist.")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay in seconds between API calls to avoid rate limiting.")
    parser.add_argument("--start_index", type=int, help="0-based start index of stocks to process from the market list.")
    parser.add_argument("--end_index", type=int, help="0-based end index (exclusive) of stocks to process.")
    
    args = parser.parse_args()

    # Python 3.7+ 에서는 asyncio.run() 사용 가능
    if sys.version_info >= (3, 7):
        asyncio.run(main(args))
    else: # 이전 버전 호환성 (필요시)
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(main(args))
        finally:
            loop.close() 