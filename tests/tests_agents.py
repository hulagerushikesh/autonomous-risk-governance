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
    assert "agent_metadata" in result
    assert result["agent_metadata"]["name"] == "ComplianceAgent"
    
    # Test enhanced reporting
    report = agent.report()
    assert report["agent"] == "ComplianceAgent"
    assert "execution_count" in report
    assert "error_count" in report



def test_bias_audit_agent(sample_input):
    agent = BiasAuditingAgent("BiasAuditingAgent")
    result = agent.evaluate(sample_input)
    assert result["bias_flagged"] is False
    assert "bias_score" in result
    assert "agent_metadata" in result
    assert result["agent_metadata"]["name"] == "BiasAuditingAgent"
    
    # Test enhanced reporting
    report = agent.report()
    assert report["agent"] == "BiasAuditingAgent"
    assert "execution_count" in report



def test_decision_support_agent(sample_input):
    agent = DecisionSupportAgent("DecisionSupportAgent")
    result = agent.evaluate(sample_input)
    assert result["decision"] == "Review"
    assert "agent_metadata" in result
    assert result["agent_metadata"]["name"] == "DecisionSupportAgent"
    
    # Test enhanced reporting
    report = agent.report()
    assert report["agent"] == "DecisionSupportAgent"
    assert "execution_count" in report

    

def test_explainability_agent(sample_input):
    agent = ExplainabilityAgent("ExplainabilityAgent")
    result = agent.evaluate(sample_input)
    assert "explanation" in result
    assert "detailed_explanation" in result
    assert "feature_importance" in result
    assert "agent_metadata" in result
    assert result["agent_metadata"]["name"] == "ExplainabilityAgent"
    
    # Test enhanced reporting
    report = agent.report()
    assert report["agent"] == "ExplainabilityAgent"
    assert "execution_count" in report
