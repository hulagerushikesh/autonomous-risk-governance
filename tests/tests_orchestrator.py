import pytest
from agents.compliance import ComplianceAgent
from agents.bias_audit import BiasAuditingAgent
from agents.decision_support import DecisionSupportAgent
from agents.explainability import ExplainabilityAgent
from orchestration.orchestrator import AgentOrchestrator

@pytest.fixture
def sample_input():
    return {
        "risk_score": 0.65,
        "bias_score": 0.25,
        "risk_level": 1,
        "features": ["income", "age", "credit_score"]
    }

def test_orchestrator_runs_all_agents(sample_input):
    agents = [
        ComplianceAgent("ComplianceAgent"),
        BiasAuditingAgent("BiasAuditingAgent"),
        DecisionSupportAgent("DecisionSupportAgent"),
        ExplainabilityAgent("ExplainabilityAgent")
    ]
    orchestrator = AgentOrchestrator(agents)
    results = orchestrator.run(sample_input)

    assert isinstance(results, dict)
    assert set(results.keys()) == {"ComplianceAgent", "BiasAuditingAgent", "DecisionSupportAgent", "ExplainabilityAgent"}
    assert "compliant" in results["ComplianceAgent"]
    assert "bias_flagged" in results["BiasAuditingAgent"]
    assert "decision" in results["DecisionSupportAgent"]
    assert "explanation" in results["ExplainabilityAgent"]
