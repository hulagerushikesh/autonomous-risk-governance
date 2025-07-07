# Autonomous Risk Governance Multi-Agent System

This project is developed by Team AlgoRythm for ANZ Hackfest 2025. It introduces a multi-agent system designed to autonomously govern AI-driven decisions in banking.

## 🔍 Project Vision
A multi-agent system that enhances:
- Credit Risk Assessment
- Fraud Detection
- Ethical Compliance

## 🧠 Technical Stack
- Python, FastAPI, LangChain, Streamlit
- SQLite/PostgreSQL
- LIME/SHAP for explainability
- Matplotlib for visualizations

## 🧩 Agent Roles
- Regulatory Compliance Agent
- Decision Support Agent
- Bias & Fairness Auditor
- Secure Access Agent
- Override Agent
- Risk Metrics Agent
- Explainability Agent

## 🏗️ Architecture
- Modular agent layer
- Central orchestration via LangChain
- FastAPI backend
- Streamlit/React frontend

## 🚀 Getting Started
1. Clone the repository
2. Create a virtual environment
3. Install dependencies from `requirements.txt`
4. Run the FastAPI server using `uvicorn api.main:app --reload`

## 📁 Folder Structure
- `agents/` - Agent logic
- `api/` - FastAPI routes
- `frontend/` - Dashboards
- `data/` - Datasets
- `models/` - ML models
- `orchestration/` - LangChain logic
- `utils/` - Helper functions
- `database/` - DB setup
- `tests/` - Unit tests

## 📄 License
MIT License



autonomous-risk-governance/
│
├── agents/                     # All agent logic (e.g., compliance, bias, explainability)
│   ├── __init__.py
│   ├── compliance_agent.py
│   ├── bias_auditor_agent.py
│   ├── explainability_agent.py
│   └── ...
│
├── api/                        # FastAPI routes and services
│   ├── __init__.py
│   ├── main.py
│   └── routes/
│       └── decision_routes.py
│
├── frontend/                   # Streamlit or React frontend
│   └── dashboard.py
│
├── data/                       # Datasets (credit, fraud, etc.)
│   └── sample_credit_data.csv
│
├── models/                     # ML models and explainability tools
│   ├── credit_model.pkl
│   └── explainer.py
│
├── orchestration/             # LangChain or CrewAI logic
│   └── orchestrator.py
│
├── utils/                      # Helper functions
│   └── logger.py
│
├── database/                   # SQLite/PostgreSQL setup
│   └── db_config.py
│
├── tests/                      # Unit and integration tests
│   └── test_agents.py
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
└── .env                        # Environment variables


Whenever open vscode run : Or in cmd
python -m venv venv 
C:\autonomous-risk-governance>venv\Scripts\activate.bat

Welcome to my project 

To run API Server (in cmd) : uvicorn api.main:app --reload
url : http://127.0.0.1:8000/docs



Repo Setup :
Clone it from git --> https://github.com/hulagerushikesh/autonomous-risk-governance.git
Add all the dependencies --> run requirements.txt --> pip install requirements.txt