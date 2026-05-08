import "../styles/components/culinary-card.css";

export default function HotelCard({ hotels = [] }) {
  if (!hotels.length) return null;

  return (
    <section className="culinary-section">
      <div className="section-header">
        <h2>Rekomendasi Penginapan</h2>
        <p>
          Penginapan terbaik di sekitar destinasi pilihan Anda
        </p>
      </div>

      <div className="culinary-grid">
        {hotels.map((hotel, index) => (
          <div className="culinary-card" key={index}>
            <div className="culinary-image-wrapper">
              <img
                src={hotel.image}
                alt={hotel.name}
                className="culinary-image"
              />

              <div className="culinary-rating">
                ⭐ {hotel.rating}
              </div>
            </div>

            <div className="culinary-content">
              <div className="culinary-top">
                <h3>{hotel.name}</h3>

                <span className="culinary-type">
                  {hotel.type}
                </span>
              </div>

              <p className="culinary-description">
                {hotel.description}
              </p>

              <div className="culinary-meta">
                <span>📍 {hotel.location}</span>
                <span>💰 {hotel.price}</span>
              </div>

              <button className="culinary-button">
                Lihat Penginapan
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}