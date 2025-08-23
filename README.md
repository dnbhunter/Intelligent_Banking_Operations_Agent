# Intelligent Banking Operations Agent 🤖🏦

This project implements a multi-agent system to automate and assist in critical banking operations, including fraud detection and credit risk assessment. It serves as a proof-of-concept for building sophisticated, AI-powered financial systems using modern tools like FastAPI, LangChain, and a React-based UI.

## ✨ Features

- **Multi-Agent System**: A team of specialized AI agents for different banking tasks.
- **Fraud Triage**: A hybrid system combining a rule engine and anomaly detection to flag suspicious transactions in real-time.
- **Credit Risk Assessment**: A scorecard-based agent for making consistent and explainable credit decisions.
- **RAG for Compliance**: A Retrieval-Augmented Generation system to ensure agents can ground their decisions in the latest policy documents.
- **Modern Tech Stack**: Built with FastAPI for a high-performance API, and a React dashboard for a user-friendly interface.
- **Local-first**: Run via Python venv and Node.js; no Docker required.

## 🏗️ High-Level Architecture

The system is composed of a React frontend, a FastAPI backend, and a core set of AI agents that handle the main business logic.

<div align="center">
  <img src="https://mermaid.ink/svg/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBzdWJncmFwaCBcIlVzZXIgSW50ZXJmYWNlXCJcbiAgICAgICAgQVtcIm_Cfm4gUmVhY3QgVUlwiXVxuICAgIGVuZFxuXG4gICAgc3ViZ3JhcGggXCJCYWNrZW5kIEFQSVwiXG4gICAgICAgIEJbXCLwn6etIEZhc3RBUEkgU2VydmVyXCJdXG4gICAgZW5kXG5cbiAgICBzdWJncmFwaCBcIkNvcmUgQWdlbnQgTG9naWNcIlxuICAgICAgICBDW1wvwn5Ss4oCIiBGcmF1ZCBUcmlhZ2UgQWdlbnRcIl1cbiAgICAgICAgRFtcIuKYkiBDcmVkaXQgUmlzayBBZ2VudFwiXVxuICAgIGVuZFxuXG4gICAgc3ViZynJhbSBcIkRhdGEgJiBTdXBwb3J0aW5nIE1vZGVsc1wiXG4gICAgICAgIEZbXCLwn5KcIFBvbGljeSBEb2N1bWVudHMgPGJyPiAoQU1MLCBLWUMsIENyZWRpdClcIl1cbiAgICAgICAgRltcIu-foCBEYXRhYmFzZSA8YnI-IChNb25nb0RCPVwiXVxuICAgICAgICBHltcIu-kkyBNYWNoaW5lIExlYXJuaW5nIE1vZGVsc1wiXVxuICAgIGVuZFxuXG4gICAgQSAtLSBcIkFQSSBDYWxscyAoSFRUUCFcIiAtLT4gQlxuICAgIEIgLS0gIFwiUm91dGVzIHRvXCIgLS0-IENcbiAgICBCIC0tICBcIlJvdXRlcyB0b1wiIC0tPiBEXG4gICAgQyAtLSAgXCJVc2VzXCIgLS0-IEfXG4gICAgRCAtLSAgXCJDb25zdWx0c1wiIC0tPiBFXG4gICAgQyAtLSAgXCJMb2dzIHRvXCIgLS0-IEZcbiAgICBEIC0tICBcIkxvZ3MgdG9cIiAtLT4gRlxuICAgIFxuICAgIHN0eWxlIEEgZmlsbDojNjFEYXFiLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHhcbiAgICBzdHlsZSBCLGZpbGw6IzAwNjhDOSxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4XG4gICAgc3R5bGUgQyBmaWxsOiMyRThCNUMsc3Ryb2tlOiMzMzMsc3Ryb2tlLXdpZHRoOjJweFxuICAgIHN0eWxlIEQgZmlsbDojMkU4QjVDLHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHhcbiAgICBzdHlsZSBFIGZpbGw6I0ZGRDcwMCxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4XG4gICAgc3R5bGUgRiBmaWxsOiNEQTcwREQsc3Ryb2tlOiMzMzMsc3Ryb2tlLXdpZHRoOjJweFxuICAgIHN0eWxlIEcgZmlsbDojRkY2MzQ3LHN0cm9rZTojMzMzLHN0cm9rZS13aWR0aDoycHhcbiIsIm1lcm1haWQiOnt9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9" alt="High-Level Architecture Diagram">
</div>

## 🛠️ Tech Stack

- **Backend**: FastAPI, Pydantic, Uvicorn
- **Frontend**: React, TypeScript, Vite, TailwindCSS
- **AI & Orchestration**: LangChain, LangGraph, OpenAI
- **Data & ML**: Pandas, Scikit-learn, ChromaDB (for RAG)
- **Infrastructure**: Local Python (venv) & Node.js environment
 
## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python (3.10+)
- Node.js (v18+) & npm
- Git
- Windows PowerShell or Command Prompt

### 1. Clone the Repository

Clone the project's source code to your local machine:
```bash
git clone <repository_url>
cd Intelligent_Banking_Operations_Agent
```
*(Note: Replace `<repository_url>` with the actual URL of the project's Git repository.)*

### 2. Set Up Environment Variables

Create a `.env` file inside the root `Intelligent_Banking_Operations_Agent/` directory with the following content:

```env
# OpenAI API Key for Large Language Models
OPENAI_API_KEY="your_openai_api_key_here"

# LangSmith is used for tracing and debugging the agents (optional but helpful)
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
LANGCHAIN_PROJECT="Intelligent Banking Ops"
```

Create another `.env` file inside `Intelligent_Banking_Operations_Agent/frontend/` with the following:
```env
VITE_API_BASE=http://127.0.0.1:8000/api/v1
VITE_USE_MOCKS=false
```

### 3. Backend (Python)

Run with a Python virtual environment (Windows PowerShell):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the backend (FastAPI):

```powershell
cd Intelligent_Banking_Operations_Agent
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Frontend (React)

In a new terminal, navigate to the frontend directory and install dependencies:
```powershell
cd Intelligent_Banking_Operations_Agent/frontend
npm install
```

Start the frontend development server:
```powershell
npm run dev
```

### 5. See It in Action!

Once both processes are running, you can access them in your browser:

- **React Dashboard**: [http://localhost:5173](http://localhost:5173)
- **FastAPI Backend Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

You can now use the dashboard to interact with the fraud and credit triage agents.

## 🔭 Future Directions

This project is a foundation. The immediate roadmap includes:
1.  **Full `BankingSupervisor` Integration**: Transition to a single API endpoint that uses the supervisor and LangGraph to route tasks to the correct agent.
2.  **Activate `ComplianceRAGAgent`**: Fully integrate the RAG agent so that all agent rationales are grounded in and cite specific policy documents.
3.  **Enhance Agent Tools**: Add database connectivity and third-party API tools to allow agents to work with real-world, dynamic data.

For more details, please see the full guide in `BOOK.md`.