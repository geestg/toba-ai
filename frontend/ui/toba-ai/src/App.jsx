import { useEffect, useState } from "react";
import { Routes, Route, useLocation } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import DestinationList from "./components/DestinationList";
import MapView from "./components/MapView";

import AboutPage from "./pages/AboutPage";
import VisitedPage from "./pages/VisitedPage";

import {
  sendMessage as apiSendMessage,
  saveUserLocation,
  getRoute,
} from "./services/api";

function ChatPage({
  messages,
  input,
  setInput,
  sendMessage,
  handleInputKeyDown,
  showQuickActions,
  onSelectDestination,
}) {
  return (
    <>
      {/* ========================================= */}
      {/* HERO */}
      {/* ========================================= */}

      <section className="hero-compact">
        <img src="/images/toba-hero.jpg" alt="Danau Toba" />

        <div className="hero-compact-content">
          <span className="hello-tag">
            Halo
          </span>

          <h1>
            Saya <span>AI Toba</span>,
            <br />
            asisten virtual pariwisata
            <br />
            Danau Toba.
          </h1>

          <p>
            Tanyakan destinasi wisata, kuliner,
            penginapan, hingga rute perjalanan
            di sekitar Danau Toba.
          </p>
        </div>
      </section>

      {/* ========================================= */}
      {/* CHAT */}
      {/* ========================================= */}

      <section className="conversation-shell">

        <div className="chat-container">

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-row ${msg.role}`}
            >

              {/* ====================== */}
              {/* TEXT */}
              {/* ====================== */}

              {msg.text && (
                <div className="chat-bubble">
                  {msg.text}
                </div>
              )}

              {/* ====================== */}
              {/* DESTINATIONS */}
              {/* ====================== */}

              {msg.destinations && (
                <div className="chat-destinations">
                  <DestinationList
                    data={{
                      destinations: msg.destinations,
                    }}
                    onSelectDestination={
                      onSelectDestination
                    }
                  />
                </div>
              )}

              {/* ====================== */}
              {/* MAP */}
              {/* ====================== */}

              {msg.route && (
                <div className="chat-map">
                  <MapView
                    route={msg.route}
                    startCoords={msg.startCoords}
                    endCoords={msg.endCoords}
                  />
                </div>
              )}

            </div>
          ))}

          {/* ========================================= */}
          {/* QUICK ACTION */}
          {/* ========================================= */}

          {showQuickActions && (
            <>
              <div className="helper-title">
                Coba pertanyaan berikut
              </div>

              <div className="features-grid">

                <div
                  className="feature-card"
                  onClick={() =>
                    sendMessage(
                      "Rekomendasikan destinasi populer di Danau Toba"
                    )
                  }
                >
                  <h3>
                    Rekomendasi Destinasi
                  </h3>

                  <p>
                    Cari tempat wisata populer.
                  </p>
                </div>

                <div
                  className="feature-card"
                  onClick={() =>
                    sendMessage(
                      "Buat itinerary 2 hari 1 malam di Samosir"
                    )
                  }
                >
                  <h3>
                    Itinerary
                  </h3>

                  <p>
                    Rencana perjalanan singkat.
                  </p>
                </div>

                <div
                  className="feature-card"
                  onClick={() =>
                    sendMessage(
                      "Kuliner khas Batak yang wajib dicoba"
                    )
                  }
                >
                  <h3>
                    Kuliner
                  </h3>

                  <p>
                    Cari makanan khas sekitar.
                  </p>
                </div>

                <div
                  className="feature-card"
                  onClick={() =>
                    sendMessage(
                      "Rute dari Medan ke Danau Toba"
                    )
                  }
                >
                  <h3>
                    Rute Perjalanan
                  </h3>

                  <p>
                    Cari jalur perjalanan terbaik.
                  </p>
                </div>

              </div>
            </>
          )}

        </div>

        {/* ========================================= */}
        {/* CHAT INPUT */}
        {/* ========================================= */}

        <div className="chat-bar">

          <input
            type="text"
            value={input}
            placeholder="Ketik pertanyaanmu di sini..."
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={handleInputKeyDown}
          />

          <button
            type="button"
            onClick={() => sendMessage()}
          >
            →
          </button>

        </div>

        <p className="chat-note">
          AI dapat memberikan kesalahan.
          Pastikan informasi penting tetap diverifikasi.
        </p>

      </section>
    </>
  );
}

function App() {

  const location = useLocation();

  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState("");

  const [activeLocation, setActiveLocation] =
    useState(null);

  const [gpsLocation, setGpsLocation] =
    useState(null);

  const [gpsActive, setGpsActive] =
    useState(false);

  const [themeMode, setThemeMode] =
    useState("siang");

  const [isSidebarOpen, setIsSidebarOpen] =
    useState(true);

  /* ========================================= */
  /* GEOLOCATION */
  /* ========================================= */

  useEffect(() => {

    if (!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(
      (position) => {

        const coords = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        setGpsLocation(coords);

        setActiveLocation({
          name: "Lokasi Saya",
          ...coords,
        });

        setGpsActive(true);

        saveUserLocation(
          coords.lat,
          coords.lng
        );
      },

      (error) => {
        console.warn(
          "Geolocation gagal:",
          error.message
        );
      }
    );

  }, []);

  /* ========================================= */
  /* THEME */
  /* ========================================= */

  useEffect(() => {

    document.body.dataset.theme =
      themeMode;

    return () => {
      delete document.body.dataset.theme;
    };

  }, [themeMode]);

  /* ========================================= */
  /* SELECT DESTINATION */
  /* ========================================= */

  const handleSelectDestination = (
    destination
  ) => {

    sendMessage(
      `Pilih ${destination.name}`,
      destination
    );

  };

  /* ========================================= */
  /* SEND MESSAGE */
  /* ========================================= */

  const sendMessage = async (
    customText,
    destinationPayload = null
  ) => {

    const text = customText || input;

    if (!text.trim()) return;

    /* USER MESSAGE */

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text,
      },
    ]);

    setInput("");

    try {

      const data = await apiSendMessage(
        text,
        destinationPayload,
        gpsLocation
      );

      const botMessage = {
        role: "bot",
        text:
          data.reply ||
          "Saya belum menemukan jawaban yang sesuai.",
      };

      /* DESTINATIONS */

      if (
        data.data?.destinations
      ) {
        botMessage.destinations =
          data.data.destinations;
      }

      /* ROUTE */

      if (
        data.data?.route
      ) {
        botMessage.route =
          data.data.route;

        botMessage.startCoords =
          data.data.start;

        botMessage.endCoords =
          data.data.end;
      }

      setMessages((prev) => [
        ...prev,
        botMessage,
      ]);

    } catch (error) {

      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text:
            "Server backend sedang bermasalah.",
        },
      ]);

    }

  };

  /* ========================================= */
  /* INPUT ENTER */
  /* ========================================= */

  const handleInputKeyDown = (
    event
  ) => {

    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }

  };

  const showQuickActions =
    messages.length === 0;

  const isChatPage =
    location.pathname === "/";

  return (
    <div
      className={`app-shell ${
        isSidebarOpen
          ? "sidebar-open"
          : "sidebar-collapsed"
      }`}
    >

      {/* ========================================= */}
      {/* SIDEBAR */}
      {/* ========================================= */}

      <Sidebar
        isOpen={isSidebarOpen}
        onToggle={() =>
          setIsSidebarOpen((prev) => !prev)
        }
        gpsActive={gpsActive}
        location={gpsLocation}
        themeMode={themeMode}
        onToggleTheme={() =>
          setThemeMode((prev) =>
            prev === "siang"
              ? "malam"
              : "siang"
          )
        }
      />

      {/* ========================================= */}
      {/* MAIN */}
      {/* ========================================= */}

      <main className="main-panel">

        {isChatPage && (
          <Navbar
            activeLocation={
              activeLocation
            }
          />
        )}

        <Routes>

          <Route
            path="/"
            element={
              <ChatPage
                messages={messages}
                input={input}
                setInput={setInput}
                sendMessage={sendMessage}
                handleInputKeyDown={
                  handleInputKeyDown
                }
                showQuickActions={
                  showQuickActions
                }
                onSelectDestination={
                  handleSelectDestination
                }
              />
            }
          />

          <Route
            path="/about"
            element={<AboutPage />}
          />

          <Route
            path="/riwayat"
            element={<VisitedPage />}
          />

        </Routes>

      </main>

    </div>
  );
}

export default App;