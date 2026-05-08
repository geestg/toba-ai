export default function Navbar({
  activeLocation,
}) {

  return (

    <header className="topbar">

      {/* ===================================== */}
      {/* LEFT */}
      {/* ===================================== */}

      <div className="topbar-left">

        <span className="topbar-label">
          AI Tourism Platform
        </span>

        <h1 className="topbar-title">
          AI Toba Assistant
        </h1>

        <p className="topbar-subtitle">
          Smart recommendation system untuk
          wisata Danau Toba.
        </p>

      </div>

      {/* ===================================== */}
      {/* RIGHT */}
      {/* ===================================== */}

      <div className="topbar-right">

        {activeLocation && (

          <div className="location-badge">

            <span className="location-dot" />

            <span>
              {activeLocation.name}
            </span>

          </div>
        )}

      </div>

    </header>
  );
}