import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import GuestForm from "./GuestForm";

function Home() {
  const [{ data: episode, error, status }, setEpisode] = useState({
    data: null,
    error: null,
    status: "pending",
  });
  const { id } = useParams();

  useEffect(() => {
    fetch(`/episodes/${id}`).then((r) => {
      if (r.ok) {
        r.json().then((episode) =>
          setEpisode({ data: episode, error: null, status: "resolved" })
        );
      } else {
        r.json().then((err) =>
          setEpisode({ data: null, error: err.error, status: "rejected" })
        );
      }
    });
  }, [id]);

  function handleAddGuest(newGuest) {
    setEpisode({
      data: {
        ...episode,
        guests: [...episode.guests, newGuest],
      },
      error: null,
      status: "resolved",
    });
  }

  if (status === "pending") return <h1>Loading...</h1>;
  if (status === "rejected") return <h1>Error: {error.error}</h1>;

  return (
    <section className="container">
      <div className="card">
        <h1>
          Episode {episode.number} - {episode.date}
        </h1>
      </div>
      <div className="card">
        <h2>Guest List</h2>
        {episode?.guests?.map((guest) => (
          <div key={guest.id}>
            <h3>{guest.name}</h3>
            <p>
              <em>{guest.occupation}</em>
            </p>
          </div>
        ))}
      </div>
      <div className="card">
        <h3>Add New Guest</h3>
        <GuestForm episodeId={episode.id} onAddGuest={handleAddGuest} />
      </div>
    </section>
  );
}

export default Home;
