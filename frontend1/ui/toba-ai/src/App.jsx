import "./App.css";
import { useEffect, useState } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import MapView from "./components/MapView";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import VisitedPage from "./pages/VisitedPage";
import AboutPage from "./pages/AboutPage";
import DestinationList from "./components/DestinationList";
import { sendMessage as apiSendMessage, saveUserLocation, getRoute } from "./services/api";

function ChatPage({
  messages,
  setMessages,
  input,
  setInput,
  sendMessage,
  handleInputKeyDown,
  showQuickActions,
  activeLocation,
  onSelectDestination,
  selectedDestination,
}) {
  return (
    <>
      <section className="hero-compact">
        <img src="/images/toba.jpg" alt="Danau Toba" />
        <div className="hero-compact-content">
          <span className="hello-tag">Halo! 👋</span>
          <h1>
            Saya <span>AI Toba</span>,
            <br />
            asisten virtual pariwisata
            <br />
            Danau Toba.
          </h1>
          <p>
            Tanyakan apa saja tentang destinasi, aktivitas, kuliner,
            <br />
            budaya, atau tips liburan. Saya siap membantu!
          </p>
        </div>
      </section>

      <section className="conversation-shell" id="chat">
        <div className="chat-container">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-row ${msg.role}`}>
              {msg.text && (
                <div className="chat-bubble">
                  {msg.text}
                </div>
              )}

              {msg.destinations && (
                <div className="chat-destinations">
                  <DestinationList
                    data={{ destinations: msg.destinations }}
                    onSelectDestination={onSelectDestination}
                  />
                </div>
              )}

              {msg.route && (
                <div className="chat-map">
                  <MapView
                    route={msg.route}
                    startCoords={msg.startCoords}
                    endCoords={msg.endCoords}
                  />
                </div>
              )}

              {msg.impact && (
                <div className="chat-impact">
                  Crowd: {msg.impact.before} → {msg.impact.after}
                </div>
              )}

              {msg.followUpOptions && (
                <div className="follow-up-options">
                  <p className="follow-up-text">{msg.followUpText}</p>
                  <div className="follow-up-buttons">
                    {msg.followUpOptions.map((opt, idx) => (
                      <button
                        key={idx}
                        className="follow-up-button"
                        onClick={() => sendMessage(opt.action)}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}

          {showQuickActions && (
            <>
              <div className="helper-title">Atau coba tanyakan ini</div>
              <div className="features-grid">
                <div className="feature-card" onClick={() => sendMessage("Rekomendasikan destinasi populer sekitar saya")}>
                  <div className="feature-icon feature-icon-green">📍</div>
                  <h3>Rekomendasi Destinasi</h3>
                  <p>Dapatkan destinasi populer sekitar kamu.</p>
                </div>

                <div className="feature-card" onClick={() => sendMessage("Buat itinerary 2 hari 1 malam di Samosir")}>
                  <div className="feature-icon feature-icon-blue">📅</div>
                  <h3>Rencana Perjalanan</h3>
                  <p>Buat itinerary 2 hari 1 malam di Samosir.</p>
                </div>

                <div className="feature-card" onClick={() => sendMessage("Cicipi makanan Batak yang wajib dicoba")}>
                  <div className="feature-icon feature-icon-orange">🍴</div>
                  <h3>Kuliner Khas</h3>
                  <p>Cicipi makanan Batak yang wajib dicoba.</p>
                </div>

                <div className="feature-card" onClick={() => sendMessage("Cara menuju Danau Toba dari Medan")}>
                  <div className="feature-icon feature-icon-purple">🚘</div>
                  <h3>Transportasi</h3>
                  <p>Cara menuju Danau Toba dari Medan.</p>
                </div>
              </div>
            </>
          )}
        </div>

        <div className="chat-bar">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleInputKeyDown}
            placeholder="Ketik pertanyaanmu di sini..."
          />
          <button onClick={() => sendMessage()} type="button">
            ↗
          </button>
        </div>

        <p className="chat-note">AI Toba dapat membuat kesalahan. Informasi penting, harap diverifikasi kembali.</p>
      </section>
    </>
  );
}

function App() {
  const location = useLocation();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [activeLocation, setActiveLocation] = useState(null);
  const [selectedDestination, setSelectedDestination] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [themeMode, setThemeMode] = useState("siang");
  const [gpsActive, setGpsActive] = useState(false);
  const [gpsLocation, setGpsLocation] = useState(null);
  const [visitedDestinations, setVisitedDestinations] = useState(() => {
    const saved = localStorage.getItem("toba-visited");
    return saved ? JSON.parse(saved) : [];
  });

  // Auto-request browser geolocation on mount
  useEffect(() => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const loc = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          handleToggleGPS(loc);
        },
        (error) => {
          console.warn("Geolocation denied or failed:", error.message);
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
      );
    }
  }, []);

  useEffect(() => {
    document.body.dataset.theme = themeMode;
    return () => {
      delete document.body.dataset.theme;
    };
  }, [themeMode]);

  const handleToggleGPS = (location) => {
    setGpsLocation(location);
    setGpsActive(true);
    setActiveLocation({ name: "Lokasi Saya", ...location });
    saveUserLocation(location.lat, location.lng);
  };

  const exampleLocations = {
    "berastagi": { lat: 2.96833, lng: 98.51833 },
    "sibayak": { lat: 2.95, lng: 98.50 },
    "tip top": { lat: 2.18956, lng: 98.67428 },
    "merdeka": { lat: 2.20559, lng: 98.67003 },
    "polda": { lat: 2.19945, lng: 98.68087 },
  };

  const geocodeLocation = async (locationString) => {
    try {
      const viewbox = "95.0,-11.0,141.0,6.0";
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
          locationString
        )}&format=json&limit=1&countrycodes=id&viewbox=${viewbox}&bounded=1`
      );
      const data = await response.json();

      if (data.length > 0) {
        const result = {
          lat: parseFloat(data[0].lat),
          lng: parseFloat(data[0].lon),
        };
        console.log(`Geocoded "${locationString}" →`, result);
        return result;
      }
      console.warn(`Geocoding failed for "${locationString}"`);
      return null;
    } catch (error) {
      console.error("Geocoding error:", error);
      return null;
    }
  };

  const parseLocation = async (locationString) => {
    const normalized = locationString.toLowerCase().trim();

    if (exampleLocations[normalized]) {
      return exampleLocations[normalized];
    }

    const coordMatch = locationString.match(
      /(-?\d+\.?\d*)\s*[,\s]\s*(-?\d+\.?\d*)/
    );
    if (coordMatch) {
      return {
        lat: parseFloat(coordMatch[1]),
        lng: parseFloat(coordMatch[2]),
      };
    }

    return await geocodeLocation(locationString);
  };

  const handleRouteRequest = async (text, useActiveLocation = false) => {
    const lower = text.toLowerCase();
    if (!lower.includes("rute") && !lower.includes("jarak") && !useActiveLocation) return null;

    let startLocationStr;
    let endLocationStr;
    let startCoords = null;

    if (useActiveLocation && activeLocation) {
      startLocationStr = activeLocation.name || "Lokasi Saya";
      startCoords = { lat: activeLocation.lat, lng: activeLocation.lng };

      const routePattern = /(?:rute|jarak).*?\bke\b\s+(.+?)(?:\s*[?!.])?\s*$/i;
      const match = text.match(routePattern);
      endLocationStr = match ? match[1]?.trim() : null;
    } else {
      const routePattern = /(?:rute|jarak)\s+(?:dari\s+)?(.+?)\s+ke\s+(.+?)(?:\s*[?!.])?\s*$/i;
      const match = text.match(routePattern);

      if (!match) {
        console.log("Route pattern not matched");
        return null;
      }

      startLocationStr = match[1]?.trim();
      endLocationStr = match[2]?.trim();
    }

    if (startLocationStr) startLocationStr = startLocationStr.replace(/[!?.]*$/, "").trim();
    if (endLocationStr) endLocationStr = endLocationStr.replace(/[!?.]*$/, "").trim();

    console.log("Parsed input - Start:", startLocationStr, "End:", endLocationStr);

    if (!startLocationStr || !endLocationStr) {
      return null;
    }

    try {
      if (!startCoords) {
        startCoords = await parseLocation(startLocationStr);
      }
      const endCoords = await parseLocation(endLocationStr);

      console.log("Geocoded coords - Start:", startCoords, "End:", endCoords);

      if (!startCoords || !endCoords) {
        return {
          error: `Lokasi tidak ditemukan: "${startLocationStr}" atau "${endLocationStr}". Format: "rute dari medan ke sibolga" atau aktifkan GPS lalu ketik "rute ke sibolga"`,
        };
      }

      const routeData = await getRoute(startCoords, endCoords);

      if (!routeData.routes || routeData.routes.length === 0) {
        return { error: "Rute tidak ditemukan antara kedua lokasi" };
      }

      const route = routeData.routes[0];
      const distance = (route.summary.distance / 1000).toFixed(2);
      const duration = Math.round(route.summary.duration / 60);
      const routeGeometry = route.geometry || [];

      console.log("Route ready - distance:", distance, "km, geometry points:", routeGeometry.length);

      return {
        success: true,
        distance,
        duration,
        startLocationStr,
        endLocationStr,
        routeGeometry: routeGeometry,
        startCoords,
        endCoords,
      };
    } catch (error) {
      console.error("Route request error:", error);
      return {
        error: `Error: ${error.message}`,
      };
    }
  };

  const addToVisited = (destination) => {
    if (!destination || !destination.name) return;
    setVisitedDestinations((prev) => {
      const exists = prev.find((d) => d.name === destination.name);
      if (exists) return prev;
      const updated = [
        { ...destination, visitedAt: new Date().toISOString() },
        ...prev,
      ];
      localStorage.setItem("toba-visited", JSON.stringify(updated));
      return updated;
    });
  };

  const handleSelectDestination = (destination) => {
    setSelectedDestination(destination);
    addToVisited(destination);
    // Send select intent to backend
    sendMessage(`Pilih ${destination.name}`, destination);
  };

  const sendMessage = async (customText, destinationPayload = null) => {
    const text = customText || input;
    if (!text) return;

    setMessages((prev) => [...prev, { role: "user", text }]);

    const useActiveForRoute = activeLocation && text.toLowerCase().includes("rute") && text.toLowerCase().includes("ke");
    const routeResult = await handleRouteRequest(text, useActiveForRoute);

    if (routeResult) {
      if (routeResult.error) {
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: `❌ ${routeResult.error}` },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "bot",
            text: `✅ Rute dari ${routeResult.startLocationStr} ke ${routeResult.endLocationStr}:\n📍 Jarak: ${routeResult.distance} km\n⏱️ Durasi: ${routeResult.duration} menit`,
            route: routeResult.routeGeometry,
            startCoords: routeResult.startCoords,
            endCoords: routeResult.endCoords,
          },
        ]);
      }
      setInput("");
      return;
    }

    try {
      // Build mobile data from GPS if available
      let mobileData = null;
      if (gpsLocation) {
        mobileData = {
          data_source: "app_gps",
          device_lat: gpsLocation.lat,
          device_lng: gpsLocation.lng,
          sample_size: 100,
        };
      }

      const data = await apiSendMessage(text, destinationPayload, mobileData);

      if (data.reply) {
        const botMsg = { role: "bot", text: data.reply };

        // If recommendation intent, render destinations
        if (data.intent === "recommendation" && data.data?.destinations) {
          botMsg.destinations = data.data.destinations;
        }

        // If select_destination intent, show follow-up options
        if (data.intent === "select_destination") {
          botMsg.followUpText = "Mau saya bantu dengan apa selanjutnya?";
          botMsg.followUpOptions = [
            { label: "🗺️ Buat Rute", action: `Buat rute ke ${data.data?.selected_destination?.name || "destinasi"}` },
            { label: "🍽️ Cari Rumah Makan", action: "Cari rumah makan sekitar" },
            { label: "🏨 Cari Penginapan", action: "Cari penginapan sekitar" },
          ];
          setSelectedDestination(data.data?.selected_destination || null);
          addToVisited(data.data?.selected_destination);
        }

        // If route intent from backend
        if (data.intent === "route" && data.data?.route) {
          botMsg.route = data.data.route;
          botMsg.startCoords = data.data.start;
          botMsg.endCoords = data.data.end;
          
        }

        setMessages((prev) => [...prev, botMsg]);
      }

      if (data.data?.route && data.intent !== "route") {
        setMessages((prev) => [
          ...prev,
          { role: "bot", route: data.data.route },
        ]);
      }

      if (data.data?.impact) {
        setMessages((prev) => [
          ...prev,
          { role: "bot", impact: data.data.impact },
        ]);
      }

    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Server error, backend lagi lucak." },
      ]);
    }

    setInput("");
  };

  const handleInputKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  };

  const showQuickActions = messages.length === 0 && !input.trim();

  const isChatPage = location.pathname === "/";

  return (
    <div className={`app-shell ${isSidebarOpen ? "sidebar-open" : "sidebar-collapsed"} ${themeMode === "malam" ? "theme-night" : "theme-day"}`}>
      <Sidebar
        isOpen={isSidebarOpen}
        onToggle={() => setIsSidebarOpen((prev) => !prev)}
        themeMode={themeMode}
        onToggleTheme={() => setThemeMode((prev) => (prev === "siang" ? "malam" : "siang"))}
        gpsActive={gpsActive}
        location={gpsLocation}
        onToggleGPS={handleToggleGPS}
      />

      <main className="main-panel">
        {isChatPage && <Navbar activeLocation={activeLocation} onSetLocation={handleToggleGPS} />}

        <Routes>
          <Route
            path="/"
            element={
              <ChatPage
                messages={messages}
                setMessages={setMessages}
                input={input}
                setInput={setInput}
                sendMessage={sendMessage}
                handleInputKeyDown={handleInputKeyDown}
                showQuickActions={showQuickActions}
                activeLocation={activeLocation}
                onSelectDestination={handleSelectDestination}
                selectedDestination={selectedDestination}
              />
            }
          />
          <Route path="/riwayat" element={<VisitedPage />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

