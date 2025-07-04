from agents.base import BaseAgent


class ComplianceAgent(BaseAgent):
    def evaluate(self, input_data: dict) -> dict:
        # Example: Check if risk score exceeds threshold
        risk_score = input_data.get("risk_score", 0)
        compliant = risk_score < 0.7
        return {"compliant": compliant, "risk_score": risk_score}

    def report(self) -> dict:
        return {"agent": self.name, "status": "Compliance check complete"}
