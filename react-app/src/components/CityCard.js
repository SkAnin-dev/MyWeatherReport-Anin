import React, { useEffect, useState } from 'react';
import { AJAX } from '../constant';

const CityCard = ({ city, onDelete, showNotification }) => {
  const [weather, setWeather] = useState({
    temp: "[??]° C",
    cond: "No information",
    icon: "/media/none.png"
  });

  const getLocalTime = () => new Date();
  const parseSunTime = (timeStr) => timeStr ? new Date(timeStr) : null;

  useEffect(() => {
    const fetchWeatherData = () => {
      const apikey = '83MPJTJKXE4NAFC8UB3TK53YA';
      const apiUrl = `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${encodeURIComponent(city.name)}?unitGroup=metric&key=${apikey}&contentType=json`;
      
      fetch(apiUrl)
        .then(response => {
          if (!response.ok) throw new Error("Weather API error");
          return response.json();
        })
        .then(data => {
          const currentData = data.currentConditions || (data.days && data.days.length > 0 ? data.days[0] : null);
          if (currentData && typeof currentData.temp !== 'undefined' && currentData.conditions) {
            let sunriseEpoch, sunsetEpoch;
            if (currentData.sunriseEpoch && currentData.sunsetEpoch) {
              sunriseEpoch = currentData.sunriseEpoch;
              sunsetEpoch = currentData.sunsetEpoch;
            } else if (data.days && data.days.length > 0) {
              sunriseEpoch = data.days[0].sunriseEpoch;
              sunsetEpoch = data.days[0].sunsetEpoch;
            }
            let dayTime = true;
            if (sunriseEpoch && sunsetEpoch) {
              const nowEpoch = Date.now() / 1000;
              dayTime = (nowEpoch >= sunriseEpoch && nowEpoch < sunsetEpoch);
            } else {
              const sunrise = currentData.sunrise ? parseSunTime(currentData.sunrise) : null;
              const sunset = currentData.sunset ? parseSunTime(currentData.sunset) : null;
              dayTime = (sunrise && sunset) ? (getLocalTime() >= sunrise && getLocalTime() < sunset) : true;
            }
            let iconFile = "none.png";
            const condition = currentData.conditions.toLowerCase();
            if (condition.includes("thunder")) {
              if (condition.includes("showers")) {
                iconFile = dayTime ? "thunder-showers-day.png" : "thunder-showers-night.png";
              } else if (condition.includes("rain")) {
                iconFile = "thunder-rain.png";
              } else {
                iconFile = "thunder.png";
              }
            } else if (condition.includes("rain") && condition.includes("snow")) {
              iconFile = "rain-snow.png";
            } else if (condition.includes("rain") && condition.includes("showers")) {
              iconFile = dayTime ? "showers-day.png" : "showers-night.png";
            } else if (condition.includes("rain")) {
              iconFile = "rain.png";
            } else if (condition.includes("snow") && condition.includes("showers")) {
              iconFile = dayTime ? "snow-showers-day.png" : "snow-showers-night.png";
            } else if (condition.includes("snow")) {
              iconFile = "snow.png";
            } else if (condition.includes("sleet")) {
              iconFile = "sleet.png";
            } else if (condition.includes("fog")) {
              iconFile = "fog.png";
            } else if (condition.includes("hail")) {
              iconFile = "hail.png";
            } else if (condition.includes("wind")) {
              iconFile = "wind.png";
            } else if (condition.includes("clear")) {
              iconFile = dayTime ? "clear-day.png" : "clear-night.png";
            } else if (condition.includes("partly") && condition.includes("cloudy")) {
              iconFile = dayTime ? "partly-cloudy-day.png" : "partly-cloudy-night.png";
            } else if (condition.includes("overcast")) {
              iconFile = "cloudy.png";
            } else if (condition.includes("cloudy")) {
              if (currentData.cloudcover !== undefined && currentData.cloudcover < 80) {
                iconFile = dayTime ? "partly-cloudy-day.png" : "partly-cloudy-night.png";
              } else {
                iconFile = "cloudy.png";
              }
            }
            setWeather({
              temp: `${currentData.temp}° C`,
              cond: currentData.conditions,
              icon: `/media/${iconFile}`
            });
          } else {
            console.error("Incomplete weather data for", city.name);
            setWeather({
              temp: "[??]° C",
              cond: "No information",
              icon: "/media/none.png"
            });
          }
        })
        .catch(err => {
          console.error("Error fetching weather for", city.name, err);
          setWeather({
            temp: "[??]° C",
            cond: "No information",
            icon: "/media/none.png"
          });
        });
    };

    fetchWeatherData();
  }, [city.name]);

  // Always send a DELETE request for any city, including default cities.
  const handleDelete = () => {
    fetch(`${AJAX}cities/${city.id}/delete/`, {
      method: 'DELETE',
      credentials: 'include'
    })
      .then(async res => {
        let data = {};
        try {
          data = await res.json();
        } catch (e) {
          if (res.ok) data.success = true;
        }
        if (res.ok && (data.status === 'success' || data.success)) {
          onDelete(city.id);
          showNotification({ type: 'success', message: `Successfully deleted '${city.name}'` });
        } else {
          const errMsg = data.message || "Error deleting city!";
          console.error("Error deleting city:", errMsg);
          showNotification({ type: 'danger', message: errMsg });
        }
      })
      .catch(err => {
        console.error("Network error deleting city", err);
        showNotification({ type: 'danger', message: "Network error or server not reachable!" });
      });
  };

  return (
    <div className="box city-box" data-city-id={city.id}>
      <article className="media">
        <div className="media-left">
          <figure className="image is-64x64">
            <img src={weather.icon} alt="Weather Icon" />
          </figure>
        </div>
        <div className="media-content">
          <div className="content">
            <p>
              <span className="title" style={{ fontWeight: 'normal' }}>{city.name}</span><br />
              <span className="subtitle" id={`temp-${city.id}`}>{weather.temp}</span><br />
              <span className="condition" id={`cond-${city.id}`}>{weather.cond}</span>
            </p>
          </div>
        </div>
        <div className="media-right">
          <button className="delete" onClick={handleDelete}></button>
        </div>
      </article>
    </div>
  );
};

export default CityCard;
