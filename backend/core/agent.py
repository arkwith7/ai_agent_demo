from langchain import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Define the tools that the agent can use
from .tools.buffett_filter_tool import BuffettFilterTool
from .tools.news_tool import NewsTool
from .tools.valuation_tool import ValuationTool

# Initialize the OpenAI model
llm = OpenAI(temperature=0)

# Define the prompt template for the agent
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="You are an investment analysis expert. Based on the user's query, analyze the stocks and recommend those that meet Warren Buffett's investment criteria. If necessary, call the appropriate tools to gather and process data."
)

# Create the LangChain agent
tools = [
    Tool(name="BuffettFilterTool", func=BuffettFilterTool().run, description="Filters stocks based on Warren Buffett's criteria."),
    Tool(name="NewsTool", func=NewsTool().run, description="Summarizes news sentiment."),
    Tool(name="ValuationTool", func=ValuationTool().run, description="Predicts 5-year FCF and compares market cap.")
]

agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

def process_query(question: str):
    response = agent({"question": question})
    return response