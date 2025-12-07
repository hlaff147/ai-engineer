# Autonomous Hedge Fund

Multi-agent stock analysis system using LangGraph, LangChain, and Groq.

## Architecture

```
User → Supervisor → Researcher → Chartist → Analyst → Report
            ↑___________|____________|___________|
```

| Agent | Role | Tools |
|-------|------|-------|
| Supervisor | Routes workflow | None (JSON output) |
| Researcher | News & sentiment | DuckDuckGo |
| Chartist | Technical analysis | Python REPL + yfinance |
| Analyst | Final report | None |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add GROQ_API_KEY to .env
```

## Usage

```bash
# CLI
python main.py

# Notebook
jupyter notebook notebooks/hedge_fund_analysis.ipynb
```

## Structure

```
hedge_fund_bot/
├── src/
│   ├── agents/     # Supervisor, Researcher, Chartist, Analyst
│   ├── tools/      # Financial & search tools
│   ├── state.py    # AgentState schema
│   └── graph.py    # LangGraph workflow
├── notebooks/
├── main.py
└── requirements.txt
```

## License

MIT
