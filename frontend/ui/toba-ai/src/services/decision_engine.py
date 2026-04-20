from backend.core.llm_client import call_llm

USE_LLM = False

def make_decision(plan, environment, routing, cost, weather, umkm):

    if not USE_LLM:
        # rule-based fallback
        best = sorted(environment, key=lambda x: x["crowd"])[0]

        return {
            "final_decision": best,
            "reason": "Lowest crowd for sustainability"
        }

    prompt = f"""
User wants optimal tourism plan.

Data:
{plan}
{environment}
{weather}
{cost}

Choose BEST destination.
Return JSON with:
- name
- reason
"""

    res = call_llm(prompt)

    content = res["choices"][0]["message"]["content"]

    return {
        "final_decision": content
    }