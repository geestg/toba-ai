export default function UMKMPanel({ data }) {
  return (
    <div className="umkm">
      <h2>Peluang UMKM</h2>

      {data.umkm.map((u, i) => (
        <div key={i}>
          <h4>{u.name}</h4>
          {u.opportunities.map((o, j) => (
            <p key={j}>- {o}</p>
          ))}
        </div>
      ))}
    </div>
  );
}