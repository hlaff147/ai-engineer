"""Analyst Agent - Synthesizes final investment report"""

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from src.state import AgentState
import logging

logger = logging.getLogger(__name__)


def get_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4, max_tokens=1500)

ANALYST_PROMPT = """You are a senior portfolio manager. Write a final investment report.

Ticker: {ticker}

Analysis history:
{context}

Report structure (max 400 words):
- Executive Summary (1 paragraph)
- Fundamental Analysis (news-based)
- Technical Analysis (indicators)
- Recommendation: BUY / SELL / HOLD
- Justification (2-3 sentences)
- Risk Level: High / Medium / Low

Use markdown formatting."""


def analyst_node(state: AgentState) -> dict:
    """Generate final report."""
    ticker = state.get("current_ticker", "UNKNOWN")
    context = "\n".join([f"{m.type}: {m.content[:200]}..." for m in state.get("messages", [])[-5:]])
    
    try:
        response = get_llm().invoke([HumanMessage(content=ANALYST_PROMPT.format(ticker=ticker, context=context))])
        logger.info(f"Analyst executed for {ticker}")
        
        return {"messages": [HumanMessage(content=f"[ANALYST - FINAL REPORT]\n\n{response.content}")]}
    
    except Exception as e:
        logger.error(f"Analyst error: {e}")
        return {"messages": [HumanMessage(content=f"[ANALYST ERROR] {str(e)}")]}
