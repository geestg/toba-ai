"""Test script untuk Smart Route Agent."""
import sys
sys.path.insert(0, "c:/Users/THINKPAD/Documents/GitHub/toba-ai")

from backend.services.route_service import calculate_smart_route
from backend.agents.route_agent import get_route_explanation

# Test 1: Smart route to Museum Huta Bolon Simanindo
print("=" * 60)
print("TEST 1: Smart Route ke Museum Huta Bolon Simanindo")
print("=" * 60)

result = calculate_smart_route(2.684, 98.715, "Museum Huta Bolon Simanindo")

if result.get("error"):
    print("ERROR:", result["error"])
else:
    print(f"Start: {result['start']}")
    print(f"End: {result['end']}")
    print(f"Route count: {result['route_count']}")
    print()

    # Best route
    best = result.get("best", {})
    print(f"🥇 BEST ROUTE:")
    print(f"   Labels: {best.get('labels', [])}")
    print(f"   Score: {best.get('score')}")
    print(f"   Distance: {best.get('distance_km')} km")
    print(f"   Duration: {best.get('duration_min')} menit")
    print(f"   Path points: {len(best.get('path', []))}")
    print()

    # Explanation
    explanation = get_route_explanation(result)
    print("EXPLANATION:")
    print(explanation)
    print()

    # Alternatives
    alternatives = result.get("alternatives", [])
    if len(alternatives) > 1:
        print("ALTERNATIVES:")
        for i, alt in enumerate(alternatives[1:], 2):
            print(f"   {i}. {alt.get('distance_km')} km, {alt.get('duration_min')} menit, "
                  f"score={alt.get('score')}, labels={alt.get('labels', [])}")
    print()

# Test 2: Smart route to Patung Yesus
print("=" * 60)
print("TEST 2: Smart Route ke Patung Yesus, Bukit Sibea-bea")
print("=" * 60)

result2 = calculate_smart_route(2.684, 98.715, "Patung Yesus, Bukit Sibea-bea")

if result2.get("error"):
    print("ERROR:", result2["error"])
else:
    best2 = result2.get("best", {})
    print(f"🥇 BEST ROUTE:")
    print(f"   Labels: {best2.get('labels', [])}")
    print(f"   Score: {best2.get('score')}")
    print(f"   Distance: {best2.get('distance_km')} km")
    print(f"   Duration: {best2.get('duration_min')} menit")
    print()
    print("EXPLANATION:")
    print(get_route_explanation(result2))

print()
print("=" * 60)
print("All tests completed!")
print("=" * 60)

