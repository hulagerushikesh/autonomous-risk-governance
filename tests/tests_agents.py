import pytest
from agents.compliance import ComplianceAgent
from agents.bias_audit import BiasAuditingAgent
from agents.decision_support import DecisionSupportAgent
from agents.explainability import ExplainabilityAgent



@pytest.fixture
def sample_input():
    return {
        "risk_score": 0.65,
        "bias_score": 0.25,
        "risk_level": 1,
        "features": ["income", "age", "credit_score"]
    }



def test_compliance_agent(sample_input):
    agent = ComplianceAgent("ComplianceAgent")
    result = agent.evaluate(sample_input)
    assert result["compliant"] is True
    assert "risk_score" in result
    assert agent.report() == {"agent": "ComplianceAgent", "status": "Compliance check complete"}



def test_bias_audit_agent(sample_input):
    agent = BiasAuditingAgent("BiasAuditingAgent")
    result = agent.evaluate(sample_input)
    assert result["bias_flagged"] is False
    assert "bias_score" in result
    assert agent.report() == {"agent": "BiasAuditingAgent", "status": "Bias audit complete"}



def test_decision_support_agent(sample_input):
    agent = DecisionSupportAgent("DecisionSupportAgent")
    result = agent.evaluate(sample_input)
    assert result["decision"] == "Review"
    assert agent.report() == {"agent": "DecisionSupportAgent", "status": "Decision support complete"}

    

def test_explainability_agent(sample_input):
    agent = ExplainabilityAgent("ExplainabilityAgent")
    result = agent.evaluate(sample_input)
    assert "explanation" in result
    for feature in sample_input["features"]:
        assert feature in result["explanation"]
    assert agent.report() == {"agent": "ExplainabilityAgent", "status": "Explainability generated"}
