from agents.base import BaseAgent


class ExplainabilityAgent(BaseAgent):
    def evaluate(self, input_data: dict) -> dict:
        explanation = f"Model used {input_data.get('features', [])} to derive risk score."
        return {"explanation": explanation}

    def report(self) -> dict:
        return {"agent": self.name, "status": "Explainability generated"}
