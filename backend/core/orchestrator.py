# core/orchestrator.py

from agents.tourist_agent import TouristAgent
from agents.policy_agent import PolicyAgent
from agents.umkm_agent import UMKMAgent
from agents.action_agent import ActionAgent

class AgentOrchestrator:
    def __init__(self):
        self.tourist = TouristAgent()
        self.policy = PolicyAgent()
        self.umkm = UMKMAgent()
        self.action = ActionAgent()

    def execute(self, plan, data):
        result = {
            "decisions": [],
            "actions": [],
            "policies": []
        }

        # tourist decision
        result["decisions"] = self.tourist.analyze(data)

        # policy
        result["policies"] = self.policy.analyze(data)

        # UMKM
        result["umkm"] = self.umkm.analyze(data)

        # ACTION (🔥 penting)
        result["actions"] = self.action.execute(plan, data)

        return result