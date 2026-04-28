"""Test script to verify backend modules import correctly after dummy data removal."""

import sys
import os

# Ensure backend is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== Testing Backend Imports ===")

# 1. Location service (should handle empty locations.json gracefully)
try:
    from backend.services.location_service import get_locations, get_location_by_name
    locs = get_locations(use_osm=False)
    print(f"✅ get_locations() static only: {len(locs)} locations (expected 0)")
except Exception as e:
    print(f"❌ location_service error: {e}")

# 2. UMKM agent (refactored to OSM)
try:
    from backend.agents.umkm_agent import find_nearby_umkm, get_umkm_insight
    print("✅ umkm_agent imported successfully")
except Exception as e:
    print(f"❌ umkm_agent error: {e}")

# 3. Booking agent (refactored to OSM)
try:
    from backend.agents.booking_agent import find_nearby_hotels, simulate_booking
    print("✅ booking_agent imported successfully")
except Exception as e:
    print(f"❌ booking_agent error: {e}")

# 4. Route service (no more dummy coords)
try:
    from backend.services.route_service import calculate_route
    print("✅ route_service imported successfully")
except Exception as e:
    print(f"❌ route_service error: {e}")

# 5. Recommendation agent (should work with empty static + OSM fallback)
try:
    from backend.agents.recommendation_agent import get_recommendation
    print("✅ recommendation_agent imported successfully")
except Exception as e:
    print(f"❌ recommendation_agent error: {e}")

# 6. Orchestrator (depends on all above)
try:
    from backend.core.orchestrator import handle_chat
    print("✅ orchestrator imported successfully")
except Exception as e:
    print(f"❌ orchestrator error: {e}")

# 7. App (FastAPI)
try:
    from backend.app import app
    print("✅ app imported successfully")
except Exception as e:
    print(f"❌ app error: {e}")

print("\n=== All imports tested ===")

