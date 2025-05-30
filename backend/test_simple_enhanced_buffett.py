#!/usr/bin/env python3
"""
Enhanced Warren Buffett AI Agent 시스템 간단 테스트
"""
import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.buffett_filter_tool_simple import BuffettFilter
from services.agent import get_agent

async def test_simple_buffett_filter():
    """간단한 BuffettFilter 도구 테스트"""
    print("🔍 Simple Enhanced Warren Buffett Filter 테스트 시작...")
    
    # 1. 기본 8단계 종합 분석 테스트
    print("\n📊 1. 8단계 종합 분석 테스트")
    tool = BuffettFilter
    
    try:
        result = tool._run(
            market_segment="KOSPI",
            min_score=60,
            max_results=5,
            include_esg=True,
            include_risk_analysis=True,
            use_real_data=False  # Mock 데이터 사용
        )
        print("✅ 8단계 종합 분석 성공")
        print(f"결과 길이: {len(result)} 문자")
        
        # JSON 파싱 테스트
        import json
        parsed = json.loads(result)
        print(f"✅ JSON 파싱 성공 - 추천 종목 수: {len(parsed.get('top_recommendations', []))}")
        
    except Exception as e:
        print(f"❌ 8단계 종합 분석 실패: {e}")
        return False

    # 2. ESG만 포함한 분석 테스트
    print("\n📊 2. ESG 포함 분석 테스트")
    try:
        result = tool._run(
            market_segment="KOSPI",
            min_score=50,
            max_results=3,
            include_esg=True,
            include_risk_analysis=False,
            use_real_data=False
        )
        print("✅ ESG 포함 분석 성공")
        
    except Exception as e:
        print(f"❌ ESG 포함 분석 실패: {e}")

    # 3. 리스크만 포함한 분석 테스트
    print("\n📊 3. 리스크 분석 포함 테스트")
    try:
        result = tool._run(
            market_segment="KOSPI",
            min_score=50,
            max_results=3,
            include_esg=False,
            include_risk_analysis=True,
            use_real_data=False
        )
        print("✅ 리스크 분석 포함 성공")
        
    except Exception as e:
        print(f"❌ 리스크 분석 포함 실패: {e}")

    return True

async def test_agent_integration():
    """Agent 통합 테스트"""
    print("\n🤖 Enhanced Warren Buffett Agent 통합 테스트 시작...")
    
    try:
        agent = await get_agent()
        print("✅ Agent 초기화 성공")
        
        # 간단한 질문 테스트
        test_query = "삼성전자에 대한 워런 버핏 8단계 투자 기준 분석을 해주세요"
        
        result = await agent.analyze_stock(test_query)
        
        if result["success"]:
            print("✅ Agent 분석 성공")
            print(f"추천 개수: {len(result['recommendations'])}")
            print(f"사용된 도구: {result['tools_used']}")
        else:
            print(f"❌ Agent 분석 실패: {result['raw_output']}")
            
    except Exception as e:
        print(f"❌ Agent 통합 테스트 실패: {e}")

async def main():
    """메인 테스트 함수"""
    print("🚀 Enhanced Warren Buffett AI Agent 간단 시스템 테스트")
    print("=" * 60)
    
    # 1. BuffettFilter 도구 테스트
    success = await test_simple_buffett_filter()
    
    if success:
        print("\n" + "=" * 60)
        
        # 2. Agent 통합 테스트
        await test_agent_integration()
    
    print("\n" + "=" * 60)
    print("🎯 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(main())
