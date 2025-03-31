import React, { useState } from 'react';
import { AJAX, PROXY } from '../constant';

const AddCityForm = ({ cities, onCityAdded, showNotification }) => {
  const [cityName, setCityName] = useState('');

  // Retrieve CSRF token from cookies.
  const getCSRFToken = () => {
    const match = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'));
    return match ? match[2] : '';
  };

  // Validate city by using the Django proxy endpoint.
  const validateCity = (name) => {
    const url = `${PROXY}weather/${encodeURIComponent(name)}/`;
    return fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error("City not found");
        }
        return response.json();
      })
      .then(data => {
        // Check if the response contains current conditions or day data.
        if (data.currentConditions || (data.days && data.days.length > 0)) {
          return true;
        }
        throw new Error("City not found");
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedName = cityName.trim();
    if (!trimmedName) return;

    // Check for duplicate city.
    if (cities.some(city => city.name.toLowerCase() === trimmedName.toLowerCase())) {
      showNotification({
        type: 'danger',
        message: `City '${trimmedName}' already exists in the list!`
      });
      return;
    }

    // First, validate the city via the proxy.
    validateCity(trimmedName)
      .then(() => {
        // City is valid. Create FormData and send the POST request.
        const formData = new FormData(e.target);
        fetch(`${AJAX}cities/add/`, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'X-CSRFToken': getCSRFToken()
          },
          body: formData
        })
          .then(res => res.json())
          .then(data => {
            if (data.status === 'success') {
              showNotification({
                type: 'success',
                message: "City added successfully!"
              });
              onCityAdded(data.city);
              setCityName('');
            } else {
              showNotification({
                type: 'danger',
                message: `City '${trimmedName}' already exists in the list!`
              });
            }
          })
          .catch(err => {
            console.error('Error adding city:', err);
            showNotification({
              type: 'danger',
              message: `Error adding city '${trimmedName}'`
            });
          });
      })
      .catch(err => {
        console.error("City validation failed:", err);
        showNotification({
          type: 'danger',
          message: `City '${trimmedName}' does not exist in the world!`
        });
      });
  };

  return (
    <div>
      <form id="addCityForm" onSubmit={handleSubmit}>
        <div className="field has-addons">
          <div className="control is-expanded">
            <input
              className="input"
              name="name"
              type="text"
              placeholder="City Name"
              required
              value={cityName}
              onChange={e => setCityName(e.target.value)}
            />
          </div>
          <div className="control">
            <button className="button is-info" type="submit">
              Add City
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default AddCityForm;
