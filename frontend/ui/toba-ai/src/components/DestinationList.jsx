import { useEffect, useRef } from "react";
import destinations from "../data/destinations";

export default function DestinationList() {
  const ref = useRef();

  useEffect(() => {
    const el = ref.current;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          el.classList.add("show");
        }
      },
      { threshold: 0.2 }
    );

    observer.observe(el);
  }, []);

  return (
    <div ref={ref} className="fade-in">
      <h2>Destinasi Trending</h2>

      <div className="grid">
        {destinations.map((d, i) => (
          <div key={i} className="card">
            <div className="image-wrap">
              <img src={d.image} />
            </div>
            <div className="card-content">
              <h3>{d.name}</h3>
              <p>⭐ {d.rating}</p>
              <p style={{ fontSize: 12, opacity: 0.6 }}>
                {d.weather} • {d.crowd}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}