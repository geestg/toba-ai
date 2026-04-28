from backend.services.osm_service import fetch_osm_locations

osm_locs = fetch_osm_locations(use_cache=False)

# Find entries that should be cultural but are nature
suspicious = [l for l in osm_locs if l["type"] == "nature" and any(kw in l["name"].lower() for kw in ["museum", "grave", "stone", "chair", "huta", "bolon", "batak", "tomb", "makam", "batu"])]

print("=== SUSPICIOUS 'nature' entries ===")
for loc in suspicious[:15]:
    print(f"Name: {loc['name']}")
    print(f"  Type: {loc['type']}, Rating: {loc['rating']}")
    print(f"  Tags: {loc.get('category_tags', [])}")
    print()

# Show all unique type counts
from collections import Counter
print("=== TYPE DISTRIBUTION ===")
for t, c in Counter(l["type"] for l in osm_locs).most_common():
    print(f"  {t}: {c}")

