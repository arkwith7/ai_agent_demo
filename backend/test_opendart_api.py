import asyncio
import sys
import os
from services.data_providers.opendart_api import OpenDARTProvider

print("[DEBUG] SCRIPT START")
print(f"[DEBUG] ENV OPEN_DART_API_KEY: {os.getenv('OPEN_DART_API_KEY')}")

async def main():
    symbol = "000660"  # SK하이닉스
    async with OpenDARTProvider() as dart:
        print(f"[OpenDART] API KEY: {dart.api_key}")
        print(f"[OpenDART] use_mock_data: {dart.use_mock_data}")
        sys.stdout.flush()
        # 최근 3년 재무제표 조회
        try:
            result = await dart.get_financial_statements(symbol, 3)
            print(f"[OpenDART] {symbol} 최근 3년 재무제표:")
            for fs in result:
                print(fs)
                sys.stdout.flush()
        except Exception as e:
            print(f"[OpenDART] API 호출 오류: {e}")
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
