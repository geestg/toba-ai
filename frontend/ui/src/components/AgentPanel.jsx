export default function AgentPanel({ data }) {
  if (!data) return null;

  return (
    <div className="agent-panel">
      <h3>Agent Decisions</h3>

      <pre>{JSON.stringify(data.decisions, null, 2)}</pre>

      <h3>Policies</h3>
      <pre>{JSON.stringify(data.policies, null, 2)}</pre>

      <h3>Actions</h3>
      <pre>{JSON.stringify(data.actions, null, 2)}</pre>
    </div>
  );
}