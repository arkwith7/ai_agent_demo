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
