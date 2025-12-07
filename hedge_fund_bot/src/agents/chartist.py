"""
Chartist Agent - Technical analysis using Python REPL
"""

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_experimental.utilities import PythonREPL
from src.state import AgentState
import logging

logger = logging.getLogger(__name__)

llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0, max_tokens=2048)
repl = PythonREPL()


@tool
def python_repl_tool(code: str) -> str:
    """
    Execute Python code for financial analysis.
    
    Available: yfinance, pandas, numpy, matplotlib
    IMPORTANT: Use print() to display results.
    """
    try:
        result = repl.run(code)
        return f"Executed:\n{result}"
    except Exception as e:
        return f"Error: {repr(e)}"


CHARTIST_PROMPT = """You are a technical analyst. Analyze stock: {ticker}

Calculate:
1. Current price and change
2. SMA 20
3. RSI 14
4. MACD (12, 26, 9)
5. Support/Resistance (30-day highs/lows)

Use print() to show results. Use .head() for large data."""


def chartist_node(state: AgentState) -> dict:
    """Run technical analysis."""
    ticker = state.get("current_ticker", "UNKNOWN")
    
    # Add .SA for Brazilian stocks if needed
    if not ticker.endswith(".SA") and ticker.isalpha() and len(ticker) <= 5:
        ticker_yf = f"{ticker}.SA"
    else:
        ticker_yf = ticker
    
    try:
        tools = [python_repl_tool]
        agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
        executor = AgentExecutor(agent=agent, tools=tools, verbose=False, max_iterations=10)
        
        result = executor.invoke({"input": CHARTIST_PROMPT.format(ticker=ticker_yf)})
        logger.info(f"Chartist executed for {ticker}")
        
        return {"messages": [HumanMessage(content=f"[CHARTIST - {ticker}]\n\n{result.get('output', 'No result')}")]}
    
    except Exception as e:
        logger.error(f"Chartist error: {e}")
        return {"messages": [HumanMessage(content=f"[CHARTIST ERROR] {str(e)}")]}
