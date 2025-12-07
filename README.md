# AI Engineer Projects

A collection of AI/ML engineering projects exploring modern AI architectures, multi-agent systems, and LLM applications.

---

## 📁 Projects

<details>
<summary><strong>1. 🤖 Autonomous Hedge Fund Bot</strong> — Multi-agent stock analysis system</summary>

<br>

### [Autonomous Hedge Fund Bot](./hedge_fund_bot/)

A multi-agent AI system for automated stock analysis and investment recommendations.

**Tech Stack:** `LangGraph` `LangChain` `Groq` `Llama 3.1 70B` `yFinance`

**Features:**
| Feature | Description |
|---------|-------------|
| 🤖 Multi-Agent | Supervisor, Researcher, Chartist, Analyst agents |
| 📊 Technical Analysis | RSI, MACD, SMA indicators |
| 📰 Sentiment Analysis | Real-time news and market sentiment |
| 📝 Recommendations | Automated BUY/SELL/HOLD decisions |

**Architecture:**
```
User → Supervisor → Researcher → Chartist → Analyst → Report
            ↑___________|____________|___________|
```

**Quick Start:**
```bash
cd hedge_fund_bot
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add GROQ_API_KEY
python main.py
```

📖 [Full Documentation](./hedge_fund_bot/docs/DOCUMENTATION.md) | 📊 [View Diagrams](./hedge_fund_bot/docs/diagrams/)

</details>

<!-- 
TEMPLATE FOR NEW PROJECTS:

<details>
<summary><strong>2. 🚀 Project Name</strong> — Short description</summary>

<br>

### [Project Name](./project_folder/)

Description of the project.

**Tech Stack:** `Tech1` `Tech2` `Tech3`

**Features:**
| Feature | Description |
|---------|-------------|
| ✨ Feature 1 | Description |
| ✨ Feature 2 | Description |

**Quick Start:**
```bash
cd project_folder
# setup commands
```

📖 [Full Documentation](./project_folder/docs/DOCUMENTATION.md)

</details>
-->

---

## 🛠️ Technologies Used

| Category | Technologies |
|----------|-------------|
| **LLM Frameworks** | LangChain, LangGraph |
| **LLM Providers** | Groq (Llama 3.1 70B) |
| **Data Sources** | yFinance, DuckDuckGo |
| **Languages** | Python 3.11+ |

---

## 📂 Repository Structure

```
ai-engineer/
├── README.md                    # This file
├── hedge_fund_bot/              # Multi-agent stock analysis
│   ├── main.py                  # CLI entry point
│   ├── src/
│   │   ├── graph.py             # LangGraph workflow
│   │   ├── state.py             # Shared state schema
│   │   ├── agents/              # AI agents
│   │   └── tools/               # External integrations
│   ├── notebooks/               # Jupyter notebooks
│   └── docs/                    # Documentation & diagrams
└── [future_projects]/           # Coming soon...
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- API Keys (varies by project)

### Clone Repository
```bash
git clone https://github.com/hlaff147/ai-engineer.git
cd ai-engineer
```

### Navigate to Project
Each project has its own README with specific setup instructions.

---

## 📜 License

This repository is for educational and research purposes.

---

## 👤 Author

**Humberto Laff**
- GitHub: [@hlaff147](https://github.com/hlaff147)

---

*Last updated: December 2025*
