from langchain_openai import AzureChatOpenAI
from core.config import settings
import tiktoken

chat_llm = AzureChatOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_key=settings.AZURE_OPENAI_API_KEY,
    azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
    openai_api_version=settings.OPENAI_API_VERSION,
)

def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

async def get_ai_response(user_query: str) -> tuple[str, int, int]:
    response_content = await chat_llm.ainvoke(user_query)
    ai_message = response_content.content
    input_tokens = count_tokens(user_query, model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME)
    output_tokens = count_tokens(ai_message, model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME)
    return ai_message, input_tokens, output_tokens

async def summarize_conversation(query_text: str, response_text: str) -> tuple[str, int, int]:
    """대화 내용을 요약하는 함수"""
    
    # 요약 프롬프트 구성
    summarize_prompt = f"""
다음 대화를 간결하고 핵심적인 내용으로 요약해주세요. 주요 질문과 답변의 핵심 포인트를 포함하여 2-3문장으로 정리해주세요.

사용자 질문: {query_text}

AI 응답: {response_text}

요약:
"""
    
    try:
        # AI 요약 생성
        response_content = await chat_llm.ainvoke(summarize_prompt)
        summary = response_content.content
        
        # 토큰 계산
        input_tokens = count_tokens(summarize_prompt, model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME)
        output_tokens = count_tokens(summary, model_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME)
        
        return summary, input_tokens, output_tokens
        
    except Exception as e:
        # 요약 실패 시 기본 요약 반환
        default_summary = f"질문: {query_text[:50]}{'...' if len(query_text) > 50 else ''}"
        return default_summary, 0, 0
