"""Chartist Agent - Technical analysis using yfinance"""

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from src.state import AgentState
import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def get_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_tokens=1500)


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> float:
    """Calculate RSI."""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]


def calculate_macd(df: pd.DataFrame) -> dict:
    """Calculate MACD."""
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return {"macd": macd.iloc[-1], "signal": signal.iloc[-1], "histogram": (macd - signal).iloc[-1]}


CHARTIST_PROMPT = """You are a technical analyst. Analyze these indicators for {ticker}:

TECHNICAL DATA:
{technical_data}

Provide analysis covering:
1. Price action and trend
2. RSI interpretation (overbought >70, oversold <30)
3. MACD signal (bullish/bearish crossover)
4. Support and resistance levels
5. Overall technical outlook"""


def chartist_node(state: AgentState) -> dict:
    """Run technical analysis."""
    ticker = state.get("current_ticker", "UNKNOWN")
    
    # Normalize ticker for yfinance
    ticker_yf = ticker if ticker.endswith(".SA") or "." in ticker else ticker
    
    try:
        # Fetch data
        stock = yf.Ticker(ticker_yf)
        df = stock.history(period="3mo")
        
        if df.empty:
            # Try with .SA suffix for Brazilian stocks
            ticker_yf = f"{ticker}.SA"
            stock = yf.Ticker(ticker_yf)
            df = stock.history(period="3mo")
        
        if df.empty:
            return {"messages": [HumanMessage(content=f"[CHARTIST - {ticker}]\n\nNo data available for {ticker}")]}
        
        # Calculate indicators
        current_price = df['Close'].iloc[-1]
        price_change = ((current_price - df['Close'].iloc[-20]) / df['Close'].iloc[-20]) * 100
        sma20 = df['Close'].rolling(20).mean().iloc[-1]
        rsi = calculate_rsi(df)
        macd = calculate_macd(df)
        high_30d = df['High'].tail(30).max()
        low_30d = df['Low'].tail(30).min()
        
        technical_data = f"""
Current Price: ${current_price:.2f}
20-day Price Change: {price_change:.1f}%
SMA 20: ${sma20:.2f}
RSI (14): {rsi:.1f}
MACD: {macd['macd']:.4f}
MACD Signal: {macd['signal']:.4f}
MACD Histogram: {macd['histogram']:.4f}
30-day High (Resistance): ${high_30d:.2f}
30-day Low (Support): ${low_30d:.2f}
Price vs SMA20: {'Above' if current_price > sma20 else 'Below'}
"""
        
        # Generate analysis with LLM
        prompt = CHARTIST_PROMPT.format(ticker=ticker, technical_data=technical_data)
        response = get_llm().invoke([HumanMessage(content=prompt)])
        
        logger.info(f"Chartist executed for {ticker}")
        
        return {"messages": [HumanMessage(content=f"[CHARTIST - {ticker}]\n\n{technical_data}\n\nANALYSIS:\n{response.content}")]}
    
    except Exception as e:
        logger.error(f"Chartist error: {e}")
        return {"messages": [HumanMessage(content=f"[CHARTIST ERROR] {str(e)}")]}
