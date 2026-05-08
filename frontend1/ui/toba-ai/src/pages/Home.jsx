import { useState } from "react";
import ChatBox from "../components/ChatBox";
import MapView from "../components/MapView";

export default function Home() {
  const [route, setRoute] = useState(null);

  return (
    <div>

      <ChatBox
        onResult={(res) => {
          console.log("AI RESPONSE:", res);

          if (res?.data?.route) {
            setRoute(res.data.route);
          }
        }}
      />

      <MapView route={route} />

    </div>
  );
}