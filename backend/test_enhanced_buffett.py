#!/usr/bin/env python3
"""
Enhanced Warren Buffett Filter Tool 테스트 스크립트
8단계 투자 분석 시스템의 핵심 기능을 검증합니다.
"""

import asyncio
import sys
import os

# 프로젝트 루트 경로를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.buffett_filter_tool import BuffettFilter
from services.agent import get_agent
from services.esg_analysis_tool import esg_analyzer
from services.advanced_analysis_tool import advanced_analyzer

async def test_enhanced_buffett_filter():
    """Enhanced BuffettFilter 도구 테스트"""
    print("🔍 Enhanced Warren Buffett Filter 테스트 시작...")
    
    # 1. 기본 8단계 분석 테스트
    print("\n📊 1. 8단계 종합 분석 테스트")
    result = BuffettFilter._run(
        market_segment="KOSPI",
        min_score=70,
        max_results=5,
        include_esg=True,
        include_risk_analysis=True,
        use_real_data=False  # Mock 데이터 사용
    )
    print("✅ 8단계 분석 결과:")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # 2. ESG 전용 분석 테스트  
    print("\n🌱 2. ESG 중심 7단계 분석 테스트")
    result = BuffettFilter._run(
        market_segment="KOSPI",
        min_score=60,
        max_results=3,
        include_esg=True,
        include_risk_analysis=False,
        use_real_data=False
    )
    print("✅ ESG 분석 결과:")
    print(result[:300] + "..." if len(result) > 300 else result)
    
    # 3. 리스크 전용 분석 테스트
    print("\n⚠️ 3. 리스크 중심 7단계 분석 테스트")
    result = BuffettFilter._run(
        market_segment="KOSPI",
        min_score=60,
        max_results=3,
        include_esg=False,
        include_risk_analysis=True,
        use_real_data=False
    )
    print("✅ 리스크 분석 결과:")
    print(result[:300] + "..." if len(result) > 300 else result)
    
    # 4. 기존 6단계 분석 테스트
    print("\n📈 4. 전통적 6단계 분석 테스트")
    result = BuffettFilter._run(
        market_segment="KOSPI",
        min_score=50,
        max_results=3,
        include_esg=False,
        include_risk_analysis=False,
        use_real_data=False
    )
    print("✅ 전통적 분석 결과:")
    print(result[:300] + "..." if len(result) > 300 else result)

async def test_individual_tools():
    """개별 분석 도구 테스트"""
    print("\n🧪 개별 분석 도구 테스트 시작...")
    
    # ESG 분석 도구 테스트
    print("\n🌿 ESG 분석 도구 테스트")
    try:
        esg_result = await esg_analyzer.analyze_esg_score("005930", "반도체")
        print(f"✅ ESG 분석 성공: {esg_result['grade']} 등급")
        print(f"   전체 점수: {esg_result['overall_score']:.1f}")
        print(f"   Buffett 호환성: {esg_result['buffett_compatibility']['grade']}")
    except Exception as e:
        print(f"❌ ESG 분석 실패: {e}")
    
    # 고급 분석 도구 테스트
    print("\n📊 고급 분석 도구 테스트")
    try:
        # Mock 주식 데이터 생성
        mock_stock = {
            "symbol": "005930",
            "name": "삼성전자", 
            "current_price": 72000,
            "market_cap": 380000000,
            "beta": 1.2
        }
        
        risk_result = await advanced_analyzer.analyze_risk(mock_stock, [mock_stock])
        print(f"✅ 리스크 분석 성공: {risk_result.risk_grade}")
        print(f"   Beta: {risk_result.beta:.2f}")
        print(f"   변동성: {risk_result.volatility:.1%}")
    except Exception as e:
        print(f"❌ 리스크 분석 실패: {e}")

async def test_agent_integration():
    """에이전트 통합 테스트"""
    print("\n🤖 Warren Buffett Agent 통합 테스트...")
    
    try:
        agent = await get_agent()
        
        # 간단한 분석 요청
        question = "KOSPI 대형주 중에서 워런 버핏 기준으로 좋은 종목 3개 추천해주세요"
        result = await agent.analyze_stock(question)
        
        print("✅ 에이전트 분석 성공")
        print(f"   사용된 도구: {result['tools_used']}")
        print(f"   추천 수: {len(result['recommendations'])}")
        print("   첫 번째 추천:")
        if result['recommendations']:
            print(f"   {result['recommendations'][0]}")
            
    except Exception as e:
        print(f"❌ 에이전트 테스트 실패: {e}")

def print_test_summary():
    """테스트 요약 출력"""
    print("\n" + "="*60)
    print("🎯 Enhanced Warren Buffett Analysis System 테스트 완료")
    print("="*60)
    print("✅ 구현된 기능:")
    print("   • 8단계 종합 투자 분석 (6단계 + ESG + 리스크)")
    print("   • ESG 분석 및 Buffett 호환성 평가") 
    print("   • 고급 리스크 분석 (Beta, VaR, 변동성)")
    print("   • 포트폴리오 최적화 제안")
    print("   • 동적 가중치 시스템")
    print("   • 실시간 API 데이터 연동 지원")
    print("   • 강화된 AI Agent 통합")
    print("\n📡 API 엔드포인트:")
    print("   • POST /api/warren-buffett-analysis (8단계 분석)")
    print("   • POST /api/stock-analysis (일반 분석)")
    print("\n🔧 다음 단계:")
    print("   • 프론트엔드 UI 업데이트")
    print("   • 실제 API 데이터 연동 테스트")
    print("   • 사용자 피드백 수집 및 개선")

async def main():
    """메인 테스트 함수"""
    print("🚀 Enhanced Warren Buffett AI Agent 시스템 테스트")
    print("="*60)
    
    # 각 테스트 수행
    await test_enhanced_buffett_filter()
    await test_individual_tools()
    await test_agent_integration()
    
    # 테스트 요약
    print_test_summary()

if __name__ == "__main__":
    # 비동기 테스트 실행
    asyncio.run(main())
