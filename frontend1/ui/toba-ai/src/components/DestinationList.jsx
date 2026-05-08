import { useState } from "react";

export default function DestinationList({ data, onSelectDestination }) {
  if (!data?.destinations || data.destinations.length === 0) return null;

  const destinations = data.destinations;

  const sectionStyle = {
    padding: "20px 0",
  };

  const headerStyle = {
    marginBottom: "20px",
    textAlign: "center",
  };

  const titleStyle = {
    fontSize: "1.4rem",
    fontWeight: "700",
    color: "#1a202c",
    marginBottom: "6px",
  };

  const subtitleStyle = {
    fontSize: "0.9rem",
    color: "#718096",
  };

  const gridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
    gap: "20px",
  };

  const cardStyle = {
    background: "#fff",
    borderRadius: "16px",
    overflow: "hidden",
    boxShadow: "0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)",
    transition: "transform 0.2s ease, box-shadow 0.2s ease",
    display: "flex",
    flexDirection: "column",
    cursor: "default",
  };

  const cardHoverStyle = {
    transform: "translateY(-4px)",
    boxShadow: "0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)",
  };

  const imageWrapStyle = {
    position: "relative",
    width: "100%",
    height: "180px",
    overflow: "hidden",
    background: "#e2e8f0",
  };

  const imgStyle = {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    display: "block",
  };

  const overlayStyle = {
    position: "absolute",
    inset: "0",
    background: "linear-gradient(to top, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.1) 50%, rgba(0,0,0,0) 100%)",
    pointerEvents: "none",
  };

  const rankBadgeStyle = {
    position: "absolute",
    top: "12px",
    left: "12px",
    background: "#fff",
    color: "#1a202c",
    fontWeight: "700",
    fontSize: "0.85rem",
    width: "32px",
    height: "32px",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 2px 4px rgba(0,0,0,0.15)",
    zIndex: 2,
  };

  const ratingBadgeStyle = {
    position: "absolute",
    top: "12px",
    right: "12px",
    background: "rgba(255,255,255,0.95)",
    color: "#1a202c",
    fontWeight: "600",
    fontSize: "0.8rem",
    padding: "4px 10px",
    borderRadius: "20px",
    display: "flex",
    alignItems: "center",
    gap: "4px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    zIndex: 2,
  };

  const scoreBadgeStyle = {
    position: "absolute",
    bottom: "12px",
    right: "12px",
    background: "#48bb78",
    color: "#fff",
    fontWeight: "700",
    fontSize: "0.75rem",
    padding: "4px 10px",
    borderRadius: "20px",
    display: "flex",
    alignItems: "center",
    gap: "4px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.15)",
    zIndex: 2,
  };

  const contentStyle = {
    padding: "16px",
    display: "flex",
    flexDirection: "column",
    flex: 1,
    gap: "10px",
  };

  const headerRowStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: "8px",
  };

  const nameStyle = {
    fontSize: "1.1rem",
    fontWeight: "700",
    color: "#1a202c",
    margin: 0,
    lineHeight: 1.3,
  };

  const typeStyle = {
    fontSize: "0.7rem",
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    color: "#4a5568",
    background: "#edf2f7",
    padding: "3px 8px",
    borderRadius: "6px",
    whiteSpace: "nowrap",
    flexShrink: 0,
  };

  const reasonStyle = {
    fontSize: "0.85rem",
    color: "#4a5568",
    lineHeight: 1.5,
    margin: 0,
  };

  const metaStyle = {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
    marginTop: "4px",
  };

  const metaItemStyle = {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontSize: "0.8rem",
    color: "#4a5568",
  };

  const tagsStyle = {
    display: "flex",
    flexWrap: "wrap",
    gap: "6px",
    marginTop: "2px",
  };

  const tagStyle = {
    fontSize: "0.7rem",
    fontWeight: "500",
    color: "#2b6cb0",
    background: "#ebf8ff",
    padding: "3px 8px",
    borderRadius: "12px",
  };

  const buttonStyle = {
    marginTop: "auto",
    padding: "10px 16px",
    borderRadius: "10px",
    border: "none",
    background: "#3182ce",
    color: "#fff",
    fontWeight: "600",
    fontSize: "0.9rem",
    cursor: "pointer",
    transition: "background 0.2s ease",
    textAlign: "center",
  };

  const buttonHoverStyle = {
    background: "#2b6cb0",
  };

  return (
    <section style={sectionStyle}>
      <div style={headerStyle}>
        <h2 style={titleStyle}>🎯 Hasil Rekomendasi</h2>
        <p style={subtitleStyle}>Top {destinations.length} destinasi berdasarkan cuaca, jarak, rating, dan keramaian</p>
      </div>

      <div style={gridStyle}>
        {destinations.map((d, i) => {
          const [hovered, setHovered] = useState(false);
          const [btnHovered, setBtnHovered] = useState(false);

          return (
            <div
              key={i}
              style={{
                ...cardStyle,
                ...(hovered ? cardHoverStyle : {}),
                animationDelay: `${i * 0.06}s`,
              }}
              onMouseEnter={() => setHovered(true)}
              onMouseLeave={() => setHovered(false)}
            >
              <div style={imageWrapStyle}>
                <img
                  src={d.image || `/images/${d.name.toLowerCase().replace(/\s+/g, "").replace(/[^a-z0-9]/g, "")}.jpg`}
                  alt={d.name}
                  loading="lazy"
                  style={imgStyle}
                  onError={(e) => { e.target.src = "/images/toba.jpg"; }}
                />
                <div style={overlayStyle} />
                <div style={rankBadgeStyle}>{i + 1}</div>
                <div style={ratingBadgeStyle}>
                  <span>⭐</span>
                  <span>{d.rating}</span>
                </div>
                <div style={scoreBadgeStyle}>
                  <span>🏆</span>
                  <span>{(d.score * 100).toFixed(0)}%</span>
                </div>
              </div>

              <div style={contentStyle}>
                <div style={headerRowStyle}>
                  <h3 style={nameStyle}>{d.name}</h3>
                  <span style={typeStyle}>{d.type}</span>
                </div>

                <p style={reasonStyle}>{d.reason}</p>

                <div style={metaStyle}>
                  <div style={metaItemStyle}>
                    <span>🌤️</span>
                    <span>{d.weather_note}</span>
                  </div>
                  <div style={metaItemStyle}>
                    <span>👥</span>
                    <span>{d.crowd_note}</span>
                  </div>
                  {d.area && (
                    <div style={metaItemStyle}>
                      <span>📍</span>
                      <span>{d.area}</span>
                    </div>
                  )}
                </div>

                {d.tags && d.tags.length > 0 && (
                  <div style={tagsStyle}>
                    {d.tags.slice(0, 4).map((tag, idx) => (
                      <span key={idx} style={tagStyle}>{tag}</span>
                    ))}
                  </div>
                )}

                <button
                  style={{
                    ...buttonStyle,
                    ...(btnHovered ? buttonHoverStyle : {}),
                  }}
                  onMouseEnter={() => setBtnHovered(true)}
                  onMouseLeave={() => setBtnHovered(false)}
                  onClick={() => onSelectDestination && onSelectDestination(d)}
                >
                  Pilih Destinasi
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

