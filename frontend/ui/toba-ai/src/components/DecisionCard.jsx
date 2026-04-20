export default function DecisionCard({ data }) {
  const d = data.decision.final_decision;

  return (
    <div className="card">
      <h2>{d.name}</h2>
      <img src={d.image} />

      <p className="desc">{d.description}</p>

      <p><b>Alasan:</b> {data.decision.reason}</p>
      <p><b>AI Reasoning:</b> {data.decision.explanation}</p>

      <h3>Makanan Sekitar</h3>
      <div className="grid">
        {data.supporting.food.map((f, i) => (
          <div key={i} className="mini-card">
            <img src={f.image} />
            <p>{f.name}</p>
          </div>
        ))}
      </div>

      <h3>Penginapan</h3>
      <div className="grid">
        {data.supporting.stay.map((s, i) => (
          <div key={i} className="mini-card">
            <img src={s.image} />
            <p>{s.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}