import asyncio
import json
from typing import List, Dict, Any
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.tools import BaseTool
from core.config import settings
from services.buffett_filter_tool import BuffettFilter
from services.news_tool import NewsTool
from services.valuation_tool import ValuationTool
import logging

logger = logging.getLogger(__name__)

class WarrenBuffettAgent:
    """
    워런 버핏 투자 기준을 적용한 AI 주식 분석 에이전트
    """
    
    def __init__(self):
        # Azure OpenAI LLM 초기화
        self.llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            openai_api_version=settings.OPENAI_API_VERSION,
            azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
            temperature=0.1,  # 일관된 분석을 위해 낮은 온도 설정
            max_tokens=2000
        )
        
        # 분석 도구들 초기화
        self.tools = [
            BuffettFilter,
            NewsTool(),
            ValuationTool()
        ]
        
        # 워런 버핏 투자 기준 프롬프트
        self.system_prompt = """
당신은 워런 버핏의 투자 철학을 정확히 구현하는 AI 투자 분석가입니다.

## 워런 버핏의 6단계 투자 기준

1. **시가총액 기준**: 상위 30% 대형주만 고려
2. **자기자본이익률(ROE)**: 최근 3년간 평균 15% 이상
3. **수익성**: 순이익률과 FCF가 업종 평균 이상
4. **성장성**: 시가총액 증가율 > 자본 증가율
5. **미래가치**: 5년 예상 FCF 합계 > 현재 시가총액
6. **가치평가**: PER/PBR 대비 내재가치 평가

## 분석 지침

- 각 기준을 체계적으로 평가하고 점수를 매기세요 (0-100점)
- 정량적 데이터와 정성적 분석을 균형있게 제시하세요
- 투자 추천은 Buy/Hold/Sell로 명확히 구분하세요
- 위험 요소와 기회 요소를 균형있게 분석하세요
- 이모지를 사용해 시각적으로 이해하기 쉽게 표현하세요

사용 가능한 도구들을 활용하여 종합적인 분석을 제공하세요.
"""
        
        # 프롬프트 템플릿 생성
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # 에이전트 생성
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 에이전트 실행기 생성
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            early_stopping_method="generate"
        )
    
    async def analyze_stock(self, question: str) -> Dict[str, Any]:
        """
        주식 분석 수행
        
        Args:
            question: 사용자의 분석 질문
            
        Returns:
            Dict: 분석 결과와 메타데이터
        """
        try:
            logger.info(f"Starting stock analysis for question: {question}")
            
            # 에이전트 실행
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.agent_executor.invoke({"input": question})
            )
            
            # 결과 파싱
            analysis_output = result.get("output", "")
            
            # 분석 결과를 구조화된 형태로 변환
            recommendations = self._parse_analysis_output(analysis_output)
            
            logger.info(f"Analysis completed with {len(recommendations)} recommendations")
            
            return {
                "recommendations": recommendations,
                "raw_output": analysis_output,
                "tools_used": self._extract_tools_used(result),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error in stock analysis: {str(e)}")
            return {
                "recommendations": [
                    f"❌ 분석 중 오류가 발생했습니다: {str(e)}",
                    "💡 다시 시도하시거나 다른 종목으로 질문해주세요."
                ],
                "raw_output": str(e),
                "tools_used": [],
                "success": False
            }
    
    def _parse_analysis_output(self, output: str) -> List[str]:
        """
        AI 분석 결과를 사용자 친화적인 추천 리스트로 변환
        """
        if not output:
            return ["❌ 분석 결과를 가져올 수 없습니다."]
        
        # 줄바꿈으로 분리하고 빈 줄 제거
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        
        if not lines:
            return [output]
        
        # 분석 결과를 구조화
        recommendations = []
        current_section = ""
        
        for line in lines:
            # 섹션 제목 감지 (##, **, 등으로 시작)
            if line.startswith(('##', '**', '###')):
                current_section = line.strip('#* ')
                recommendations.append(f"📊 **{current_section}**")
            
            # 불릿 포인트 또는 번호 매김 감지
            elif line.startswith(('-', '•', '*')) or any(line.startswith(f"{i}.") for i in range(1, 10)):
                cleaned_line = line.lstrip('-•* 0123456789.')
                if cleaned_line:
                    recommendations.append(f"  {cleaned_line}")
            
            # 일반 텍스트
            elif len(line) > 10:  # 너무 짧은 줄은 제외
                recommendations.append(line)
        
        return recommendations if recommendations else [output]
    
    def _extract_tools_used(self, result: Dict) -> List[str]:
        """
        사용된 도구들 추출
        """
        tools_used = []
        
        # intermediate_steps에서 사용된 도구 정보 추출
        intermediate_steps = result.get("intermediate_steps", [])
        
        for step in intermediate_steps:
            if len(step) >= 1 and hasattr(step[0], 'tool'):
                tools_used.append(step[0].tool)
        
        return list(set(tools_used))  # 중복 제거

# 전역 에이전트 인스턴스
_agent_instance = None

async def get_agent() -> WarrenBuffettAgent:
    """
    싱글톤 패턴으로 에이전트 인스턴스 반환
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = WarrenBuffettAgent()
    return _agent_instance

async def process_query(question: str) -> List[str]:
    """
    주식 분석 질문 처리 (기존 API 호환성을 위한 래퍼 함수)
    
    Args:
        question: 사용자의 분석 질문
        
    Returns:
        List[str]: 분석 결과 추천 리스트
    """
    try:
        agent = await get_agent()
        result = await agent.analyze_stock(question)
        return result["recommendations"]
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return [
            f"❌ 질문 처리 중 오류가 발생했습니다: {str(e)}",
            "💡 네트워크 연결을 확인하시거나 잠시 후 다시 시도해주세요.",
            "🔧 문제가 지속되면 관리자에게 문의해주세요."
        ]