"""
Researcher Agent - Searches for news and market sentiment
"""

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from src.tools.search_tools import search_financial_news, search_market_sentiment
from src.state import AgentState
import logging

logger = logging.getLogger(__name__)

llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.3, max_tokens=1024)


@tool
def search_news(query: str) -> str:
    """Search financial news about a stock or company."""
    results = search_financial_news(query, max_results=5)
    if not results:
        return f"No news found for '{query}'"
    
    formatted = "News found:\n"
    for i, r in enumerate(results, 1):
        formatted += f"\n{i}. {r.get('title', 'No title')}\n   {r.get('body', '')}\n"
    return formatted


@tool
def search_sentiment(ticker: str) -> str:
    """Search market sentiment for a stock."""
    results = search_market_sentiment(ticker, max_results=5)
    if not results:
        return f"No sentiment found for {ticker}"
    
    formatted = f"Sentiment for {ticker}:\n"
    for i, r in enumerate(results, 1):
        formatted += f"\n{i}. {r.get('title', 'No title')}\n   {r.get('body', '')}\n"
    return formatted


RESEARCHER_PROMPT = """You are a financial researcher. Search for news and market sentiment about: {ticker}

Steps:
1. Search for general news
2. Search for market sentiment
3. Summarize findings (max 300 words)"""


def researcher_node(state: AgentState) -> dict:
    """Search for news and analysis."""
    ticker = state.get("current_ticker", "UNKNOWN")
    
    try:
        tools = [search_news, search_sentiment]
        agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
        executor = AgentExecutor(agent=agent, tools=tools, verbose=False, max_iterations=5)
        
        result = executor.invoke({"input": RESEARCHER_PROMPT.format(ticker=ticker)})
        logger.info(f"Researcher executed for {ticker}")
        
        return {"messages": [HumanMessage(content=f"[RESEARCHER - {ticker}]\n\n{result.get('output', 'No result')}")]}
    
    except Exception as e:
        logger.error(f"Researcher error: {e}")
        return {"messages": [HumanMessage(content=f"[RESEARCHER ERROR] {str(e)}")]}
