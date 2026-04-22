import { destinations } from "../data/destinations";

export default function DestinationCarousel() {
  return (
    <div>
      <h2>Destinasi Wisata</h2>

      <div className="grid">
        {destinations.map((d, i) => (
          <div key={i} className="card">
            <div className="image-wrap">
              <img src={d.image} />
            </div>

            <div className="card-content">
              <h3>{d.name}</h3>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}