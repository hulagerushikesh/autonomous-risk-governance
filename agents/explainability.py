from agents.base import BaseAgent

class ExplainabilityAgent(BaseAgent):
    def evaluate(self, input_data: dict) -> dict:
        features = input_data.get("features", [])
        explanation = f"Model used {features} to derive risk score."
        return {"explanation": explanation}

    def report(self) -> dict:
        return {"agent": self.name, "status": "Explainability generated"}
