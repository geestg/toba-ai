export default function DecisionCard({ data }) {
  const d = data.decision.final_decision;

  return (
    <div className="decision">
      <h2>Rekomendasi Utama</h2>

      <h3>{d.name}</h3>
      <p>{d.description}</p>

      <hr />

      <p><b>Alasan Sistem:</b></p>
      <p>{data.decision.reason}</p>

      <p>{data.decision.explanation}</p>
    </div>
  );
}