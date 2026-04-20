import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function ImpactChart({ simulation }) {
  if (!simulation) return null;

  const data = Object.keys(simulation.before).map((loc) => ({
    name: loc,
    before: simulation.before[loc],
    after: simulation.after[loc]
  }));

  return (
    <div className="card">
      <h3>Visitor Distribution</h3>
      <BarChart width={400} height={250} data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="before" />
        <Bar dataKey="after" />
      </BarChart>
    </div>
  );
}