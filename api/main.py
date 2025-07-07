from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.testclient import TestClient

from agents.bias_audit import BiasAuditingAgent
from agents.compliance import ComplianceAgent
from agents.decision_support import DecisionSupportAgent
from agents.explainability import ExplainabilityAgent
from orchestration.orchestrator import AgentOrchestrator

# Define the input schema using Pydantic
class EvaluationRequest(BaseModel):
    risk_score: float
    bias_score: float
    risk_level: int
    features: List[str]

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Autonomous Risk Governance API"}

# Create orchestrator with all agents
orchestrator = AgentOrchestrator([
    ComplianceAgent("Compliance"),
    BiasAuditingAgent("BiasAudit"),
    DecisionSupportAgent("DecisionSupport"),
    ExplainabilityAgent("Explainability")
])

# Define the /evaluate endpoint
@app.post("/evaluate")
async def evaluate(request: EvaluationRequest):
    input_data = request.dict()
    results = orchestrator.run(input_data)
    return results
