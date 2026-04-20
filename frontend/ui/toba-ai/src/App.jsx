import { useState } from "react";

import ChatWindow from "./components/ChatWindow";
import DecisionCard from "./components/DecisionCard";
import ImpactPanel from "./components/ImpactPanel";
import AgentFlow from "./components/AgentFlow";
import Loader from "./components/Loader";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="app">
      <h1>Toba AI Decision System</h1>

      <ChatWindow setData={setData} setLoading={setLoading} />

      {loading && <Loader />}

      {data && (
        <>
          <AgentFlow />
          <DecisionCard data={data} />
          <ImpactPanel impact={data.impact} />
        </>
      )}
    </div>
  );
}

export default App;