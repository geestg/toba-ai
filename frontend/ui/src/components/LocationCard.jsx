export default function LocationCard({ loc }) {
  return (
    <div className="card">
      <h3>{loc.name}</h3>
      <p>Crowd: {loc.simulated_crowd}</p>
      <p>Status: {loc.status}</p>
    </div>
  );
}