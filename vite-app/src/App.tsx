import React, { useState } from 'react';
import './App.css';

function App() {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [lat, setLat] = useState('');
  const [lng, setLng] = useState('');
  const [routeInfo, setRouteInfo] = useState({ directions: [{ narrative: '', distance: '', }], distance: '', formattedTime: '', status: '' });
  const [sunInfo, setSunInfo] = useState({ sunrise: '', sunset: '' });

  const handleRouteSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/route', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ origin, destination }),
      });
      const data = await response.json();
      setRouteInfo(data);
    } catch (error) {
      console.error("Failed to fetch", error);
    }
  };

  const handleSunSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:5000/sun`,
      { method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ lat, lng }),
      });
      const data = await response.json();
    
        setSunInfo({
          sunrise: data.results.sunrise,
          sunset: data.results.sunset,
    });
      }
     catch (error) {
      console.error("Failed to fetch", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Route and Sun Times Finder</h1>
        <form onSubmit={handleRouteSubmit}>
          <input type="text" value={origin} onChange={(e) => setOrigin(e.target.value)} placeholder="Starting Location" required />
          <input type="text" value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="Destination" required />
          <button type="submit">Find Route</button>
        </form>

        <form onSubmit={handleSunSubmit}>
          <input type="text" value={lat} onChange={(e) => setLat(e.target.value)} placeholder="Latitude" required />
          <input type="text" value={lng} onChange={(e) => setLng(e.target.value)} placeholder="Longitude" required />
          <button type="submit">Get Sunrise and Sunset</button>
        </form>

        {routeInfo.status === 'success' && (
          <div>
            <h2>Route Details</h2>
            <p>Distance: {routeInfo.distance}</p>
            <p>Estimated Time: {routeInfo.formattedTime}</p>
            <h3>Directions</h3>
            <ol>
              {routeInfo.directions.map((step, index) => (
                <li key={index}>{step.narrative} - {step.distance}</li>
              ))}
            </ol>
          </div>
        )}

        {(sunInfo.sunrise && sunInfo.sunset) && (
          <div>
            <h2>Sunrise and Sunset Times (UTC)</h2>
            <p>Sunrise: {sunInfo.sunrise}</p>
            <p>Sunset: {sunInfo.sunset}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
