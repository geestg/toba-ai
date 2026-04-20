import React from "react";

export default function SimulationView({ simulation }) {
  if (!simulation) return null;

  const { before, after, best_location } = simulation;

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Tourism Simulation</h2>

      <div style={styles.section}>
        <h3 style={styles.subtitle}>Before Distribution</h3>
        {Object.entries(before).map(([location, value]) => (
          <div key={location} style={styles.row}>
            <span>{location}</span>
            <span>{value} visitors</span>
          </div>
        ))}
      </div>

      <div style={styles.section}>
        <h3 style={styles.subtitle}>After Optimization</h3>
        {Object.entries(after).map(([location, value]) => (
          <div
            key={location}
            style={{
              ...styles.row,
              ...(location === best_location ? styles.highlight : {})
            }}
          >
            <span>{location}</span>
            <span>{value} visitors</span>
          </div>
        ))}
      </div>

      <div style={styles.result}>
        <strong>Optimized Location:</strong> {best_location}
      </div>
    </div>
  );
}

const styles = {
  container: {
    marginTop: "20px",
    padding: "20px",
    border: "1px solid #444",
    borderRadius: "10px"
  },
  title: {
    marginBottom: "15px"
  },
  subtitle: {
    marginBottom: "10px"
  },
  section: {
    marginBottom: "15px"
  },
  row: {
    display: "flex",
    justifyContent: "space-between",
    padding: "5px 0"
  },
  highlight: {
    backgroundColor: "#1e293b",
    borderRadius: "5px",
    padding: "5px"
  },
  result: {
    marginTop: "10px",
    fontSize: "16px"
  }
};