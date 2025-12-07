"""
LangGraph Workflow - Multi-agent orchestration
"""

from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.supervisor import supervisor_node
from src.agents.researcher import researcher_node
from src.agents.chartist import chartist_node
from src.agents.analyst import analyst_node
import logging

logger = logging.getLogger(__name__)


def create_graph():
    """Create and compile the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Researcher", researcher_node)
    workflow.add_node("Chartist", chartist_node)
    workflow.add_node("Analyst", analyst_node)
    
    # Workers return to Supervisor
    workflow.add_edge("Researcher", "Supervisor")
    workflow.add_edge("Chartist", "Supervisor")
    workflow.add_edge("Analyst", "Supervisor")
    
    # Supervisor routes conditionally
    workflow.add_conditional_edges(
        "Supervisor",
        lambda x: x["next"],
        {"Researcher": "Researcher", "Chartist": "Chartist", "Analyst": "Analyst", "FINISH": END}
    )
    
    workflow.set_entry_point("Supervisor")
    
    return workflow.compile()
