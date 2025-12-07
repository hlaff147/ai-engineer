"""Supervisor Agent - Routes workflow based on current state"""

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from src.state import AgentState
import json
import logging

logger = logging.getLogger(__name__)


def get_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_tokens=256)

SUPERVISOR_PROMPT = """You are a senior hedge fund manager.

Workers: Researcher, Chartist, Analyst

Rules:
- If Researcher never ran, send to Researcher
- If Researcher finished, send to Chartist  
- If both finished, send to Analyst
- If final report exists, respond FINISH
- Never send to same agent twice in a row

Respond with JSON only:
{{"next": "Researcher|Chartist|Analyst|FINISH", "reasoning": "brief reason"}}

History: {messages}
Ticker: {ticker}
Iteration: {iteration}"""


def supervisor_node(state: AgentState) -> dict:
    """Route to next agent."""
    messages_str = "\n".join([f"[{m.type}]: {m.content[:100]}..." for m in state["messages"][-10:]])
    
    prompt = SUPERVISOR_PROMPT.format(
        messages=messages_str,
        ticker=state.get("current_ticker", "UNKNOWN"),
        iteration=state.get("iteration_count", 0),
    )
    
    try:
        response = get_llm().invoke([HumanMessage(content=prompt)])
        text = response.content.strip()
        
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()
        
        result = json.loads(text)
        next_agent = result.get("next", "FINISH")
        
        logger.info(f"Supervisor: {next_agent}")
        return {"next": next_agent, "messages": [HumanMessage(content=f"[SUPERVISOR] Next: {next_agent}")]}
    
    except Exception as e:
        logger.error(f"Supervisor error: {e}")
        for agent in ["Researcher", "Chartist", "Analyst"]:
            if agent in str(response.content):
                return {"next": agent}
        return {"next": "FINISH"}
