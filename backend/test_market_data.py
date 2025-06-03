import asyncio
from services.data_providers.financial_services_stock import fss_provider

async def test_market_data():
    print("=== 시장 데이터 수집 테스트 시작 ===")
    
    # 전체 시장 데이터 조회
    data = await fss_provider.get_market_data()
    print(f"\n수집된 종목 수: {len(data)}")
    
    if data:
        print("\n첫 3개 종목:")
        for item in data[:3]:
            print(f"- {item['itmsNm']} ({item['srtnCd']}): {item['clpr']}원")
    
    # 특정 종목 데이터 조회 (삼성전자)
    print("\n=== 삼성전자 데이터 조회 ===")
    samsung_data = await fss_provider.get_market_data("005930")
    if samsung_data:
        for item in samsung_data:
            print(f"- {item['itmsNm']} ({item['srtnCd']}): {item['clpr']}원")

if __name__ == "__main__":
    asyncio.run(test_market_data()) 