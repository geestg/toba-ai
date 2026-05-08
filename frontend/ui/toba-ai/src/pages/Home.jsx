import { useState } from "react";

import HeroSection from "../components/HeroSection";

import ChatBox from "../components/ChatBox";

import RecommendationCard from "../components/RecommendationCard";

import MapView from "../components/MapView";

import CulinaryCard from "../components/CulinaryCard";

import HotelCard from "../components/HotelCard";


export default function Home() {

  const [response, setResponse] = useState(null);

  return (

    <div className="home-page">

      {/* ========================= */}
      {/* HERO */}
      {/* ========================= */}

      <HeroSection />

      {/* ========================= */}
      {/* CHAT */}
      {/* ========================= */}

      <ChatBox
        onResult={(res) => {

          console.log("AI RESPONSE:", res);

          setResponse(res);
        }}
      />

      {/* ========================= */}
      {/* RECOMMENDATION */}
      {/* ========================= */}

      {response?.data?.destinations && (

        <RecommendationCard
          destinations={response.data.destinations}
        />
      )}

      {/* ========================= */}
      {/* FOOD */}
      {/* ========================= */}

      {response?.data?.foods && (

        <CulinaryCard
          data={response.data.foods}
        />
      )}

      {/* ========================= */}
      {/* HOTEL */}
      {/* ========================= */}

      {response?.data?.hotels && (

        <HotelCard
          hotels={response.data.hotels}
        />
      )}

      {/* ========================= */}
      {/* MAP */}
      {/* ========================= */}

      {response?.data?.route && (

        <MapView
          route={response.data.route}
        />
      )}

    </div>
  );
}