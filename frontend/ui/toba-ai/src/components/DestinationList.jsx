export default function DestinationList({ data }) {
  if (!data?.destinations) return null;

  return (
    <div className="dest-grid">
      {data.destinations.map((d, i) => (
        <div key={i} className="dest-card">
          <img src={d.image} alt={d.name} />
          <div className="overlay" />
          <div className="content">
            <h3>{d.name}</h3>
            <span>⭐ {d.rating}</span>
          </div>
        </div>
      ))}
    </div>
  );
}