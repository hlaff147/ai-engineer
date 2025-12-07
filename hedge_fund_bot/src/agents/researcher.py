"""Researcher Agent - Searches for news and market sentiment"""

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from src.tools.search_tools import search_financial_news, search_market_sentiment
from src.state import AgentState
import logging

logger = logging.getLogger(__name__)


def get_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=1500)


RESEARCHER_PROMPT = """You are a financial researcher at a hedge fund.

Analyze the following news and market sentiment data for {ticker}, then provide a summary.

NEWS:
{news}

MARKET SENTIMENT:
{sentiment}

Provide a concise summary (max 300 words) covering:
1. Key recent news and events
2. Overall market sentiment (bullish/bearish/neutral)
3. Any red flags or positive catalysts"""


def researcher_node(state: AgentState) -> dict:
    """Search for news and analysis."""
    ticker = state.get("current_ticker", "UNKNOWN")
    
    try:
        # Search for news
        news_results = search_financial_news(f"{ticker} stock news", max_results=5)
        news_text = "\n".join([f"- {r.get('title', '')}: {r.get('body', '')[:200]}" for r in news_results]) or "No news found"
        
        # Search for sentiment
        sentiment_results = search_market_sentiment(ticker, max_results=5)
        sentiment_text = "\n".join([f"- {r.get('title', '')}: {r.get('body', '')[:200]}" for r in sentiment_results]) or "No sentiment data found"
        
        # Generate summary with LLM
        prompt = RESEARCHER_PROMPT.format(ticker=ticker, news=news_text, sentiment=sentiment_text)
        response = get_llm().invoke([HumanMessage(content=prompt)])
        
        logger.info(f"Researcher executed for {ticker}")
        
        return {"messages": [HumanMessage(content=f"[RESEARCHER - {ticker}]\n\n{response.content}")]}
    
    except Exception as e:
        logger.error(f"Researcher error: {e}")
        return {"messages": [HumanMessage(content=f"[RESEARCHER ERROR] {str(e)}")]}
