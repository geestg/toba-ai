"""Quick test to verify OSM data sources still work after removing static dummy data."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.services.location_service import get_locations
from backend.services.osm_service import fetch_osm_locations, _osm_cache

# Clear any cache
_osm_cache.clear()

print("=== Testing OSM data source (static data now empty) ===")

# With OSM enabled and static empty, should return OSM data only
all_locs = get_locations(use_osm=True)
print(f"Total locations with OSM: {len(all_locs)}")

if all_locs:
    sources = {}
    for l in all_locs:
        s = l.get("source", "unknown")
        sources[s] = sources.get(s, 0) + 1
    print(f"Sources breakdown: {sources}")
    print(f"\nFirst 5 locations:")
    for loc in all_locs[:5]:
        print(f"  - {loc['name']} ({loc.get('type','?')}, {loc.get('area','?')}, rating={loc.get('rating','?')})")
else:
    print("WARNING: No locations returned!")

print("\n=== OSM-only test ===")
osm_only = fetch_osm_locations(use_cache=False)
print(f"Pure OSM fetch: {len(osm_only)} locations")
if osm_only:
    print(f"First 3: {[l['name'] for l in osm_only[:3]]}")

