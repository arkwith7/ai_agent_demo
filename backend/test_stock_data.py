import asyncio
import logging
from services.data_providers.financial_services_stock import fss_provider

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_stock_data():
    print("=== 한화 주가 데이터 테스트 ===")
    
    # 한화 데이터 조회
    data = await fss_provider.get_market_data("000880")
    
    if data:
        print("\n한화 데이터:")
        for item in data:
            print(f"- {item['itmsNm']} ({item['srtnCd']})")
            print(f"  현재가: {item['clpr']}원")
            print(f"  등락률: {item['fltRt']}%")
            print(f"  거래량: {item['trqu']}주")
            print(f"  시가총액: {item['mrktTotAmt']}원")
    else:
        print("데이터를 찾을 수 없습니다.")

if __name__ == "__main__":
    asyncio.run(test_stock_data()) 