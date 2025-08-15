# 🚀 ANZ Hackfest 2025 – Autonomous Risk Governance Multi-Agent System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

👨‍💻 Author: **Rushikesh Hulage**

---

## ✅ Step 1: Project Setup & Environment Configuration

### 🎯 Purpose
Establish a clean and modular project structure to support agent-based development and orchestration.

### 🛠️ Actions Taken
- Created a structured folder layout:
  - [`agents/`](agents/): Contains individual agent implementations.
  - [`orchestration/`](orchestration/): Contains orchestration logic.
  - [`api/`](api/): Contains FastAPI application.
  - [`tests/`](tests/): Contains unit tests.
- Initialized Python virtual environment.
- Installed required packages: `fastapi`, `uvicorn`, `pydantic`.

### 🧪 Technologies Used
- Python 3.11
- FastAPI for API layer
- Pydantic for input validation
- Uvicorn for ASGI server

### ✅ Outcome
- A modular and scalable project structure ready for agent development.
- Environment configured for local development and testing.

---

## ✅ Step 2: Designing Agent Interfaces & Orchestration Logic

### 🎯 Purpose
Define how agents interact and how orchestration coordinates their execution.

### 🛠️ Actions Taken
- Created `BaseAgent` abstract class in [`agents/base.py`](agents/base.py) with `evaluate()` and `report()` methods.
- Implemented four agents:
  - [`ComplianceAgent`](agents/compliance.py): Checks risk score compliance.
  - [`BiasAuditingAgent`](agents/bias_audit.py): Flags bias based on bias score.
  - [`DecisionSupportAgent`](agents/decision_support.py): Maps risk level to decision.
  - [`ExplainabilityAgent`](agents/explainability.py): Generates explanation from input features.
- Built `AgentOrchestrator` in [`orchestration/orchestrator.py`](orchestration/orchestrator.py) to run agents sequentially.
- Created FastAPI endpoint `/evaluate` in [`api/main.py`](api/main.py) using Pydantic model `EvaluationRequest`.

### 🧪 Technologies Used
- Python classes and inheritance
- FastAPI for RESTful endpoint
- Pydantic for schema validation

### ✅ Outcome
- Fully functional agent orchestration system.
- API endpoint `/evaluate` accepts structured input and returns agent results.
- Swagger UI enabled for testing and debugging.

---

## 🚀 Next Steps
- Step 3: Integrate LangChain tools and memory for contextual reasoning.
- Add logging, error handling, and unit tests.
- Build frontend or visualization layer.



