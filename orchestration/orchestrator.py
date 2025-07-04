class AgentOrchestrator:
    def __init__(self, agents: list):
        self.agents = agents

    def run(self, input_data: dict) -> dict:
        results = {}
        for agent in self.agents:
            result = agent.evaluate(input_data)
            results[agent.name] = result
        return results
