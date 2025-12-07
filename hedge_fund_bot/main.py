"""
Main CLI Entry Point
"""

import os
import sys
import logging
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.graph import create_graph
from src.state import AgentState

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if not os.getenv("GROQ_API_KEY"):
    print("Error: GROQ_API_KEY not configured")
    sys.exit(1)


def run_analysis(ticker: str) -> dict:
    """Run complete stock analysis."""
    print(f"\nStarting analysis for {ticker}...")
    
    graph = create_graph()
    
    initial_state: AgentState = {
        "messages": [HumanMessage(content=f"Analyze stock {ticker}")],
        "next": "Supervisor",
        "current_ticker": ticker,
        "current_stock_data": {},
        "iteration_count": 0,
    }
    
    try:
        return graph.invoke(initial_state, config={"recursion_limit": 25})
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return initial_state


def print_report(state: dict) -> None:
    """Display final report."""
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60 + "\n")
    
    for msg in state.get("messages", []):
        if "[ANALYST" in msg.content:
            print(msg.content.replace("[ANALYST - FINAL REPORT]\n\n", ""))
            break


def main():
    print("\n" + "="*60)
    print("AUTONOMOUS HEDGE FUND")
    print("="*60)
    print("LangGraph + Groq + Llama 3.1 70b\n")
    
    while True:
        ticker = input("Enter ticker (or 'exit'): ").strip().upper()
        
        if ticker == 'EXIT':
            print("Goodbye!")
            break
        
        if not ticker:
            continue
        
        result = run_analysis(ticker)
        print_report(result)


if __name__ == "__main__":
    main()
