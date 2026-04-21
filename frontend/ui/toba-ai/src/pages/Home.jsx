import { useState } from "react";
import Navbar from "../components/Navbar";
import DestinationCarousel from "../components/DestinationCarousel";
import ChatBox from "../components/ChatBox";
import RouteMap from "../components/RouteMap";
import ImpactChart from "../components/ImpactChart";

export default function Home() {
  const [response, setResponse] = useState(null);

  return (
    <div className="main">
      <Navbar />

      <DestinationCarousel />

      <ChatBox setResponse={setResponse} />

      {response && (
        <>
          <div className="card">
            <div className="card-content">
              <h3>{response.reply}</h3>

              {response.data?.chosen && (
                <p>
                  Dipilih karena:
                  <br />
                  - Crowd lebih rendah
                  <br />
                  - Cuaca mendukung
                  <br />
                  - Akses lebih mudah
                </p>
              )}
            </div>
          </div>

          <RouteMap route={response.data?.route} />

          <ImpactChart />
        </>
      )}
    </div>
  );
}