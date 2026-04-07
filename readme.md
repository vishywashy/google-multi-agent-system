# 🤖 Autonomous Multi-Agent Orchestrator
### PyTorch Router | LangGraph | Google Workspace | Discord UI

A sophisticated, stateful AI ecosystem that utilizes a custom **PyTorch Intent Router** to orchestrate specialized **LangGraph Agents**. This system enables autonomous management of **Google Calendar** and **Gmail** through a real-time **Discord interface**, featuring advanced ReAct (Reasoning & Acting) logic.

## 🧠 System Architecture

1.  **Intent Classification (PyTorch):** A custom neural network router that analyzes user input to determine the optimal workflow path.
2.  **Agent Orchestration (LangGraph):** Manages complex, stateful loops between agents, ensuring memory persistence and multi-step reasoning.
3.  **Specialized Agents:**
    *   **Gmail Agent:** Autonomous email drafting, searching, and formatting.
    *   **Calendar Agent:** Intelligent scheduling, conflict detection, and RFC datetime management.
4.  **Interface Layer (Discord):** A fully integrated bot hosting the agents, providing a "Human-in-the-Loop" experience.

## 🛠 Tech Stack
- **AI Core:** PyTorch (Neural Routing), Ollama (LLM), LangGraph (State Machine).
- **Automation:** LangGraph, Transformers, Scikit-learn.
- **APIs:** Google OAuth2 (Calendar/Gmail), Discord.py.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running.
- Google Cloud Console Project with Calendar/Gmail APIs enabled.

### Installation
1. **Clone the repository:**
   ```bash
   git clone vishywashy/google-multi-agent-system
   cd vishywashy/google-multi-agent-system