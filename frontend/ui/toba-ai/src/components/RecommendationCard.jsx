export default function RecommendationCard({
  destinations = [],
}) {

  if (!destinations.length) {
    return null;
  }

  function crowdLabel(level) {

    if (level === "low") {
      return "Sepi";
    }

    if (level === "medium") {
      return "Normal";
    }

    return "Ramai";
  }

  function weatherLabel(weather) {

    const mapping = {
      clear: "Cerah",
      sunny: "Panas",
      cloudy: "Berawan",
      foggy: "Berkabut",
      rainy: "Hujan",
    };

    return mapping[weather] || "Normal";
  }

  return (
    <div className="recommendation-grid">

      {destinations.map((item) => (

        <div
          key={item.id}
          className="recommendation-card animate-fade-up"
        >

          {/* ===================== */}
          {/* IMAGE */}
          {/* ===================== */}

          <div className="recommendation-image-wrap">

            <img
              src={item.image}
              alt={item.name}
              className="recommendation-image"
            />

            <div className="recommendation-overlay" />

            {/* SCORE */}

            <div className="recommendation-score">
              {Math.round(item.score || 0)}
            </div>

          </div>

          {/* ===================== */}
          {/* CONTENT */}
          {/* ===================== */}

          <div className="recommendation-content">

            <div className="recommendation-top">

              <div>

                <h2 className="recommendation-title">
                  {item.name}
                </h2>

                <p className="recommendation-area">
                  {item.area}
                </p>

              </div>

              <div className="recommendation-rating">
                ★ {item.rating}
              </div>

            </div>

            <p className="recommendation-desc">
              {item.description}
            </p>

            {/* ===================== */}
            {/* CHIPS */}
            {/* ===================== */}

            <div className="recommendation-meta">

              <div className="recommendation-chip">
                {weatherLabel(item.weather)}
              </div>

              <div className="recommendation-chip">
                {crowdLabel(item.crowd)}
              </div>

              <div className="recommendation-chip">
                {item.distance} km
              </div>

            </div>

            {/* ===================== */}
            {/* TAGS */}
            {/* ===================== */}

            <div className="recommendation-tags">

              {item.tags?.slice(0, 4).map((tag) => (

                <span
                  key={tag}
                  className="recommendation-tag"
                >
                  #{tag}
                </span>

              ))}

            </div>

          </div>

        </div>
      ))}
    </div>
  );
}