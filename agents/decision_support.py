from agents.base import BaseAgent


class DecisionSupportAgent(BaseAgent):
    def evaluate(self, input_data: dict) -> dict:
        recommendations = ["Approve", "Review", "Reject"]
        decision = recommendations[input_data.get("risk_level", 1)]
        return {"decision": decision}

    def report(self) -> dict:
        return {"agent": self.name, "status": "Decision support complete"}
