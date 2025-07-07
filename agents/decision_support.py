from agents.base import BaseAgent


class DecisionSupportAgent(BaseAgent):
    def evaluate(self, input_data: dict) -> dict:
        recommendations = ["Approve", "Review", "Reject"]
        risk_level = input_data.get("risk_level", 1)
        decision = recommendations[min(risk_level, len(recommendations) - 1)]
        return {"decision": decision}

    def report(self) -> dict:
        return {"agent": self.name, "status": "Decision support complete"}
