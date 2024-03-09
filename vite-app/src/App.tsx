import React, { useState } from 'react';
import './App.css';

function App() {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [routeInfo, setRouteInfo] = useState({ directions: [{
    narrative: '',
    distance: '',
  }], distance: '', formattedTime: '', status: '' });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
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

  return (
    <div className="App">
      <header className="App-header">
        <h1>Route Finder</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            placeholder="Starting Location"
            required
          />
          <input
            type="text"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="Destination"
            required
          />
          <button type="submit">Find Route</button>
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
      </header>
    </div>
  );
}

export default App;
