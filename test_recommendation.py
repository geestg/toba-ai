"""Test full recommendation flow end-to-end."""
import asyncio
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.orchestrator import handle_chat

async def test():
    result = await handle_chat("rekomendasi wisata danau toba")
    print("Intent:", result["intent"])
    print("Reply preview:", result["reply"][:300])
    print("Destinations count:", len(result.get("data", {}).get("destinations", [])))
    if result.get("data", {}).get("destinations"):
        for d in result["data"]["destinations"][:5]:
            print("  -", d["name"], "(score=" + str(d["score"]) + ", type=" + d["type"] + ")")
    else:
        print("  WARNING: No destinations returned!")

asyncio.run(test())

