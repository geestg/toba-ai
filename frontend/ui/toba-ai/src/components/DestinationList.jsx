export default function DestinationList({
  data,
  onSelectDestination,
}) {

  const destinations =
    data?.destinations || [];

  if (!destinations.length) {
    return null;
  }

  return (

    <div className="recommendation-grid">

      {destinations.map(
        (destination, index) => (

          <div
            key={index}
            className="recommendation-card"
          >

            <img
              src={destination.image}
              alt={destination.name}
              className="recommendation-image"
            />

            <div className="recommendation-content">

              <div className="recommendation-top">

                <h3>
                  {destination.name}
                </h3>

                <span className="recommendation-rating">
                   {destination.rating}
                </span>

              </div>

              <p>
                {destination.description}
              </p>

              <div className="recommendation-meta">

                <span>
                   {destination.area}
                </span>

                <span>
                   {destination.crowd}
                </span>

              </div>

              <button
                className="recommendation-button"
                onClick={() =>
                  onSelectDestination(
                    destination
                  )
                }
              >
                Lihat Detail
              </button>

            </div>

          </div>
        )
      )}

    </div>
  );
}