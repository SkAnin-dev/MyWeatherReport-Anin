import React, { useState, useEffect, useRef, useCallback } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Marquee from './components/Marquee';
import AddCityForm from './components/AddCityForm';
import CityList from './components/CityList';
import Footer from './components/Footer';
import Notification from './components/Notification';
import { API } from './constant';

// The list of default cities, no longer used to auto-refresh deleted cities.
//const DEFAULT_CITIES = ['Tokyo', 'New York', 'London'];

function App() {
  // Initialise cities from localStorage as a fallback.
  const [cities, setCities] = useState(() => {
    const stored = localStorage.getItem('cities');
    return stored ? JSON.parse(stored) : [];
  });
  const [notification, setNotification] = useState(null);
  const formRef = useRef(null);

  // Update localStorage when cities change.
  const updateLocalStorage = (newCities) => {
    localStorage.setItem('cities', JSON.stringify(newCities));
  };

  // syncCities fetches the current list from the backend.
  const syncCities = useCallback(() => {
    fetch(API + 'cities/', { credentials: 'include' })
      .then(response => response.json())
      .then(data => {
        setCities(data);
        updateLocalStorage(data);
        // (Default cities are no longer re-added here.)
      })
      .catch(err => console.error("Error syncing cities:", err));
  }, []);

  // Initial sync on mount.
  useEffect(() => {
    syncCities();
  }, [syncCities]);

  const showNotification = (notif) => {
    setNotification(notif);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // For both add and delete actions, we simply sync the list.
  const addCity = () => {
    syncCities();
  };

  const removeCity = () => {
    syncCities();
  };

  return (
    <div>
      <Header />
      <Hero />
      <Marquee />
      <section
        className="section"
        style={{
          background: "url('/media/metofficegovuk_heroXLarge.jpeg') no-repeat center center",
          backgroundSize: 'cover'
        }}
      >
        <div className="container">
          <div className="columns">
            <div className="column is-offset-4 is-4" ref={formRef}>
              <AddCityForm
                cities={cities}
                onCityAdded={addCity}
                showNotification={showNotification}
              />
              {notification && (
                <Notification
                  type={notification.type}
                  message={notification.message}
                  onClose={() => setNotification(null)}
                />
              )}
            </div>
          </div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <div className="columns">
            <CityList
              cities={cities}
              onCityDeleted={removeCity}
              showNotification={showNotification}
            />
          </div>
        </div>
      </section>
      <hr style={{ borderTop: "2px solid #000", marginBottom: 0 }} />
      <Footer />
    </div>
  );
}

export default App;
