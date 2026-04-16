import { useState } from "react";
import { sendChat, fetchSimulation } from "./api/api";

import Header from "./components/Header";
import ChatBox from "./components/ChatBox";
import SystemFlow from "./components/SystemFlow";
import AgentPanel from "./components/AgentPanel";
import ImpactChart from "./components/ImpactChart";
import Loader from "./components/Loader";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [flowStep, setFlowStep] = useState(0);
  const [result, setResult] = useState(null);
  const [impact, setImpact] = useState(null);

  const handleChat = async (message) => {
    setLoading(true);
    setResult(null);

    // fake thinking flow
    for (let i = 1; i <= 4; i++) {
      setFlowStep(i);
      await new Promise((r) => setTimeout(r, 400));
    }

    const res = await sendChat(message);
    setResult(res);

    const sim = await fetchSimulation();
    setImpact(sim);

    setLoading(false);
  };

  return (
    <div className="container">
      <Header />

      <ChatBox onSend={handleChat} />

      {loading && <Loader />}

      <SystemFlow step={flowStep} />

      {result && (
        <>
          <AgentPanel data={result.execution} />
        </>
      )}

      {impact && <ImpactChart data={impact} />}
    </div>
  );
}