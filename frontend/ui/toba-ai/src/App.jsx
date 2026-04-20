import { useState } from "react";

import ChatWindow from "./components/ChatWindow";
import DecisionCard from "./components/DecisionCard";
import ImpactPanel from "./components/ImpactPanel";
import SimulationView from "./components/SimulationView";
import AgentFlow from "./components/AgentFlow";
import Loader from "./components/Loader";
import ImpactChart from "./components/ImpactChart";
import MapView from "./components/MapView";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="container">
      <h1>Toba AI System</h1>

      <ChatWindow setData={setData} setLoading={setLoading} />

      {loading && <Loader />}

      {data && (
        <>
          <AgentFlow trigger={data} />
          <DecisionCard decision={data.decision} />
          <MapView decision={data.decision} />
          <SimulationView simulation={data.simulation} />
          <ImpactChart simulation={data.simulation} />
          <ImpactPanel impact={data.impact} />
        </>
      )}
    </div>
  );
}

export default App;