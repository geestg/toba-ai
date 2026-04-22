export default function RouteMap({ data }) {
  if (!data?.route) return null;

  return (
    <div className="route-box">
      <h3> Rute Perjalanan</h3>
      <p>Jarak: {(data.route.distance / 1000).toFixed(1)} km</p>
      <p>Durasi: {(data.route.duration / 60).toFixed(0)} menit</p>
    </div>
  );
}