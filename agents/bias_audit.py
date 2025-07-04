from agents.base import BaseAgent


class BiasAuditingAgent(BaseAgent):
    def evaluate(self, input_data: dict) -> dict:
        bias_score = input_data.get("bias_score", 0.0)
        flagged = bias_score > 0.3
        return {"bias_flagged": flagged, "bias_score": bias_score}

    def report(self) -> dict:
        return {"agent": self.name, "status": "Bias audit complete"}
