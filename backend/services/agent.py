import asyncio
import json
from typing import List, Dict, Any
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.tools import BaseTool
from core.config import settings
from services.buffett_filter_tool_simple import BuffettFilter
from services.advanced_analysis_tool import AdvancedAnalysisTool
from services.logger import LoggerService
from services.data_providers.financial_services_stock import fss_provider
from services.data_providers.opendart_api import opendart_provider

logger = LoggerService()

class StockAnalysisAgent:
    """
    주식 분석을 수행하는 AI 에이전트
    """
    def __init__(self):
        self.fss = fss_provider
        self.opendart = opendart_provider
        self.logger = LoggerService()

    async def collect_market_data(self, stock_code: str = "") -> List[Dict[str, Any]]:
        """시장 데이터를 수집합니다."""
        try:
            if stock_code:
                stock_data = await self.fss.get_stock_price(stock_code)
                return [stock_data] if stock_data else []
            else:
                return await self.fss.get_market_data()
        except Exception as e:
            self.logger.error(f"시장 데이터 수집 중 오류 발생: {str(e)}")
            return []

    async def collect_financial_data(self, stock_code: str) -> Dict[str, Any]:
        """재무 데이터를 수집합니다."""
        try:
            return await self.opendart.get_company_financials(stock_code)
        except Exception as e:
            self.logger.error(f"재무 데이터 수집 중 오류 발생: {str(e)}")
            return {}

class WarrenBuffettAgent:
    """
    워런 버핏 투자 기준을 적용한 AI 주식 분석 에이전트
    """
    def __init__(self):
        # Azure OpenAI LLM 초기화
        self.llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
            openai_api_version=settings.OPENAI_API_VERSION,
        )
        
        # 도구 초기화
        self.tools = [
            BuffettFilter(),
            AdvancedAnalysisTool()
        ]
        
        # 시스템 프롬프트 설정
        system_prompt = """당신은 워렌 버핏의 투자 철학을 따르는 주식 분석 전문가입니다.
        다음 도구들을 사용하여 주식 분석을 수행하세요:
        1. 버핏 필터: 워렌 버핏의 투자 기준에 따라 종목을 평가
        2. 뉴스 분석: 관련 뉴스와 시장 동향 분석
        3. 가치 평가: 기업의 내재가치와 적정주가 평가
        4. 고급 분석: 기술적, 펀더멘털, 시장 심리 분석
        
        분석 결과는 다음 형식으로 제공하세요:
        1. 종목 개요
        2. 버핏 기준 평가
        3. 가치 평가
        4. 리스크 분석
        5. 투자 추천
        """
        
        # 에이전트 초기화
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )
    
    async def analyze_stock(self, question: str) -> Dict[str, Any]:
        """
        주식 분석을 수행하고 결과를 반환합니다.
        """
        try:
            logger.info(f"Starting stock analysis for question: {question}")
            # 에이전트 실행
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.agent_executor.invoke({"input": question})
            )
            analysis_output = result.get("output", "")
            # 구조화된 JSON 파싱 시도
            try:
                parsed = json.loads(analysis_output) if isinstance(analysis_output, str) else analysis_output
                # content_type, structured_data, text 필드가 있으면 그대로 반환
                if isinstance(parsed, dict) and "content_type" in parsed:
                    logger.info("Structured JSON result detected from agent.")
                    return {
                        "recommendations": [parsed.get("text", "")],
                        "raw_output": analysis_output,
                        "tools_used": self._extract_tools_used(result),
                        "success": True,
                        "content_type": parsed.get("content_type"),
                        "structured_data": parsed.get("structured_data"),
                        "text": parsed.get("text", "")
                    }
            except Exception as e:
                logger.warning(f"Agent output is not valid JSON: {e}")
            # fallback: 기존 텍스트 파싱
            recommendations = self._parse_analysis_output(analysis_output)
            logger.info(f"Analysis completed with {len(recommendations)} recommendations")
            return {
                "recommendations": recommendations,
                "raw_output": analysis_output,
                "tools_used": self._extract_tools_used(result),
                "success": True,
                "content_type": "text",
                "structured_data": None,
                "text": analysis_output
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
                "success": False,
                "content_type": "text",
                "structured_data": None,
                "text": str(e)
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
    
    def _extract_tools_used(self, result: Dict[str, Any]) -> List[str]:
        """
        에이전트 실행 중 사용된 도구 목록을 추출
        """
        tools_used = []
        if "intermediate_steps" in result:
            for step in result["intermediate_steps"]:
                if isinstance(step, tuple) and len(step) > 0:
                    tool_name = step[0].tool
                    if tool_name not in tools_used:
                        tools_used.append(tool_name)
        return tools_used

# 전역 에이전트 인스턴스
_agent_instance = None

async def get_agent() -> StockAnalysisAgent:
    """
    싱글톤 패턴으로 에이전트 인스턴스 반환
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = StockAnalysisAgent()
    return _agent_instance

async def process_query(question: str) -> List[str]:
    """
    주식 분석 질문 처리 (기존 API 호환성을 위한 래퍼 함수)
    """
    try:
        agent = await get_agent()
        market_data = await agent.collect_market_data()
        if not market_data:
            return ["❌ 시장 데이터를 가져올 수 없습니다."]
        
        return [f"📊 분석된 종목 수: {len(market_data)}개"]
    except Exception as e:
        logger.error(f"질문 처리 중 오류 발생: {str(e)}")
        return [f"❌ 오류가 발생했습니다: {str(e)}"]