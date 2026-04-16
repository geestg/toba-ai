# backend/services/chat_engine.py

import os
from dotenv import load_dotenv
from openai import OpenAI

from core.planner import TaskPlanner
from core.orchestrator import AgentOrchestrator
from simulation.dummy_data import get_dummy_data

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

planner = TaskPlanner()
orchestrator = AgentOrchestrator()


def call_llm(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Toba AI, an autonomous tourism assistant. "
                    "Extract user intent including destination, budget, duration, and preferences."
                ),
            },
            {"role": "user", "content": user_input},
        ],
    )

    return response.choices[0].message.content


def process_user_query(user_input):
    #  1. LLM parsing (biar gak rule-based lagi)
    parsed = call_llm(user_input)

    #  2. Planning
    plan = planner.create_plan(parsed)

    #  3. Data
    data = get_dummy_data()

    #  4. Execute agents
    execution = orchestrator.execute(plan, data)

    return {
        "goal": user_input,
        "parsed_intent": parsed,
        "plan": plan,
        "execution": execution,
    }