from backend.core.llm_client import call_llm

USE_LLM = True

def make_decision(intent, plan, environment, routing, cost, weather, umkm):

    # fallback dulu (biar stabil)
    best_location = sorted(environment, key=lambda x: x["crowd"])[0]

    if not USE_LLM:
        return {
            "final_decision": best_location,
            "reason": "Lowest crowd for sustainability",
            "explanation": "System selected destination with lowest crowd density"
        }

    prompt = f"""
You are Toba AI Decision Engine.

User Intent:
{intent}

Tourism Plan:
{plan}

Environment Data:
{environment}

Weather:
{weather}

Cost:
{cost}

UMKM Impact:
{umkm}

TASK:
Select ONE best destination.

You MUST:
1. Optimize for low crowd (sustainability)
2. Maintain good experience
3. Support local economy (UMKM)
4. Consider weather

OUTPUT STRICT JSON:

{{
  "final_decision": {{
    "name": "...",
    "reason": "...",
    "experience_score": 0-100,
    "sustainability_score": 0-100
  }},
  "impact": {{
    "environment": "...",
    "economic": "..."
  }},
  "explanation": "Explain WHY this decision is optimal in a smart, analytical way"
}}
"""

    res = call_llm(prompt)
    content = res["choices"][0]["message"]["content"]

    return content