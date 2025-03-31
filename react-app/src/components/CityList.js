import React from 'react';
import CityCard from './CityCard';

const CityList = ({ cities, onCityDeleted, showNotification }) => {
  return (
    <div id="cityList" className="column is-offset-4 is-4">
      {cities.length > 0 ? (
        cities.map(city => (
          <CityCard key={city.id} city={city} onDelete={onCityDeleted} showNotification={showNotification} />
        ))
      ) : (
        <p className="has-text-centered">No cities added yet.</p>
      )}
    </div>
  );
};

export default CityList;
