from fastapi import FastAPI, Request

from agents.bias_audit import BiasAuditingAgent
from agents.compliance import ComplianceAgent
from agents.decision_support import DecisionSupportAgent
from agents.explainability import ExplainabilityAgent
from orchestration.orchestrator import AgentOrchestrator

app = FastAPI()
orchestrator = AgentOrchestrator([
    ComplianceAgent("Compliance"),
    BiasAuditingAgent("BiasAudit"),
    DecisionSupportAgent("DecisionSupport"),
    ExplainabilityAgent("Explainability")
])

@app.post("/evaluate")
async def evaluate(request: Request):
    input_data = await request.json()
    results = orchestrator.run(input_data)
    return results
