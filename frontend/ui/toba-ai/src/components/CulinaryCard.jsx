export default function CulinaryCard({ data, insight }) {
  const typeLabel = (type) => {
    const labels = {
      restaurant: "Restoran",
      cafe: "Kafe",
      fast_food: "Fast Food",
      market: "Market",
      shop: "Toko",
    };
    return labels[type] || type;
  };

  const typeColor = (type) => {
    const colors = {
      restaurant: "#e7f8f5",
      cafe: "#fff2e7",
      fast_food: "#ffe7e7",
      market: "#ecf4ff",
      shop: "#f1eaff",
    };
    return colors[type] || "#f0f4f8";
  };

  const typeTextColor = (type) => {
    const colors = {
      restaurant: "#2fb3bd",
      cafe: "#f29b39",
      fast_food: "#e74c3c",
      market: "#2f8dea",
      shop: "#8c5ae6",
    };
    return colors[type] || "#607084";
  };

  return (
    <div className="culinary-card animate-fade-in-up">
      <div className="culinary-header">
        <span className="culinary-icon">🍽️</span>
        <div>
          <h3 className="culinary-title">Rekomendasi Kuliner</h3>
          <p className="culinary-subtitle">{data.count || data.umkm_list?.length || 0} tempat di sekitar destinasi</p>
        </div>
      </div>

      <div className="culinary-list">
        {(data.umkm_list || []).slice(0, 5).map((place, i) => (
          <div key={i} className="culinary-item">
            <div className="culinary-item-main">
              <div className="culinary-item-info">
                <span
                  className="culinary-badge"
                  style={{
                    background: typeColor(place.type),
                    color: typeTextColor(place.type),
                  }}
                >
                  {typeLabel(place.type)}
                </span>
                <h4 className="culinary-name">{place.name}</h4>
              </div>
              <div className="culinary-meta">
                <span className="culinary-rating">⭐ {place.rating}</span>
                <span className="culinary-distance">📍 {place.distance_km} km</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {insight?.suggestion && (
        <div className="culinary-footer">
          <span className="culinary-tip-icon">💡</span>
          <p className="culinary-tip">{insight.suggestion}</p>
        </div>
      )}
    </div>
  );
}

